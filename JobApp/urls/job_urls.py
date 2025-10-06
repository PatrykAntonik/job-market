"""
This file contains the URL patterns for job-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.job_views import (
    ContractTypeListView,
    EmployerJobOfferListView,
    IndustryListView,
    JobOfferDetailView,
    JobOfferListProfileView,
    JobOfferListView,
    JobOfferProfileDetailView,
    RemotenessLevelListView,
    SeniorityListView,
    SkillListView,
)


urlpatterns = [
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path("industries/", IndustryListView.as_view(), name="industry-list"),
    path("seniority/", SeniorityListView.as_view(), name="seniority-list"),
    path("contract-types/", ContractTypeListView.as_view(), name="contract-type-list"),
    path(
        "remoteness-levels/",
        RemotenessLevelListView.as_view(),
        name="remoteness-level-list",
    ),
    path("<int:pk>/", JobOfferDetailView.as_view(), name="job-offer-detail"),
    path("profile/", JobOfferListProfileView.as_view(), name="job-offer-list-profile"),
    path(
        "profile/<int:pk>/",
        JobOfferProfileDetailView.as_view(),
        name="job-offer-profile-detail",
    ),
    path(
        "employer/<int:pk>/",
        EmployerJobOfferListView.as_view(),
        name="employer-job-offer-list",
    ),
    path("", JobOfferListView.as_view(), name="job-offer-list"),
]
