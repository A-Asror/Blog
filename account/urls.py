from django.urls import path

from admin.views import CRAdminFacultyAPIView, CRAdminUniversityAPIView
from .views import RegistrationApiView, LoginAPIView, LogoutView, UsersAPIView, FriendsAPIView, EducationAPIView, RUsersAPIView  # RetrieveFriendsAPIView

urlpatterns = [
    path('register/', RegistrationApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('detail/', UsersAPIView.as_view()),
    path('detail/<int:pk>/', RUsersAPIView.as_view()),
    # path('friends/', RetrieveFriendsAPIView.as_view()),
    path('faculty/', CRAdminFacultyAPIView.as_view()),
    path('university/', CRAdminUniversityAPIView.as_view()),
    path('friends/', FriendsAPIView.as_view()),
    path('education/', EducationAPIView.as_view()),
]
