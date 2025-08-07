from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models
from phone_field import PhoneField

from .managers import CustomUserManager


class Country(models.Model):
    """
    :ivar name: The country associated with the candidate.
    :type name: CharField
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    :ivar name: City as CharField.
    :type name: CharField
    :ivar province: Province as CharField.
    :type province: CharField
    :ivar zip_code: Zip code as CharField.
    :type zip_code: CharField
    :ivar country : Country associated with a city.
    :type country: Country
    """

    name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user that extends the default Django AbstractUser with additional attributes.

    Is a base model for employer and candidate. Collects columns common for Candidate and Employer models.

    :ivar first_name: The first name of the user.
    :type first_name: str
    :ivar last_name: The last name of the user.
    :type last_name: str
    :ivar email: The email address of the user.
    :type email: str
    :ivar password: The hashed password of the user.
    :type password: str
    :ivar phone_number: The phone number of the user. Must be unique.
    :type phone_number: PhoneField
    :ivar city: The city where the user is located.
    :type city: ForeignKey
    """

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.email


class Candidate(models.Model):
    """
    Represents a Candidate entity.

    It extends the base user
    model via a one-to-one relationship.

    :ivar user: One-to-one relationship with the User model.
    :type user: User
    :ivar resume: File field for uploading the candidate's resume.
    :type resume: File
    :ivar about: Optional text field for additional information about the candidate.
    :type about: str or None
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Industry(models.Model):
    """
    Represents an Industry entity within the application.

    :ivar name: The unique name of the industry.
    :type name: CharField
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Employer(models.Model):
    """
    Represents an employer entity within the application.

    It extends the base user
    model via a one-to-one relationship.

    :ivar user: The user associated with the employer.
    :type user: models.OneToOneField
    :ivar company_name: The unique name of the employer's company.
    :type company_name: models.CharField
    :ivar website_url: The unique URL of the employer's website.
    :type website_url: models.URLField
    :ivar description: Optional text giving additional details about the
        employer or its operations.
    :type description: models.TextField
    :ivar industry: The industry to which the employer belongs.
    :type industry: models.ForeignKey
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, unique=True)
    website_url = models.URLField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    benefits = models.ManyToManyField("Benefit", blank=True)

    def __str__(self):
        return self.company_name + " - " + self.industry.name


