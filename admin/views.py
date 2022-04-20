from rest_framework.views import APIView

from account.models import UserProfile, Faculty, University, Education, User
from account.serializers import ProfileSerializer, FacultySerializer, UniversitySerializer, EducationSerializer
from base.views.custom_generics import AdminRUDAPIView, CRAPIView, CustomUpdateAPIView, BaseView, CRUDObjectApiView
from myapp.models import Category, VideoPost, Article, PhotoPost
from myapp.serializers import CategorySerializer, VideoPostSerialize, PhotoPostSerialize, ArticleSerialize
from utils.permissions import IsAdminUserCustom, IsManagerUser, IsAuthenticatedCustom, CheckObjectUserInUser, IsManagerCheckObjectUserInUser


class AdminUsersAPIView(AdminRUDAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = ProfileSerializer
    queryset = UserProfile
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = user.get()
                self.kwargs['pk'] = user.profile.pk
                self.serializer_context['instance'] = [user]


class RUDAdminUniversityAPIView(AdminRUDAPIView):
    permission_classes = [IsManagerUser]
    serializer_class = UniversitySerializer
    queryset = University


class CRAdminUniversityAPIView(CRAPIView):
    permission_classes = [IsManagerUser]
    serializer_class = UniversitySerializer
    queryset = University


class RUDAdminFacultyAPIView(AdminRUDAPIView):
    permission_classes = [IsManagerUser]
    serializer_class = FacultySerializer
    queryset = Faculty


class CRAdminFacultyAPIView(CRAPIView):
    permission_classes = [IsManagerUser]
    serializer_class = FacultySerializer
    queryset = Faculty


class EducationAPIView(BaseView, APIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = EducationSerializer
    queryset = Education

    def patch(self, request, *args, **kwargs):
        pk_university = self.request.data.get('university', None)
        pk_faculty = self.request.data.get('faculty', None)
        pk_user = self.request.data.get('user', None)
        if not pk_user:
            return self.check_refresh(['id null', 400])
        user = User.objects.filter(pk=pk_user)
        if not user.exists():
            return self.check_refresh(['no data to id user', 400])
        user = user.get()
        if pk_faculty:
            faculty = Faculty.objects.filter(pk=pk_faculty)
            if faculty.exists():
                faculty = faculty.get()
                user.education.faculty = faculty
                user.education.save()
                return self.check_refresh(['success saved', 200])
            return self.check_refresh(['no data to pk', 400])
        elif pk_university:
            university = University.objects.filter(pk=pk_university)
            if university.exists():
                university = university.get()
                user.education.university = university
                user.education.save()
                return self.check_refresh(['success saved', 200])
            return self.check_refresh(['no data to pk', 400])
        return self.check_refresh(['id null', 400])


class CRAdminCategoryAPIView(CRAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = CategorySerializer
    queryset = Category


class RUDAdminCategoryAPIView(AdminRUDAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = CategorySerializer
    queryset = Category


class RUDAdminVideoPostAPIView(CRUDObjectApiView):
    permission_classes = [IsManagerCheckObjectUserInUser]
    serializer_class = VideoPostSerialize
    queryset = VideoPost  # class RUDAdmin CR APIView
    customize = True
    video = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = user.get()
                self.kwargs['pk'] = user.profile.pk
                self.serializer_context['instance'] = [user]


class RUDPhotoPostAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = PhotoPostSerialize
    queryset = PhotoPost  # class RUD CR APIView
    photo = True
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = user.get()
                self.kwargs['pk'] = user.profile.pk
                self.serializer_context['instance'] = [user]


class RUDAdminArticleAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = ArticleSerialize
    queryset = Article  # class RUDAdmin CR APIView
    photo = True
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_context(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = user.get()
                self.kwargs['pk'] = user.profile.pk
                self.serializer_context['instance'] = [user]
