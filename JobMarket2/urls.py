"""
URL configuration for JobMarket2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from JobApp.views.test import health


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(), name="redoc"),
    # path("api/employers/", include("JobApp.urls.employer_urls")),
    path("api/candidates/", include("JobApp.urls.candidate_urls")),
    path("api/jobs/", include("JobApp.urls.job_urls")),
    path("api/users/", include("JobApp.urls.user_urls")),
    path("api/employers/", include("JobApp.urls.employer_urls")),
    path("", SpectacularSwaggerView.as_view(), name="docs"),
    path("health/", health, name="health"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
