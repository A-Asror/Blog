from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from jwt import api_jwt
from rest_framework.response import Response

from account.models import Jwt


class Token:

    def token_generator(self, payload, format_time):
        data_token = {
            'id': payload,
            'exp': timezone.now() + timedelta(**format_time),  # minutes, days
            'iat': timezone.now()
        }
        token = api_jwt.encode(data_token, settings.SECRET_KEY, algorithm='HS256')
        return token


class Refresh(Token):

    def __init__(self, request):
        self.request = request

    @property
    def access_and_refresh_token(self):
        refresh = self.token_generator(self.request.user.id, {'days': 30})
        access = self.token_generator(self.request.user.id, {'days': 40})
        return access, refresh

    @property
    def check_jwt_model_and_update(self):
        jwt_user = Jwt.objects.filter(user_id=self.request.user.id)
        if not jwt_user.exists():
            return 'User not found!', False
        access, refresh = self.access_and_refresh_token
        jwt_user.update(access=access, refresh=refresh)
        return [access, refresh], True

    @property
    def create_access_refresh_token(self):
        access, refresh = self.access_and_refresh_token
        jwt_user = Jwt.objects.filter(user_id=self.request.user.id).exists()
        if not jwt_user:
            Jwt(user_id=self.request.user.id, access=access, refresh=refresh).save()
            return self._response(access, refresh)
        return self.response

    @property
    def response(self):
        data, exc = self.check_jwt_model_and_update
        if exc:
            return self._response(data[0], data[1])
        return Response({'error': data}, status=400)

    def _response(self, access, refresh):
        response = Response()
        response.set_cookie(key='_at', value=refresh, httponly=True, samesite='none')  # , samesite=None
        response.status_code = 200
        response.data = {'access': access, 'refresh': refresh}
        return response
