from django.core.management.base import BaseCommand

from JobApp.models import (
    Benefit,
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
    City,
    Country,
    Employer,
    EmployerLocation,
    Industry,
    JobOffer,
    JobOfferSkill,
    OfferResponse,
    Skill,
    User,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Clearing all data from the database...")
        OfferResponse.objects.all().delete()
        JobOfferSkill.objects.all().delete()
        JobOffer.objects.all().delete()
        EmployerLocation.objects.all().delete()
        CandidateEducation.objects.all().delete()
        CandidateExperience.objects.all().delete()
        CandidateSkill.objects.all().delete()
        Skill.objects.all().delete()
        Benefit.objects.all().delete()
        Employer.objects.all().delete()
        Industry.objects.all().delete()
        Candidate.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All data cleared successfully."))
