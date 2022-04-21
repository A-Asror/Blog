from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from base.mixins.mixins import CustomUpdateMixin, BaseMixin
from base.views.custom_generics import BaseView, CRUDAPIView, CustomUpdateAPIView, CRAPIView, \
    CustomRetrieveAPIView, AdminRUDAPIView, CustomCreateAPIView, RUAPAIView, CRUDObjectApiView
from utils.permissions import IsAuthenticatedCustom, IsAdminUserCustom, IsManagerUser
from utils.token import Refresh
from .models import User, UserProfile, Jwt, University, Faculty, Friends, Education
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, UniversitySerializer, \
    FacultySerializer, FriendsSerializer, EducationSerializer, IDFriendsSerializer


class RegistrationApiView(BaseView, APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, required=False)
        if serializer.is_valid(raise_exception=False):
            password_data = serializer.validated_data
            if password_data['password1'] != password_data['password2']:
                return Response({'error': 'passwords do not match'}, status=400)
            data = serializer.data
            data['password'] = password_data['password1']
            serializer.create(data)
            user = User.objects.get(email=data['email'])
            UserProfile(user=user).save()
            Friends(user=user).save()
            Education(user=user).save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        data = serializer.data
        if User.objects.filter(username=data['username'], email=data['email']).exists():
            return Response({'error': 'A user with the same email or username already exists'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.data
            request.user = authenticate(request, email=data['email'], password=data['password'])
            if request.user is None:
                return Response({'error': 'User not found!'}, status=401)
            return Refresh(request=request).create_access_refresh_token
        return Response({'error': 'data not valid'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        user_id = request.user.id
        Jwt.objects.filter(user_id=user_id).delete()
        response = Response()
        response.delete_cookie(key='_at')
        response.status_code = 200
        response.data = "logged out successfully"

        return response


class UsersAPIView(CRUDObjectApiView):
    # permission_classes = [IsAuthenticatedCustom]
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    queryset = UserProfile
    detail = True
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        self.serializer_context['instance'] = [self.request.user]


class RUsersAPIView(CustomRetrieveAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = ProfileSerializer
    queryset = UserProfile
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        self.serializer_context['sub_class'] = False


class FriendsAPIView(BaseView, CustomUpdateMixin):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = FriendsSerializer
    queryset = Friends
    follow = None
    remove = None
    unfollow = None

    def get(self, request, *args, **kwargs):
        self.custom(request)
        self.kwargs['pk'] = Friends.objects.get(user_id=self.request.user.pk).pk
        data, status_code = self.retrieve_or_all
        return self.check_refresh([data, status_code])

    # followers, cast = подписчики, following, fast = подписки
    def patch(self, request, *args, **kwargs):
        self.custom(request)
        serializer = IDFriendsSerializer(data=request.data)
        if serializer.is_valid():
            filter_data = {}
            self.follow = serializer.data.get('follow', False)
            self.unfollow = serializer.data.get('unfollow', False)
            self.remove = serializer.data.get('remove', False)
            filter_data['pk'] = self.follow or self.unfollow or self.remove
            instance = User.objects.filter(**filter_data)
            following_user = Friends.objects.filter(user=self.request.user)
            if instance.exists() and following_user.exists():
                self.request.instance = instance.get()
                self.request.follower_user = Friends.objects.filter(user=self.request.instance).get()
                self.request.follow_user = following_user.get()
                self.update_context()
                self.func = 1
                serializer = self.serializer_class(instance, data=request.data, partial=True, context=self.validation_context_and_filter)
                serializer.save() if serializer.is_valid(raise_exception=False) else None
                return self.check_refresh(['success saved', 201])
        return self.check_refresh([serializer.errors, 400])

    def update_context(self):
        self.serializer_context['many'] = {
            'key1': {'cast_or_fast': self.request.follow_user.following, 'follow_or_unfollow': None, 'user': self.request.instance},  # 'user': User, 'pk_user': self.request.instance.pk
            'key2': {'cast_or_fast': self.request.follower_user.followers, 'follow_or_unfollow': 'follower', 'user': self.request.user}}
        # 'user': User, 'pk_user': self.request.user.pk
        if self.follow:
            self._update_context('follow')
            # self.serializer_context['many']['key1']['follow_or_unfollow'] = 'follow'
        elif self.unfollow:
            self._update_context('unfollow')
            # self.serializer_context['many']['key1']['follow_or_unfollow'] = 'unfollow'
        elif self.remove:
            self._update_context('remove')
            self._update_context('unfollow', 'key2')
            self._update_context(self.request.follower_user.following, 'key2', 'cast_or_fast')
            self._update_context(self.request.follow_user.followers, sub_key='cast_or_fast')
            # self.serializer_context['many']['key1']['follow_or_unfollow'] = 'remove'
            # self.serializer_context['many']['key2']['follow_or_unfollow'] = 'unfollow'
            # self.serializer_context['many']['key2']['cast_or_fast'] = self.request.follower_user.following
            # self.serializer_context['many']['key1']['cast_or_fast'] = self.request.follow_user.followers

    def _update_context(self, value, key='key1', sub_key='follow_or_unfollow'):
        self.serializer_context['many'][key][sub_key] = value


# class RetrieveFriendsAPIView(CRUDObjectApiView):
#     permission_classes = [IsAuthenticatedCustom]
#     serializer_class = FriendsSerializer
#     queryset = Friends


class EducationAPIView(BaseView, APIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = EducationSerializer
    queryset = Education

    def patch(self, request, *args, **kwargs):
        pk_university = self.request.data.get('university', None)
        pk_faculty = self.request.data.get('faculty', None)
        if pk_faculty:
            faculty = Faculty.objects.filter(pk=pk_faculty)
            if faculty.exists():
                faculty = faculty.get()
                self.request.user.education.faculty = faculty
                self.request.user.education.save()
                return self.check_refresh(['success saved', 200])
            return self.check_refresh(['no data to pk', 400])
        elif pk_university:
            university = University.objects.filter(pk=pk_university)
            if university.exists():
                university = university.get()
                self.request.user.education.university = university
                self.request.user.education.save()
                return self.check_refresh(['success saved', 200])
            return self.check_refresh(['no data to pk', 400])
        return self.check_refresh(['id null', 400])
    # def update(self, faculty_or_university):

        # or pk_university:
        #     if
        #     self.filter_data['pk'] = pk
        #     self.serializer_context['foreign'] = {
        #         'key1': [Education, self.request.user.education, 'university'],
        #         'key2': [Education, self.request.user, 'faculty']}
        #     instance = self.get_object
        #     data, status_code = self.update(instance, request.data)
        #     return self.check_refresh([data, status_code])