class Benefit(models.Model):
    """
    Represents a benefit that can be offered by an employer.

    :ivar name: The unique name of the benefit.
    :type name: str
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Represents a skill in the system.

    :ivar name: The unique name of the skill.
    :type name: models.CharField
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CandidateSkill(models.Model):
    """
    Represents the association between a candidate and a skill.

    Each instance of CandidateSkill represents one skill associated with a candidate.

    :ivar candidate: The candidate associated with the skill.
    :type candidate: ForeignKey
    :ivar skill: The skill linked to the candidate.
    :type skill: ForeignKey
    """

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("candidate", "skill")

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} - {self.skill.name}"


class CandidateExperience(models.Model):
    """
    Represents the professional experience of a candidate.

    :ivar candidate: The candidate to whom this experience belongs.
    :type candidate: ForeignKey
    :ivar company_name: The name of the company where the candidate worked.
    :type company_name: CharField
    :ivar date_from: The starting date of the candidate's employment.
    :type date_from: DateField
    :ivar date_to: The ending date of the candidate's employment. Can be
        `None` if the candidate is currently employed.
    :type date_to: DateField
    :ivar is_current: Indicates whether the candidate is currently employed
        at this company.
    :type is_current: BooleanField
    :ivar job_position: The job title or position held by the candidate.
    :type job_position: CharField
    :ivar description: A description or additional details about the work
        experience. Can be left blank.
    :type description: TextField
    """

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    job_position = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} - {self.company_name}"


class CandidateEducation(models.Model):
    """
    Represents the educational details of a candidate.

    :ivar candidate: The candidate associated with this education record.
    :type candidate: ForeignKey
    :ivar school_name: The name of the educational institution attended by the candidate.
    :type school_name: CharField
    :ivar field_of_study: The area of study or specialization undertaken by the candidate.
    :type field_of_study: CharField
    :ivar degree: The degree or qualification obtained by the candidate.
    :type degree: CharField
    :ivar date_from: The starting date of the candidate's education.
    :type date_from: DateField
    :ivar date_to: The ending date of the candidate's education. Can be `None` if the candidate is currently enrolled.
    :type date_to: DateField
    :ivar is_current: Indicates whether the candidate is currently enrolled in this educational program.
    :type is_current: BooleanField
    """

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)


class EmployerLocation(models.Model):
    """
    Represents the location of an employer.

    :ivar employer: The employer this location is associated with.
    :type employer: Employer
    :ivar city: The city where the employer is located.
    :type city: City
    """

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employer.company_name} - {self.city}"


class JobOffer(models.Model):
    """
    Represents a job offer within the application.

    This model stores all relevant information about a job offer, including its
    description, location, and the required skills. It also defines several
    choices for fields like seniority, contract type, and remoteness level
    to ensure data consistency.

    :ivar employer: The employer who created the job offer.
    :type employer: ForeignKey
    :ivar description: A detailed description of the job offer.
    :type description: TextField
    :ivar location: The location where the job is based.
    :type location: ForeignKey
    :ivar remoteness: The level of remote work allowed (e.g., onsite, hybrid, remote).
    :type remoteness: CharField
    :ivar contract: The type of employment contract (e.g., full-time, part-time).
    :type contract: CharField
    :ivar seniority: The required seniority level for the position (e.g., junior, senior).
    :type seniority: CharField
    :ivar position: The title of the job position.
    :type position: CharField
    :ivar wage: The salary for the position.
    :type wage: IntegerField
    :ivar currency: The currency of the wage.
    :type currency: CharField
    :ivar skills: The skills required for the job.
    :type skills: ManyToManyField
    """

    class Seniority(models.TextChoices):
        """
        An enumeration of the available seniority levels for a job offer.
        """

        INTERN = "INTERN", "Intern"
        JUNIOR = "JUNIOR", "Junior"
        MID = "MID", "Mid"
        SENIOR = "SENIOR", "Senior"
        LEAD = "LEAD", "Lead"

    class ContractType(models.TextChoices):
        """
        An enumeration of the available contract types for a job offer.
        """

        EMPLOYMENT_CONTRACT = "employment_contract", "Employment contract"  # UoP
        MANDATE_CONTRACT = "mandate_contract", "Mandate contract"  # Umowa zlecenie
        B2B_CONTRACT = "b2b_contract", "B2B contract"  # Kontrakt B2B
        SPECIFIC_TASK_CONTRACT = (
            "specific_task_contract",
            "Specific task contract",
        )  # Umowa o dzieło
        INTERNSHIP_CONTRACT = "internship_contract", "Internship contract"

    class RemotenessLevel(models.TextChoices):
        """
        An enumeration of the available remoteness levels for a job offer.
        """

        ONSITE = "onsite", "Onsite"
        HYBRID = "hybrid", "Hybrid"
        REMOTE = "remote", "Remote"

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.ForeignKey(EmployerLocation, on_delete=models.CASCADE)
    remoteness = models.CharField(
        max_length=255,
        choices=RemotenessLevel.choices,
    )
    contract = models.CharField(
        max_length=255,
        choices=ContractType.choices,
    )
    seniority = models.CharField(
        max_length=255,
        choices=Seniority.choices,
    )
    position = models.CharField(max_length=255)
    wage = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, through="JobOfferSkill")

    def __str__(self):
        return self.employer.company_name + " - " + self.position


class JobOfferSkill(models.Model):
    """
    Represents the relationship between a job offer and a skill.
    This model serves as a bridge table to associate specific skills with
    a given job offer.

    :ivar offer: The job offer to which the skill is associated.
    :type offer: ForeignKey
    :ivar skill: The skill associated with the job offer.
    :type skill: ForeignKey
    """

    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.offer.employer.company_name} - {self.skill.name}"


class OfferResponse(models.Model):
    """
    Represents a response to a job offer by a candidate.

    :ivar offer: The job offer to which the candidate has responded.
    :type offer: ForeignKey to JobOffer
    :ivar candidate: The candidate who has responded to the job offer.
    :type candidate: ForeignKey to Candidate
    """

    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidate.user.first_name} {self.candidate.user.last_name} applied to {self.offer.employer.company_name} - {self.offer.description}"
