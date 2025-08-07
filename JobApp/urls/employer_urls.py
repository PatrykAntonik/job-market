from django.urls import path

from JobApp.views.employer_views import *

urlpatterns = [
    path("countries/", getCountries, name="countries"),
    path("cities/", getCities, name="cities"),
    path("industries/", getIndustries, name="industries"),
    path("industries/<str:pk>/", getIndustry, name="industry"),
    path("<str:pk>/locations/", getEmployerLocation, name="employer_location"),
    path("<str:pk>/", getEmployer, name="employer"),
    path("", getEmployers, name="employers"),
]
