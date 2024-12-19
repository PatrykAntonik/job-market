from django.urls import path
from JobApp.views.candidate_views import *

urlpatterns = [
    path('<int:pk>/skills/', getCandidateSkills, name="candidate_skills"),
    path('<int:pk>/experience/', getCandidateExperience, name="candidate_experience"),
    path('<int:pk>/experience/', getCandidateEducation, name="candidate_education"),
    path('<int:pk>/', getCandidate, name="candidate"),
    path('', getCandidates, name="candidates"),
]
