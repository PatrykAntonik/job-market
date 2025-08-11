from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class CustomUserAdmin(UserAdmin):
    """Custom admin interface for the User model."""

    model = User
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Candidate)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Employer)
admin.site.register(Skill)
admin.site.register(CandidateSkill)
admin.site.register(JobOffer)
admin.site.register(JobOfferSkill)
admin.site.register(CandidateExperience)
admin.site.register(OfferResponse)
admin.site.register(EmployerLocation)
admin.site.register(Industry)
admin.site.register(CandidateEducation)
admin.site.register(Benefit)
