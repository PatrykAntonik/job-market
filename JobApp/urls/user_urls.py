"""
This file contains the URL patterns for user-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.user_views import (
    CityDetailView,
    CityListView,
    CountryDetailView,
    CountryListView,
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
    path("cities/<int:pk>/", CityDetailView.as_view(), name="city"),
    path("cities/", CityListView.as_view(), name="cities"),
    path("countries/<int:pk>/", CountryDetailView.as_view(), name="country"),
    path("countries/", CountryListView.as_view(), name="countries"),
    path("<int:pk>/", UserDetailView.as_view(), name="user"),
    path("", UserListView.as_view(), name="users"),
]
