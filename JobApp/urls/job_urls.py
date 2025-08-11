# """
# This file contains the URL patterns for job-related views in the JobApp application.
# """
#
# from django.urls import path
#
# from JobApp.views.job_views import (
#     getContractTypes,
#     getEmployerJobOffers,
#     getJobOffer,
#     getJobOffers,
#     getRemotenessLevels,
#     getSeniority,
#     getSkills,
# )
#
#
# urlpatterns = [
#     path("contract_types/", getContractTypes, name="contract_types"),
#     path("skills/", getSkills, name="skills"),
#     path("remoteness_levels/", getRemotenessLevels, name="remoteness_levels"),
#     path("seniority/", getSeniority, name="seniority"),
#     path("employer/<int:pk>/", getEmployerJobOffers, name="employer_job_offers"),
#     path("<int:pk>/", getJobOffer, name="job_offer"),
#     path("", getJobOffers, name="job_offers"),
# ]
