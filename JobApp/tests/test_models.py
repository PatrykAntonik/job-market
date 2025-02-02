import pytest
import datetime
from django.conf import settings
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from JobApp.models import *


@pytest.mark.django_db
def test_user_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        first_name='Test',
        last_name='User',
        phone_number='1234567890',
        zip_code='12345',
        city='Test',
        country='Test',
        province='Test',
        is_candidate=True
    )
    assert user.username == 'testuser', f"Expected user.username to be 'testuser', but got '{user.username}'"
    assert user.email == 'test@gmail.com', f"Expected user.email to be 'test@gmail.com', but got '{user.email}'"
    assert user.first_name == 'Test', f"Expected user.first_name to be 'Test', but got '{user.first_name}'"
    assert user.last_name == 'User', f"Expected user.last_name to be 'User', but got '{user.last_name}'"
    assert user.phone_number == '1234567890', f"Expected user.phone_number to be '1234567890', but got '{user.phone_number}'"
    assert user.zip_code == '12345', f"Expected user.zip_code to be '12345', but got '{user.zip_code}'"
    assert user.city == 'Test', f"Expected user.city to be 'Test', but got '{user.city}'"
    assert user.country == 'Test', f"Expected user.country to be 'Test', but got '{user.country}'"
    assert user.province == 'Test', f"Expected user.province to be 'Test', but got '{user.province}'"
    assert user.is_candidate is True, f"Expected user.is_candidate to be True, but got {user.is_candidate}"
    assert str(user) == "Test User", f"Expected str(user) to be 'Test User', but got '{str(user)}'"

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username='duplicateuser',
            email='duplicate@gmail.com',
            password='<PASSWORD>',
            first_name='Duplicate',
            last_name='User',
            phone_number=user.phone_number,
            is_candidate=True
        )

    incomplete_user = User(username='', phone_number='')
    with pytest.raises(ValidationError) as excinfo:
        incomplete_user.full_clean()
    assert 'username' in excinfo.value.message_dict
    assert 'phone_number' in excinfo.value.message_dict


