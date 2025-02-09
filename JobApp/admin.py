from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_candidate', 'is_employer')
    list_filter = ('is_superuser', 'groups')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_candidate', 'is_employer', 'first_name', 'last_name',
                'phone_number', 'city')}
         ),
    )

    fieldsets = (
        (None, {
            'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(Skill)
admin.site.register(CandidateSkill)
admin.site.register(ContractType)
admin.site.register(RemotenessLevel)
admin.site.register(JobOffer)
admin.site.register(JobOfferSkill)
admin.site.register(CandidateExperience)
admin.site.register(OfferResponse)
admin.site.register(EmployerBenefit)
admin.site.register(EmployerLocation)
admin.site.register(Industry)
admin.site.register(Seniority)
admin.site.register(CandidateEducation)
