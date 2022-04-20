import os

from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from base.views.custom_generics import AdminRUDAPIView, CRAPIView, CRUDObjectApiView, CustomRetrieveAPIView
from .models import Category, VideoPost, PhotoPost, Article, Photos, Comments, SubComments
from .serializers import CategorySerializer, VideoPostSerialize, PhotoPostSerialize, ArticleSerialize, PhotosSerialize, CommentsSerialize, SubCommentsSerialize, MetaDataSerializer
from utils.permissions import IsManagerUser, CheckObjectUserInUser, IsAuthenticatedCustom
from rest_framework import exceptions


class RUDVideoPostAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = VideoPostSerialize
    queryset = VideoPost  # class RUD CR APIView
    video = True


class RetrieveVideoPostAPIView(CustomRetrieveAPIView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = VideoPostSerialize
    queryset = VideoPost  # class RUD CR APIView


class RUDPhotoPostAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = PhotoPostSerialize
    queryset = PhotoPost  # class RUD CR APIView
    photo = True


class RetrievePhotoPostAPIView(CustomRetrieveAPIView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = PhotoPostSerialize
    queryset = PhotoPost  # class RUD CR APIView


class RUDArticleAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = ArticleSerialize
    queryset = Article  # class RUD CR APIView
    article = True

    def post(self, request, *args, **kwargs):
        data = super(RUDArticleAPIView, self).post(request, *args, **kwargs)
        pk = data.data.get('id', None)
        if pk:
            # print(self.request.FILES.get('photo', False))
            list_data = []
            # photos = PhotosSerialize(data=request.data, context=self.validation_context_and_filter, many=True)
            # photos.is_valid(raise_exception=True)
            # urls = photos.validated_data
            [list_data.append(Photos(article_id=pk, photo=photo)) for photo in self.request.photos]
            Photos.objects.bulk_create(list_data)
            return data
        return Response('error, saved Articl and not saved photos', status=400)


class RetrieveArticleAPIView(CustomRetrieveAPIView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = ArticleSerialize
    queryset = Article  # class RUD CR APIView


class CRUDCommentAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = CommentsSerialize
    queryset = Comments
    comment = True


class RCommentAPIView(CustomRetrieveAPIView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = CommentsSerialize
    queryset = Comments

    def updating_query_params(self):
        key_list = ['video_post_id', 'photo_post_id', 'article_post_id']
        query_params = self.request.query_params.keys()
        if len(query_params) > 1:
            raise exceptions.ValidationError("error query params.")
        for key in key_list:
            value_kwargs = self.request.query_params.get(key, None)
            if value_kwargs is not None and type(value_kwargs) == str:
                self.filter_data = {key: int(value_kwargs)}
                self.kwargs = {}
                break

    def get(self, request, *args, **kwargs):
        self.updating_query_params()
        self.custom(request)
        data, status_code = self.retrieve_or_all
        return self.check_refresh([data, status_code])


class CRUDSubCommentAPIView(CRUDObjectApiView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = SubCommentsSerialize
    queryset = SubComments
    sub_comment = True


class RsubCommentAPIView(CustomRetrieveAPIView):
    permission_classes = [CheckObjectUserInUser]
    serializer_class = SubCommentsSerialize
    queryset = SubComments  # class RUD CR APIView
    customize = True

    def dict_func(self):
        self.custom_funcs = [self.update_context]

    def update_filter(self):
        self.serializer_context['sub_class'] = False


class UpdatedCounts(APIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = MetaDataSerializer

    def patch(self, request, *args, **kwargs):
        list_data_keys = ['id_video', 'id_photo', 'id_article', 'id_sub_comment', 'id_comment']
        list_data = {'id_video': VideoPost, 'id_photo': PhotoPost, 'id_article': Article, 'id_sub_comment': SubComments, 'id_comment': Comments}
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.data
        keys = ['views', 'likes', 'dislikes']
        update_data = {'views': 0, 'likes': 0, 'dislikes': 0}
        pk = None
        model = None
        for key in data.keys():
            upd_data = data.get(key, False)
            if upd_data and key in keys:
                update_data[key] = 1
            if key in list_data_keys:
                model = list_data.get(key)
                pk = data.get(key, None)
        obj = model.objects.filter(pk=pk)
        if obj.exists():
            obj = obj.get()
            obj.views += update_data['views']
            obj.likes += update_data['likes']
            obj.dislikes += update_data['dislikes']
            obj.save()
            return Response('success', 200)
        return Response('not updated data', 400)


# class StreamingFileView(APIView):
#     dict_data = {'article': Article, 'video': VideoPost}
#     pk = None
#     model = None
#
#     def set_play(self, obj):
#         print(obj)
#         print(obj.plays_count)
#         obj.plays_count += 1
#         obj.save()
#
#     def filter_model(self):
#         for key in self.dict_data:
#             self.pk = self.request.query_params.get(key, None)
#             if self.pk is not None:
#                 self.model = self.dict_data.get(key)
#                 break
#         if self.pk is None:
#             raise exceptions.ValidationError('query_params not valid')
#
#     def get(self, request, *args, **kwargs):
#         self.filter_model()
#         pk = self.kwargs.get('pk', None)
#         if pk is None:
#             raise exceptions.ValidationError('query_params not valid')
#         obj = get_object_or_404(self.model, id=pk)
#         if os.path.exists(obj.video.path):
#             self.set_play(obj)
#             return FileResponse(open(obj.video.path, 'rb'), filename=obj.video.name)
#         raise exceptions.ValidationError('query_params not valid')
