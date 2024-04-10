from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
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
