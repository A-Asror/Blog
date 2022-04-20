from django.urls import path
from .views import AdminUsersAPIView, CRAdminUniversityAPIView, RUDAdminUniversityAPIView, CRAdminFacultyAPIView, RUDAdminFacultyAPIView, EducationAPIView, CRAdminCategoryAPIView, RUDAdminCategoryAPIView, \
    RUDAdminVideoPostAPIView, RUDAdminArticleAPIView


urlpatterns = [
    # path('detail/', UsersAPIView.as_view()),
    path('detail/<int:pk>/', AdminUsersAPIView.as_view()),
    path('university/', CRAdminUniversityAPIView.as_view()),
    path('university/<int:pk>/', RUDAdminUniversityAPIView.as_view()),
    path('faculty/', CRAdminFacultyAPIView.as_view()),
    path('faculty/<int:pk>/', RUDAdminFacultyAPIView.as_view()),
    # # path('friends/', RetrieveFriendsAPIView.as_view()),
    # path('friends/', FriendsAPIView.as_view()),
    path('education/', EducationAPIView.as_view()),
    path('video/', RUDAdminVideoPostAPIView.as_view()),
    path('article/', RUDAdminArticleAPIView.as_view()),
    path('category/', CRAdminCategoryAPIView.as_view()),
    path('category/<int:pk>/', RUDAdminCategoryAPIView.as_view()),
]
