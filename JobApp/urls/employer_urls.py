from django.urls import path
from JobApp.views.employer_views import *

urlpatterns = [
    path('industries/', getIndustries, name="industries"),
    path('<str:pk>/industries/', getIndustry, name="industry"),
    path('benefits/', getBenefit, name="employer_benefit"),
    path('<str:pk>/benefits/', getEmployerBenefit, name="employer_benefit"),
    path('<str:pk>/locations/', getEmployerLocation, name="employer_location"),
    path('<str:pk>/', getEmployer, name="employer"),
    path('', getEmployers, name="employers"),
]