@pytest.mark.django_db
def test_candidate_model(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    resume_file = SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    candidate = Candidate.objects.create(
        user=user,
        resume=resume_file,
        about="about me"
    )
    assert candidate.user == user, f"Expected candidate.user to be {user}, but got {candidate.user}"
    assert candidate.resume is not None, "Expected candidate.resume to be a file, but got None"
    assert candidate.resume.size > 0, f"Expected candidate.resume to have size > 0, but got {candidate.resume.size}"
    assert candidate.about == "about me", f"Expected candidate.about to be 'about me', but got '{candidate.about}'"

    incomplete_candidate = Candidate(user=user, resume=None)
    with pytest.raises(ValidationError) as excinfo:
        incomplete_candidate.full_clean()
    assert 'resume' in excinfo.value.message_dict, "Expected 'resume' to be in excinfo.value.message_dict"


@pytest.mark.django_db
def test_industry_model():
    industry = Industry.objects.create(
        name='Test Industry',
    )
    assert industry.name == "Test Industry", f"Expected industry.name to be 'Test Industry', but got '{industry.name}'"

    incomplete_industry = Industry(name='')
    with pytest.raises(ValidationError) as excinfo:
        incomplete_industry.full_clean()
    assert 'name' in excinfo.value.message_dict, "Expected 'industry' to be in excinfo.value.message_dict"


@pytest.mark.django_db
def test_employer_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    industry = Industry.objects.create(
        name='Test Industry',
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )

    assert employer.user == user, f"Expected employer.user to be {user}, but got {employer.user}"
    assert employer.company_name == 'Test Employer', f"Expected employer.company_name to be 'Test Emplopery', but got '{employer.company_name}'"
    assert employer.website_url == 'www.test.com', f"Expected employer.website to be 'www.test.com', but got {employer.website_url}"
    assert employer.description == 'Test employer', f"Expected employer.description to be 'Test employer', but got {employer.description}"
    assert employer.industry == industry, f"Expected employer.industry to be {industry}, but got {employer.industry}"

    incomplete_employer = Employer(user=user, company_name='', website_url='', description='', industry=industry)
    with pytest.raises(ValidationError) as excinfo:
        incomplete_employer.full_clean()
    assert incomplete_employer.company_name == '', f"Expected incomplete_employer.company_name to be '', but got {incomplete_employer.company_name}"
    assert incomplete_employer.website_url == '', f"Expected incomplete_employer.website_url to be '', but got {incomplete_employer.website_url}"
    assert incomplete_employer.description == '', f"Expected incomplete_employer.description to be '', but got {incomplete_employer.description}"

    with pytest.raises(IntegrityError):
        Employer.objects.create(
            user=user,
            company_name=employer.company_name,
            website_url='www.test.com',
            description='Test employer',
            industry=industry
        )


@pytest.mark.django_db
def test_skill_model():
    skill = Skill.objects.create(
        name='Test Skill',
    )
    assert skill.name == "Test Skill", f"Expected skill.name to be 'Test Skill', but got '{skill.name}'"

    incomplete_skill = Skill(name='')
    with pytest.raises(ValidationError) as excinfo:
        incomplete_skill.full_clean()
    assert 'name' in excinfo.value.message_dict, "Expected 'skill' to be in excinfo.value.message_dict"


@pytest.mark.django_db
def test_candidate_skill_model(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    candidate = Candidate.objects.create(
        user=user,
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf"),
        about="about me"
    )
    skill = Skill.objects.create(
        name="Test skill"
    )
    skill_candidate = CandidateSkill.objects.create(
        skill=skill,
        candidate=candidate
    )
    assert skill_candidate.skill == skill, f'Expected skill to be {skill}, but got {skill_candidate.skill}'
    assert skill_candidate.candidate == candidate, f'Expected candidate to be {candidate}, but got {skill_candidate.candidate}'

    incomplete_candidate_skill = CandidateSkill(candidate=None, skill=None)
    with pytest.raises(ValidationError) as excinfo:
        incomplete_candidate_skill.full_clean()
    assert 'candidate' in excinfo.value.message_dict
    assert 'skill' in excinfo.value.message_dict


@pytest.mark.django_db
def test_contract_type_model():
    contract_type = ContractType.objects.create(
        contract_type='Test type'
    )
    assert contract_type.contract_type == 'Test type', f"Expected contract_type to be 'Test type', but got {contract_type.contract_type}"


@pytest.mark.django_db
def test_remoteness_type_model():
    remoteness_type = RemotenessLevel.objects.create(
        remote_type='Test type'
    )
    assert remoteness_type.remote_type == 'Test type', f"Expected remoteness_type to be 'Test type', but got {remoteness_type.remote_type}"


@pytest.mark.django_db
def test_senority_level_model():
    senority_level = Seniority.objects.create(
        seniority_level='Test level'
    )
    assert senority_level.seniority_level == 'Test level', f"Expected seniority_level to be 'Test level', but got {seniority_level.seniority_level}"


@pytest.mark.django_db
def test_job_offer_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=Industry.objects.create(name='Test industry')
    )
    country = Country.objects.create(
        name='Test Country',
    )

    city = City.objects.create(
        name='Test City',
        country=country,
    )

    location = EmployerLocation.objects.create(
        employer=employer,
        city=city,
    )
    remoteness = RemotenessLevel.objects.create(remote_type='Test type')
    contract = ContractType.objects.create(contract_type='Test type')
    seniority = Seniority.objects.create(seniority_level='Test level')

    job_offer = JobOffer.objects.create(
        employer=employer,
        location=location,
        description='Test description',
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='Test position',
        wage=5000,
        currency='$'
    )

    assert job_offer.employer == employer, f"Expected job_offer.employer to be {employer}, but got {job_offer.employer}"
    assert job_offer.description == 'Test description', f"Expected job_offer.description to be 'Test description', but got {job_offer.description}"
    assert job_offer.location == location, f"Expected job_offer.location to be {location}, but got {job_offer.location}"
    assert job_offer.remoteness == remoteness, f"Expected job_offer.remoteness to be {remoteness}, but got {job_offer.remoteness}"
    assert job_offer.contract == contract, f"Expected job_offer.contract to be {contract}, but got {job_offer.contract}"
    assert job_offer.seniority == seniority, f"Expected job_offer.seniority to be {seniority}, but got {job_offer.seniority}"
    assert job_offer.position == 'Test position', f"Expected job_offer.position to be 'Test position', but got {job_offer.position}"
    assert job_offer.wage == 5000, f"Expected job_offer.wage to be 5000, but got {job_offer.wage}"
    assert job_offer.currency == '$', f"Expected job_offer.currency to be '$', but got {job_offer.currency}"


@pytest.mark.django_db
def test_job_offer_skill_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=Industry.objects.create(name='Test industry')
    )
    country = Country.objects.create(
        name='Test Country',
    )

    city = City.objects.create(
        name='Test City',
        country=country,
    )

    location = EmployerLocation.objects.create(
        employer=employer,
        city=city,
    )

    remoteness = RemotenessLevel.objects.create(remote_type='Test type')
    contract = ContractType.objects.create(contract_type='Test type')
    seniority = Seniority.objects.create(seniority_level='Test level')

    job_offer = JobOffer.objects.create(
        employer=employer,
        location=location,
        description='Test description',
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='Test position',
        wage=5000,
        currency='$'
    )

    skill1 = Skill.objects.create(name='Python')
    job_offer.skills.add(skill1)
    assert job_offer.skills.count() == 1, f"Expected 1 skill, got {job_offer.skills.count()}"
    assert skill1 in job_offer.skills.all(), "Expected 'Python' skill to be associated with the job offer"
    assert JobOfferSkill.objects.filter(offer=job_offer,
                                        skill=skill1).exists(), "Expected a JobOfferSkill entry for skill1"


