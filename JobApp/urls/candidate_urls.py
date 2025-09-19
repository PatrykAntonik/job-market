"""
This file contains the URL patterns for candidate-related views in the JobApp application.
"""

from django.urls import path

from JobApp.views.candidate_views import (
    CandidateDetailView,
    CandidateEducationDetailView,
    CandidateEducationListView,
    CandidateEducationProfileView,
    CandidateExperienceDetailView,
    CandidateExperienceListView,
    CandidateExperienceProfileView,
    CandidateListView,
    CandidateProfileView,
    CandidateSkillDetailView,
    CandidateSkillListView,
    CandidateSkillProfileView,
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
    path(
        "profile/skills/<int:pk>",
        CandidateSkillDetailView.as_view(),
        name="skill-detail",
    ),
    path("profile/skills/", CandidateSkillProfileView.as_view(), name="skill-profile"),
    path(
        "profile/education/<int:pk>",
        CandidateEducationDetailView.as_view(),
        name="education-detail",
    ),
    path(
        "profile/education/",
        CandidateEducationProfileView.as_view(),
        name="education-profile",
    ),
    path(
        "profile/experience/<int:pk>",
        CandidateExperienceDetailView.as_view(),
        name="experience-detail",
    ),
    path(
        "profile/experience/",
        CandidateExperienceProfileView.as_view(),
        name="experience-profile",
    ),
    path("profile/", CandidateProfileView.as_view(), name="profile"),
    path("<int:pk>/", CandidateDetailView.as_view(), name="candidate"),
    path("", CandidateListView.as_view(), name="candidates"),
]
