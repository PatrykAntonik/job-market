from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from JobApp.models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
    City,
    Country,
    Employer,
    Industry,
    Skill,
    User,
)


# TODO- Clean tests, create fixtures for repeated code


@pytest.mark.django_db
def test_get_candidates_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)
    user1 = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    user2 = User.objects.create_user(
        email="test2@gmail.com",
        password="<PASSWORD>",
        phone_number="012345678900",
        city=city,
    )
    candidate1 = Candidate.objects.create(
        user=user1,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    candidate2 = Candidate.objects.create(
        user=user2,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    response = client.get("/api/candidates/")
    expected_data = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": candidate1.id,
                "user": {
                    "id": user1.id,
                    "first_name": user1.first_name,
                    "last_name": user1.last_name,
                    "email": user1.email,
                    "city": user1.city.id,
                    "phone_number": user1.phone_number,
                },
                "resume": f"http://testserver/media/{candidate1.resume.name}",
                "about": "about candidate",
                "total_experience": 0.0,
            },
            {
                "id": candidate2.id,
                "user": {
                    "id": user2.id,
                    "first_name": user2.first_name,
                    "last_name": user2.last_name,
                    "email": user2.email,
                    "city": user2.city.id,
                    "phone_number": user2.phone_number,
                },
                "resume": f"http://testserver/media/{candidate2.resume.name}",
                "about": "about candidate",
                "total_experience": 0.0,
            },
        ],
    }

    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidates_without_permission():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    client.force_authenticate(user=user)
    response = client.get(f"/api/candidates/")
    expected_data = {"detail": "Access restricted to employers only"}
    assert (
        response.status_code == HTTP_403_FORBIDDEN
    ), f"Expected status code 403 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    reponse = client.get(f"/api/candidates/{candidate.id}/")
    expected_data = {
        "id": candidate.id,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "city": user.city.id,
            "phone_number": user.phone_number,
        },
        "resume": f"http://testserver/media/{candidate.resume.name}",
        "about": "about candidate",
        "total_experience": 0.0,
    }
    assert (
        reponse.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {reponse.status_code}"
    assert (
        reponse.json() == expected_data
    ), f"Expected: {expected_data}, but got: {reponse.json()}"


@pytest.mark.django_db
def test_get_candidate_not_found():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)
    response = client.get("/api/candidates/1/")
    expected_data = {"detail": "No Candidate matches the given query."}
    assert (
        response.status_code == HTTP_404_NOT_FOUND
    ), f"Expected status code 404 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_without_permission():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    response = client.get(f"/api/candidates/{candidate.id}/")
    expected_data = {"detail": "Access restricted to employers only"}
    assert (
        response.status_code == HTTP_403_FORBIDDEN
    ), f"Expected status code 403 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_skills_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    skill = Skill.objects.create(
        name="Test Skill",
    )
    skill2 = Skill.objects.create(
        name="Test Skill2",
    )
    candidate_skill = CandidateSkill.objects.create(
        candidate=candidate,
        skill=skill,
    )
    candidate_skill2 = CandidateSkill.objects.create(
        candidate=candidate,
        skill=skill2,
    )
    response = client.get(f"/api/candidates/{candidate.id}/skills/")
    expected_data = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": candidate_skill.id,
                "skill": {"id": skill.id, "name": "Test Skill"},
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": city.id,
                        "phone_number": user.phone_number,
                    },
                },
            },
            {
                "id": candidate_skill2.id,
                "skill": {"id": skill2.id, "name": "Test Skill2"},
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": city.id,
                        "phone_number": user.phone_number,
                    },
                },
            },
        ],
    }
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_skills_not_found():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    response = client.get(f"/api/candidates/{candidate.id}/skills/")
    expected_data = {"count": 0, "next": None, "previous": None, "results": []}
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_skills_without_permission():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    response = client.get(f"/api/candidates/{candidate.id}/skills/")
    expected_data = {"detail": "Access restricted to employers only"}
    assert (
        response.status_code == HTTP_403_FORBIDDEN
    ), f"Expected status code 403 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_experience_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    experience = CandidateExperience.objects.create(
        candidate=candidate,
        company_name="Test Company",
        date_from="2021-01-01",
        date_to="2022-01-01",
        is_current=False,
        job_position="Test Position",
        description="Test Description",
    )
    experience2 = CandidateExperience.objects.create(
        candidate=candidate,
        company_name="Test Company2",
        date_from="2021-01-01",
        date_to="2022-01-01",
        is_current=False,
        job_position="Test Position2",
        description="Test Description2",
    )
    response = client.get(f"/api/candidates/{candidate.id}/experience/")
    expected_data = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": experience.id,
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": user.city.id,
                        "phone_number": user.phone_number,
                    },
                },
                "company_name": experience.company_name,
                "date_from": experience.date_from,
                "date_to": experience.date_to,
                "is_current": experience.is_current,
                "job_position": experience.job_position,
                "description": experience.description,
            },
            {
                "id": experience2.id,
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": user.city.id,
                        "phone_number": user.phone_number,
                    },
                },
                "company_name": experience2.company_name,
                "date_from": experience2.date_from,
                "date_to": experience2.date_to,
                "is_current": experience2.is_current,
                "job_position": experience2.job_position,
                "description": experience2.description,
            },
        ],
    }
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_experience_not_found():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    response = client.get(f"/api/candidates/{candidate.id}/experience/")
    expected_data = {"count": 0, "next": None, "previous": None, "results": []}
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_experience_without_permission():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    response = client.get(f"/api/candidates/{candidate.id}/experience/")
    expected_data = {"detail": "Access restricted to employers only"}
    assert (
        response.status_code == HTTP_403_FORBIDDEN
    ), f"Expected status code 403 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_education_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    education = CandidateEducation.objects.create(
        candidate=candidate,
        school_name="Test School",
        degree="Test Degree",
        field_of_study="Test Field",
        date_from="2021-01-01",
        date_to="2022-01-01",
        is_current=False,
    )
    education2 = CandidateEducation.objects.create(
        candidate=candidate,
        school_name="Test School2",
        degree="Test Degree",
        field_of_study="Test Field",
        date_from="2021-01-01",
        date_to="2022-01-01",
        is_current=False,
    )
    response = client.get(f"/api/candidates/{candidate.id}/education/")
    expected_data = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": education.id,
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": user.city.id,
                        "phone_number": user.phone_number,
                    },
                },
                "school_name": education.school_name,
                "degree": education.degree,
                "field_of_study": education.field_of_study,
                "date_from": education.date_from,
                "date_to": education.date_to,
                "is_current": education.is_current,
            },
            {
                "id": education2.id,
                "candidate": {
                    "id": candidate.id,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "city": user.city.id,
                        "phone_number": user.phone_number,
                    },
                },
                "school_name": education2.school_name,
                "degree": education2.degree,
                "field_of_study": education2.field_of_study,
                "date_from": education2.date_from,
                "date_to": education2.date_to,
                "is_current": education2.is_current,
            },
        ],
    }
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_education_not_found():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    employer_user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    industry = Industry.objects.create(
        name="Test Industry",
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=industry,
    )
    client.force_authenticate(user=employer_user)

    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    response = client.get(f"/api/candidates/{candidate.id}/education/")
    expected_data = {"count": 0, "next": None, "previous": None, "results": []}
    assert (
        response.status_code == HTTP_200_OK
    ), f"Expected status code 200 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_education_without_permission():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test1@gmail.com",
        password="<PASSWORD>",
        phone_number="123456789",
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    response = client.get(f"/api/candidates/{candidate.id}/education/")
    expected_data = {"detail": "Access restricted to employers only"}
    assert (
        response.status_code == HTTP_403_FORBIDDEN
    ), f"Expected status code 403 but got {response.status_code}"
    assert (
        response.json() == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_register_candidate_success():
    client = APIClient()
    country = Country.objects.create(
        name="Test Country",
    )
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    data = {
        "email": "test@gmail.com",
        "password": "testpassword",
        "phone_number": "1234567890",
        "city": city.id,
        "first_name": "John",
        "last_name": "Doe",
        "about": "about me",
        "resume": SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    }
    response = client.post("/api/candidates/register/", data, format="multipart")
    user = User.objects.get(email="test@gmail.com")
    candidate = Candidate.objects.get(user=user)
    expected_data = {
        "id": candidate.id,
        "user": {
            "id": user.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@gmail.com",
            "city": city.id,
            "phone_number": "1234567890",
        },
        "resume": f"http://testserver/media/{candidate.resume.name}",
        "about": "about me",
    }
    response_data = response.json()
    response_data.pop("access", None)
    response_data.pop("refresh", None)

    assert (
        response.status_code == HTTP_201_CREATED
    ), f"Expected status code 201 but got {response.status_code}"
    assert (
        response_data == expected_data
    ), f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_candidate_profile_success():
    client = APIClient()
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
        first_name="John",
        last_name="Doe",
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    response = client.get("/api/candidates/profile/")
    expected_data = {
        "id": candidate.id,
        "user": {
            "id": user.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@gmail.com",
            "city": city.id,
            "phone_number": "1234567890",
        },
        "resume": f"http://testserver/media/{candidate.resume.name}",
        "about": "about candidate",
    }
    assert response.status_code == HTTP_200_OK
    assert response.json() == expected_data


@pytest.mark.django_db
def test_get_candidate_profile_unauthorized():
    client = APIClient()
    response = client.get("/api/candidates/profile/")
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_candidate_profile_not_a_candidate():
    client = APIClient()
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="employer@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    Industry.objects.create(name="Test Industry")
    Employer.objects.create(
        user=user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=Industry.objects.first(),
    )
    client.force_authenticate(user=user)
    response = client.get("/api/candidates/profile/")
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_candidate_profile_success():
    client = APIClient()
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="test@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
        first_name="John",
        last_name="Doe",
    )
    candidate = Candidate.objects.create(
        user=user,
        about="about candidate",
        resume=SimpleUploadedFile(
            "resume.pdf", b"pdf content", content_type="application/pdf"
        ),
    )
    client.force_authenticate(user=user)
    update_data = {
        "about": "updated about",
    }
    response = client.patch("/api/candidates/profile/", update_data, format="json")
    assert response.status_code == HTTP_200_OK
    user.refresh_from_db()
    candidate.refresh_from_db()
    assert candidate.about == "updated about"


@pytest.mark.django_db
def test_update_candidate_profile_unauthorized():
    client = APIClient()
    update_data = {"about": "updated about"}
    response = client.patch("/api/candidates/profile/", update_data, format="json")
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_candidate_profile_not_a_candidate():
    client = APIClient()
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    user = User.objects.create_user(
        email="employer@gmail.com",
        password="<PASSWORD>",
        phone_number="1234567890",
        city=city,
    )
    Industry.objects.create(name="Test Industry")
    Employer.objects.create(
        user=user,
        company_name="Test Employer",
        website_url="www.test.com",
        description="Test employer",
        industry=Industry.objects.first(),
    )
    client.force_authenticate(user=user)
    update_data = {"about": "updated about"}
    response = client.patch("/api/candidates/profile/", update_data, format="json")
    assert response.status_code == HTTP_404_NOT_FOUND
