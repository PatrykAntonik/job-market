"""
This file contains the URL patterns for candidate-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.candidate_views import (
    CandidateDetailView,
    CandidateEducationListView,
    CandidateExperienceListView,
    CandidateListView,
    CandidateProfileView,
    CandidateSkillListView,
    RegisterCandidateView,
)


urlpatterns = [
    path("<int:pk>/skills/", CandidateSkillListView.as_view(), name="candidate_skills"),
    path(
        "<int:pk>/experience/",
        CandidateExperienceListView.as_view(),
        name="candidate_experience",
    ),
    path(
        "<int:pk>/education/",
        CandidateEducationListView.as_view(),
        name="candidate_education",
    ),
    path("register/", RegisterCandidateView.as_view(), name="register"),
    path("profile/", CandidateProfileView.as_view(), name="profile"),
    path("<int:pk>/", CandidateDetailView.as_view(), name="candidate"),
    path("", CandidateListView.as_view(), name="candidates"),
]
