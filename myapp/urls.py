from django.urls import path
from .views import RUDVideoPostAPIView, RetrieveVideoPostAPIView, RUDPhotoPostAPIView, RetrievePhotoPostAPIView, RUDArticleAPIView, RetrieveArticleAPIView, CRUDCommentAPIView, RCommentAPIView, \
    CRUDSubCommentAPIView, RsubCommentAPIView, UpdatedCounts  # , StreamingFileView

urlpatterns = [
    path('video/', RUDVideoPostAPIView.as_view()),
    path('video/<int:pk>/', RetrieveVideoPostAPIView.as_view()),
    path('photo/', RUDPhotoPostAPIView.as_view()),
    path('photo/<int:pk>/', RetrievePhotoPostAPIView.as_view()),
    path('article/', RUDArticleAPIView.as_view()),
    path('article/<int:pk>/', RetrieveArticleAPIView.as_view()),
    path('comment/', CRUDCommentAPIView.as_view()),
    path('comment/<int:pk>/', RCommentAPIView.as_view()),
    path('sub_comment/', CRUDSubCommentAPIView.as_view()),
    path('sub_comment/<int:pk>/', RsubCommentAPIView.as_view()),
    path('count/', UpdatedCounts.as_view()),
    # path('stream_video/<int:pk>/', StreamingFileView.as_view())
]
#     path('update_video/', views.VideoUpdateVideo.as_view()),
#     path('destroy_video/', views.DestroyVideo.as_view()),
#
#     path('article/', views.ArticleAPIView.as_view()),
#     path('update_article/', views.ArticleUpdate.as_view()),
#     path('destroy_article/', views.ArticleDestroy.as_view()),
#
#     path('video_list/', views.VideoListView.as_view()),
#     path('article_list/', views.ArticleListView.as_view()),
#
#     path('video_count/', views.VideoUpdateVideo.as_view()),
#     path('article_count/', views.Article_count.as_view()),
#
#     path('TopVideo/', views.TopVideo.as_view()),
#     path('TopArticle/', views.TopArticle.as_view()),
#
#     # path('create_Video/', views.CReateAPIView.as_view()),
# ]
