from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField


class User(AbstractUser):
    phone_number = PhoneField(max_length=255, unique=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    is_employer = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="user",
    )

    # class Meta:
    #     permissions = [
    #         ("can_view_candidates", "Can view candidates"),
    #         ("can_view_employers", "Can view employers"),
    #         ("can_view_job_offers", "Can view job offers"),
    #         ("can_view_skills", "Can view skills"),
    #         ("can_view_contract_types", "Can view contract types"),
    #         ("can_view_remoteness_levels", "Can view remoteness levels"),
    #         ("can_view_candidate_experiences", "Can view candidate experiences"),
    #         ("can_view_offer_responses", "Can view offer responses"),
    #         ("can_view_employer_benefits", "Can view employer benefits"),
    #         ("can_view_employer_locations", "Can view employer locations"),
    #     ]

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.username


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField()
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Industry(models.Model):
    industry = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.industry


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, unique=True)
    website_url = models.URLField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name + " - " + self.industry.industry


class Skill(models.Model):
    skill = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.skill


class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} - {self.skill.skill}"


class ContractType(models.Model):
    contract_type = models.CharField(max_length=255)

    def __str__(self):
        return self.contract_type


class RemotenessLevel(models.Model):
    remote_type = models.CharField(max_length=255)

    def __str__(self):
        return self.remote_type


class Seniority(models.Model):
    seniority_level = models.CharField(max_length=255)

    def __str__(self):
        return self.seniority_level


class JobOffer(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    description = models.TextField()
    city = models.CharField(max_length=255)
    remoteness = models.ForeignKey(RemotenessLevel, on_delete=models.CASCADE)
    contract = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    seniority = models.ForeignKey(Seniority, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    wage = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, through='JobOfferSkill')

    def __str__(self):
        return self.employer.company_name + " - " + self.position


class JobOfferSkill(models.Model):
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.offer.employer.company_name} - {self.skill.skill}"


class CandidateExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    is_current = models.BooleanField()
    job_position = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} - {self.company_name}"


class OfferResponse(models.Model):
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} applied to {self.offer.employer.company_name} - {self.offer.description}"


class EmployerBenefit(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    benefit_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.employer.company_name} - {self.benefit_name}"


class EmployerLocation(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.employer.company_name} - {self.city}"
