"""
This file contains the URL patterns for employer-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.employer_views import (
    EmployerBenefitDetailView,
    EmployerBenefitListProfileView,
    EmployerDetailView,
    EmployerListBenefitView,
    EmployerListView,
    EmployerLocationDetailView,
    EmployerLocationListProfileView,
    EmployerLocationListView,
    EmployerProfileView,
    RegisterEmployerView,
)


urlpatterns = [
    path("register/", RegisterEmployerView.as_view(), name="register-employer"),
    path(
        "profile/locations/<int:pk>/",
        EmployerLocationDetailView.as_view(),
        name="employer-profile-location-detail",
    ),
    path(
        "profile/locations/",
        EmployerLocationListProfileView.as_view(),
        name="employer-profile-locations",
    ),
    path(
        "profile/benefits/<int:pk>/",
        EmployerBenefitDetailView.as_view(),
        name="employer-profile-benefit-detail",
    ),
    path(
        "profile/benefits/",
        EmployerBenefitListProfileView.as_view(),
        name="employer-profile-benefits",
    ),
    path("profile/", EmployerProfileView.as_view(), name="employer-profile"),
    path(
        "<int:pk>/benefits/",
        EmployerListBenefitView.as_view(),
        name="employer-benefits",
    ),
    path("<int:pk>/locations/", EmployerLocationListView.as_view(), name="locations"),
    path("<int:pk>/", EmployerDetailView.as_view(), name="employer"),
    path("", EmployerListView.as_view(), name="employers"),
]