@pytest.mark.django_db
def test_job_offer_candidate_experience_model(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    candidate = Candidate.objects.create(
        user=user,
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf"),
        about="about me"
    )
    candidate_experience = CandidateExperience.objects.create(
        candidate=candidate,
        company_name='Test company',
        date_from=datetime.date(2023, 1, 1),
        date_to=datetime.date(2023, 1, 31),
        is_current=False,
        job_position='Test position',
        description='Test description',
    )
    assert candidate_experience.candidate == candidate, f"Expected candidate_experience.candidate to be {candidate}, but got {candidate_experience.candidate}"
    assert candidate_experience.company_name == 'Test company', f"Expected candidate_experience.company_name to be 'Test company', but got {candidate_experience.company_name}"
    assert candidate_experience.date_from == datetime.date(2023, 1,
                                                           1), f"Expected candidate_experience.date_from to be {datetime.date(2023, 1, 1)}, but got {candidate_experience.date_from}"
    assert candidate_experience.date_to == datetime.date(2023, 1,
                                                         31), f"Expected candidate_experience.date_to to be {datetime.date(2023, 1, 31)}, but got {candidate_experience.date_to}"
    assert candidate_experience.is_current is False, f"Expected candidate_experience.is_current to be False, but got {candidate_experience.is_current}"
    assert candidate_experience.job_position == 'Test position', f"Expected candidate_experience.job_position to be 'Test position', but got {candidate_experience.job_position}"
    assert candidate_experience.description == 'Test description', f"Expected candidate_experience.description to be 'Test description', but got {candidate_experience.description}"


@pytest.mark.django_db
def test_job_offer_candidate_education_model(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    candidate = Candidate.objects.create(
        user=user,
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf"),
        about="about me"
    )
    candidate_education = CandidateEducation.objects.create(
        candidate=candidate,
        school_name='Test school',
        field_of_study='Test field of study',
        degree='Test degree',
    )
    assert candidate_education.candidate == candidate, f"Expected candidate_education.candidate to be {candidate}, but got {candidate_education.candidate}"
    assert candidate_education.school_name == 'Test school', f"Expected candidate_education.school_name to be 'Test school', but got {candidate_education.school_name}"
    assert candidate_education.field_of_study == 'Test field of study', f"Expected candidate_education.field_of_study to be 'Test field of study', but got {candidate_education.field_of_study}"
    assert candidate_education.degree == 'Test degree', f"Expected candidate_education.degree to be 'Test degree', but got {candidate_education.degree}"


@pytest.mark.django_db
def test_offer_response_model(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=Industry.objects.create(name='Test industry')
    )
    country = Country.objects.create(
        name='Test Country',
    )

    city = City.objects.create(
        name='Test City',
        country=country,
    )

    location = EmployerLocation.objects.create(
        employer=employer,
        city=city,
    )

    remoteness = RemotenessLevel.objects.create(remote_type='Test type')
    contract = ContractType.objects.create(contract_type='Test type')
    seniority = Seniority.objects.create(seniority_level='Test level')

    job_offer = JobOffer.objects.create(
        employer=employer,
        location=location,
        description='Test description',
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='Test position',
        wage=5000,
        currency='$'
    )
    candidate = Candidate.objects.create(
        user=user,
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf"),
        about="about me"
    )
    offer_response = OfferResponse.objects.create(
        offer=job_offer,
        candidate=candidate,
    )


@pytest.mark.django_db
def test_employer_benefit_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    industry = Industry.objects.create(
        name='Test Industry',
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )
    benefit = EmployerBenefit.objects.create(
        employer=employer,
        benefit_name='Test Benefit',
    )
    assert benefit.employer == employer, f"Expected benefit.employer to be {employer}, but got {benefit.employer}"
    assert benefit.benefit_name == 'Test Benefit', f"Expected benefit.benefit to be 'Test Benefit', but got {benefit.benefit}"


@pytest.mark.django_db
def test_employer_location_model():
    user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890'
    )
    industry = Industry.objects.create(
        name='Test Industry',
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )

    country = Country.objects.create(
        name='Test Country',
    )

    city = City.objects.create(
        name='Test City',
        country=country,
    )

    location = EmployerLocation.objects.create(
        employer=employer,
        city=city,
    )
