"""
This file contains the URL patterns for user-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.user_views import (
    MyTokenObtainPairView,
    UpdateUserPasswordView,
    UserDetailView,
    UserListView,
    UserProfileView,
    UserRegistrationView,
)


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    # path('profile/update/', updateUserProfile, name='profile-update'),
    path(
        "profile/password/",
        UpdateUserPasswordView.as_view(),
        name="user-update-password",
    ),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("<int:pk>/", UserDetailView.as_view(), name="user"),
    path("", UserListView.as_view(), name="users"),
]
