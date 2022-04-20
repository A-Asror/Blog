from django.utils import timezone
from django.conf import settings

from rest_framework import authentication, exceptions
import jwt

from account.models import User, Jwt


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'
    refresh = False
    request = None
    token = None

    def authenticate(self, request):
        request.user = None
        self.request = request
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            prefix = auth_header[0].decode('utf-8')
            if prefix.lower() == auth_header_prefix:
                self.token = auth_header[1].decode('utf-8')
                data, exc = self.verif_token(self.token)
                if exc:

                    if self.chek_token_life(data):
                        return self._authenticate_credentials(data)
                return self.request.user, data
        return None

    @property
    def refresh_token(self):
        cookie = self.request.COOKIES.get('_at', None)
        if cookie is not None:
            data, exc = self.verif_token(cookie)
            if exc:
                try:
                    jwt_user = Jwt.objects.get(user_id=data['id'])
                except Exception:
                    msg = 'Пользователь соответствующий данному токену не найден.'
                    return exceptions.AuthenticationFailed(msg), False
                if jwt_user.refresh != cookie:
                    msg = 'Этот Cookie уже деактивирован.'
                    return exceptions.AuthenticationFailed(msg), False
                self.refresh = True
                if self.chek_token_life(data):
                    return data, True
                msg = 'Этот Cookie уже деактивирован.'
                return exceptions.AuthenticationFailed(msg), False
        return None, None

    def _authenticate_credentials(self, payload):
        try:
            user = User.objects.get(pk=payload['id'])
        except Exception:
            msg = 'Неверный токен.'
            return self.request.user, msg
        # user.is_active = False
        if not self.refresh and user.jwt.access != self.token:
            return self.refresh_token
        if not user.is_active:
            msg = 'Данный токен пользователя деактивирован, введите логин заново.'
            return self.request.user, msg
        self.request.user = user
        if self.refresh:
            # self.request.acc = user
            self.request.user.refresh = True
            return self.request.user, True
            # return Refresh(request=self.request).response
        return self.request.user, payload

    def verif_token(self, token):
        try:
            decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return decode_data, True
        except Exception:
            if self.refresh:
                msg = 'Данный токен пользователя деактивирован, залогинтесь зново.'
                return msg, False
            self.refresh = True
            return self.refresh_token

    def chek_token_life(self, decode_data):
        exp = decode_data['exp']
        if int(timezone.now().timestamp()) < exp:
            return True
        return False
