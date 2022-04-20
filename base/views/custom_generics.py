import json

from rest_framework.response import Response

from account.models import User
from base.mixins.mixins import CustomDestroyModelMixin, CustomCreateMixin, BaseMixin, CustomUpdateMixin
from myapp.models import VideoPost, PhotoPost, Article, Comments
from myapp.serializers import MetaDataSerializer
from utils.permissions import IsAuthenticatedCustom
from utils.token import Refresh


class BaseView:
    """
    customize[bool] может быть
    """
    permission_classes = [IsAuthenticatedCustom]
    customize = False
    custom_funcs = []
    data = None

    def del_or_patch(self):
        # print(self.queryset.__name__)
        # if self.request.method == 'GET' and self.queryset.__name__ in ['VideoPost', 'PhotoPost', 'Article']:
        #     self.filter_data = {'is_active': True, 'is_active_admin': True}
        methods = ['PATCH', 'DELETE']
        if self.request.method in methods:
            # pk = json.loads(self.requests.data).get('pk', None)
            pk = self.kwargs.get('pk', None)
            if pk is not None:
                self.filter_data['pk'] = pk
                self.func = 0
                self._filter = False

    def custom(self, request):
        self.serializer_context = {'request': request}
        if self.customize:
            self.dict_func()
            [function() for function in self.custom_funcs] if len(self.custom_funcs) else None
        self.del_or_patch()

    def check_refresh(self, data):
        self.data = {'data': data[0], 'status': data[1]}
        return self.__check_refresh

    @property
    def __check_refresh(self):
        try:
            if self.request.user.refresh:
                response = Refresh(self.request).response
                try:
                    self.data['data'].append({'access': response.data['access']})
                except Exception:
                    self.data['data']['access'] = response.data['access']
                response.data = self.data['data']
                response.status_code = 205
                return response
        except Exception:
            return Response(**self.data)


class CustomUpdateAPIView(BaseView, CustomUpdateMixin):
    def patch(self, request, *args, **kwargs):
        self.custom(request)
        instance = self.get_object
        data, status_code = self.update(instance, request.data)
        return self.check_refresh([data, status_code])


class CustomRetrieveAPIView(BaseView, BaseMixin):
    def get(self, request, *args, **kwargs):
        self.custom(request)
        data, status_code = self.retrieve_or_all
        return self.check_refresh([data, status_code])


class CustomCreateAPIView(BaseView, CustomCreateMixin):
    def post(self, request, *args, **kwargs):
        self.custom(request)
        data, status_code = self.create(request.data)
        return self.check_refresh([data, status_code])


class CustomDestoryAPIView(BaseView, CustomDestroyModelMixin):
    def delete(self, request, *args, **kwargs):
        self.custom(request)
        pk = kwargs.get('pk', None)
        data, status_code = self.destroy(pk)
        return self.check_refresh([data, status_code])


class AdminRUDAPIView(CustomUpdateAPIView, CustomRetrieveAPIView, CustomDestoryAPIView):
    pass


class RUAPAIView(CustomRetrieveAPIView, CustomUpdateAPIView):
    pass


class CRAPIView(CustomRetrieveAPIView, CustomCreateAPIView):
    filter_data = {}


class CRUDObjectApiView(CustomRetrieveAPIView, CustomUpdateAPIView, CustomDestoryAPIView, CustomCreateAPIView):  # CustomCreateAPIView
    article = False
    detail = False
    video = False
    photo = False
    friends = False
    sub_comment = False
    comment = False
    data_serializer = None
    partial = False

    def del_or_patch(self):
        methods = ['POST', 'PATCH', 'DELETE']
        created = self.request.method == 'POST'
        update = self.request.method == 'PATCH'
        created_or_updated = ['POST', 'PATCH']
        serializer = MetaDataSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        data = serializer.data
        if self.request.method == 'GET':
            if self.queryset.__name__ == 'UserProfile':
                self.serializer_context['sub_class'] = False
            self.filter_data = {}
            if self.queryset.__name__ in ['VideoPost', 'PhotoPost', 'Article']:
                self.filter_data = {'is_active': True, 'is_active_admin': True}
        if self.request.method in created_or_updated:
            self.partial = True if update else None
            self.data_serializer = self.get_serializer(data=self.request.data, context=self.validation_context_and_filter, partial=self.partial)
            self.data_serializer.is_valid(raise_exception=True)
        if self.request.method in methods:
            pk = None
            if self.detail:
                pk = self.request.user.profile.pk
            elif self.video:
                pk = data.get('id_video', None)
                self.serializer_context['create'] = VideoPost
                self.serializer_context['key'] = 'video'
                self.request.content_data = self.data_serializer.validated_data['video'] if created else None
            elif self.photo:
                pk = data.get('id_photo', None)
                self.serializer_context['key'] = 'photo'
                self.serializer_context['create'] = PhotoPost
                self.request.content_data = self.data_serializer.validated_data['photo'] if created else None
            elif self.article:
                pk = data.get('id_article', None)
                self.serializer_context['create'] = Article
                self.serializer_context['key'] = 'video'
                self.request.photos = self.data_serializer.validated_data.pop('photos', False)
                self.request.content_data = self.data_serializer.validated_data['video'] if created else None
            elif self.comment:
                pk = data.get('id_comment', None)
                self.serializer_context['create'] = Comments
            elif self.sub_comment:
                pk = data.get('id_sub_comment', None)
                self.serializer_context['create'] = Comments
                # self.serializer_context['key'] = 'video'
                # self.request.photos = self.data_serializer.validated_data.pop('photos', False)
                # self.request.content_data = self.data_serializer.validated_data['video'] if created else None
            if pk is not None:
                self.filter_data['pk'] = pk
                self.func = 0
                self._filter = False

    def create(self, data):
        self.serializer_context['author'] = self.request.user.pk
        obj = self.data_serializer.create(self.data_serializer.validated_data)
        serializer = self.get_serializer(obj)
        return serializer.data, 201


class CRUDAPIView(CustomRetrieveAPIView, CustomUpdateAPIView, CustomDestoryAPIView, CustomCreateAPIView):
    pass
    # post = CustomCreateAPIView.post

# class CRUDAPIView(CustomRetrieveAPIView, CustomUpdateAPIView, CustomDestoryAPIView):
#     pass
#
