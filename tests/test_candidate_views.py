from datetime import date
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from rest_framework import status
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


def resume_file():
    return SimpleUploadedFile(
        f"resume-{uuid.uuid4()}.pdf", b"pdf content", content_type="application/pdf"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_data():
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    industry = Industry.objects.create(name="Test Industry")
    employer_user = User.objects.create_user(
        email="employer@example.com",
        password="password123",
        phone_number="7000000000",
        city=city,
    )
    Employer.objects.create(
        user=employer_user,
        company_name="Employer Inc",
        industry=industry,
        website_url="https://employer.example.com",
    )
    candidate_user1 = User.objects.create_user(
        email="candidate1@example.com",
        password="password123",
        phone_number="5500000001",
        city=city,
        first_name="John1",
        last_name="Doe1",
    )
    candidate1 = Candidate.objects.create(
        user=candidate_user1, about="About candidate 1", resume=resume_file()
    )
    candidate_user2 = User.objects.create_user(
        email="candidate2@example.com",
        password="password123",
        phone_number="5500000002",
        city=city,
        first_name="John2",
        last_name="Doe2",
    )
    candidate2 = Candidate.objects.create(
        user=candidate_user2, about="About candidate 2", resume=resume_file()
    )
    return (
        country,
        city,
        industry,
        employer_user,
        candidate_user1,
        candidate1,
        candidate_user2,
        candidate2,
    )


@pytest.mark.django_db
class TestCandidateListView:
    def test_get_candidates_success(self, api_client, common_data):
        _, _, _, employer_user, _, candidate1, _, candidate2 = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get("/api/candidates/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        returned_ids = {item["id"] for item in response.data["results"]}
        assert returned_ids == {candidate1.id, candidate2.id}
        assert all("total_experience" in item for item in response.data["results"])

    def test_get_candidates_without_permission(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.get("/api/candidates/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Access restricted to employers only"


@pytest.mark.django_db
class TestCandidateDetailView:
    def test_get_candidate_success(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == candidate.id
        assert response.data["user"]["email"] == candidate.user.email

    def test_get_candidate_not_found(self, api_client, common_data):
        _, _, _, employer_user, _, _, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get("/api/candidates/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_candidate_without_permission(self, api_client, common_data):
        _, _, _, _, _, candidate, _, other_candidate = common_data
        api_client.force_authenticate(user=other_candidate.user)
        response = api_client.get(f"/api/candidates/{candidate.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Access restricted to employers only"


@pytest.mark.django_db
class TestCandidateSkillListView:
    def test_get_candidate_skills_success(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        skill1 = Skill.objects.create(name="Python")
        skill2 = Skill.objects.create(name="Django")
        CandidateSkill.objects.create(candidate=candidate, skill=skill1)
        CandidateSkill.objects.create(candidate=candidate, skill=skill2)
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/skills/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        returned_skill_ids = {item["skill"]["id"] for item in response.data["results"]}
        assert returned_skill_ids == {skill1.id, skill2.id}

    def test_get_candidate_skills_empty(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/skills/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_get_candidate_skills_without_permission(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.get(f"/api/candidates/{candidate.id}/skills/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Access restricted to employers only"


@pytest.mark.django_db
class TestCandidateExperienceListView:
    def test_get_candidate_experience_success(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        experience1 = CandidateExperience.objects.create(
            candidate=candidate,
            company_name="Company A",
            date_from=date(2020, 1, 1),
            date_to=date(2021, 1, 1),
        )
        experience2 = CandidateExperience.objects.create(
            candidate=candidate,
            company_name="Company B",
            date_from=date(2021, 2, 1),
            date_to=date(2022, 2, 1),
        )
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/experience/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        returned_ids = {item["id"] for item in response.data["results"]}
        assert returned_ids == {experience1.id, experience2.id}

    def test_get_candidate_experience_empty(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/experience/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_get_candidate_experience_without_permission(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.get(f"/api/candidates/{candidate.id}/experience/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Access restricted to employers only"


@pytest.mark.django_db
class TestCandidateEducationListView:
    def test_get_candidate_education_success(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        education1 = CandidateEducation.objects.create(
            candidate=candidate,
            school_name="School A",
            degree="BSc",
            date_from=date(2016, 1, 1),
            date_to=date(2019, 1, 1),
        )
        education2 = CandidateEducation.objects.create(
            candidate=candidate,
            school_name="School B",
            degree="MSc",
            date_from=date(2019, 9, 1),
            date_to=date(2021, 6, 1),
        )
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/education/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        returned_ids = {item["id"] for item in response.data["results"]}
        assert returned_ids == {education1.id, education2.id}

    def test_get_candidate_education_empty(self, api_client, common_data):
        _, _, _, employer_user, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/candidates/{candidate.id}/education/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_get_candidate_education_without_permission(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.get(f"/api/candidates/{candidate.id}/education/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Access restricted to employers only"


@pytest.mark.django_db
class TestCandidateRegistrationView:
    def test_register_candidate_success(self, api_client, common_data):
        _, city, _, _, _, _, _, _ = common_data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "phone_number": "8800000000",
            "city": city.id,
            "about": "About me",
            "resume": resume_file(),
        }
        response = api_client.post(
            "/api/candidates/register/", data, format="multipart"
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.data.copy()
        assert "access" in response_data and "refresh" in response_data
        response_data.pop("access")
        response_data.pop("refresh")
        candidate = Candidate.objects.get(user__email=data["email"])
        assert response_data["id"] == candidate.id
        assert response_data["user"]["email"] == data["email"]
        assert response_data["about"] == data["about"]


@pytest.mark.django_db
class TestCandidateProfileView:
    def test_get_candidate_profile_success(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.get("/api/candidates/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == candidate.id
        assert response.data["user"]["email"] == candidate.user.email

    def test_get_candidate_profile_unauthorized(self, api_client):
        response = api_client.get("/api/candidates/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_candidate_profile_not_a_candidate(self, api_client, common_data):
        _, _, _, employer_user, _, _, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.get("/api/candidates/profile/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCandidateProfileUpdateView:
    def test_update_candidate_profile_success(self, api_client, common_data):
        _, _, _, _, _, candidate, _, _ = common_data
        api_client.force_authenticate(user=candidate.user)
        response = api_client.patch(
            "/api/candidates/profile/",
            {"about": "Updated about"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        candidate.refresh_from_db()
        assert candidate.about == "Updated about"

    def test_update_candidate_profile_unauthorized(self, api_client):
        response = api_client.patch(
            "/api/candidates/profile/",
            {"about": "Updated about"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_candidate_profile_not_a_candidate(self, api_client, common_data):
        _, _, _, employer_user, _, _, _, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.patch(
            "/api/candidates/profile/",
            {"about": "Updated about"},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
