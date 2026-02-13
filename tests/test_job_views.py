import pytest
from rest_framework import status
from rest_framework.test import APIClient

from JobApp.models import (
    Candidate,
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


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_data():
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    industry = Industry.objects.create(name="Technology")
    user = User.objects.create_user(
        email="employer@example.com",
        password="password123",
        phone_number="5100000000",
        city=city,
    )
    employer = Employer.objects.create(
        user=user,
        company_name="Employer Inc",
        website_url="https://employer.example.com",
        industry=industry,
    )
    location = EmployerLocation.objects.create(employer=employer, city=city)
    skill = Skill.objects.create(name="Python")
    job_offer = JobOffer.objects.create(
        employer=employer,
        location=location,
        position="Test Job Offer",
        remoteness=JobOffer.RemotenessLevel.ONSITE,
        contract=JobOffer.ContractType.B2B_CONTRACT,
        seniority=JobOffer.Seniority.JUNIOR,
    )
    JobOfferSkill.objects.create(offer=job_offer, skill=skill)
    return employer, user, industry, city, country, location, job_offer, skill


@pytest.fixture
def candidate_data(common_data):
    _, _, _, city, _, _, _, _ = common_data
    user = User.objects.create_user(
        email="candidate@example.com",
        password="password123",
        phone_number="5100000001",
        city=city,
    )
    candidate = Candidate.objects.create(user=user, about="Test candidate")
    return candidate, user


@pytest.mark.django_db
class TestSkillListView:
    def test_get_skills_success(self, api_client, common_data):
        _, _, _, _, _, _, _, skill = common_data
        response = api_client.get("/api/jobs/skills/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == skill.name


@pytest.mark.django_db
class TestIndustryListView:
    def test_get_industries_success(self, api_client, common_data):
        _, _, industry, _, _, _, _, _ = common_data
        response = api_client.get("/api/jobs/industries/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == industry.name


@pytest.mark.django_db
class TestSeniorityListView:
    def test_get_seniority_levels_success(self, api_client):
        response = api_client.get("/api/jobs/seniority/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) > 0


@pytest.mark.django_db
class TestContractTypeListView:
    def test_get_contract_types_success(self, api_client):
        response = api_client.get("/api/jobs/contract-types/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) > 0


@pytest.mark.django_db
class TestRemotenessLevelListView:
    def test_get_remoteness_levels_success(self, api_client):
        response = api_client.get("/api/jobs/remoteness-levels/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) > 0


@pytest.mark.django_db
class TestJobOfferListView:
    def test_get_job_offers_success(self, api_client, common_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        response = api_client.get("/api/jobs/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["position"] == job_offer.position


@pytest.mark.django_db
class TestJobOfferDetailView:
    def test_get_job_offer_success(self, api_client, common_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        response = api_client.get(f"/api/jobs/{job_offer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["position"] == job_offer.position

    def test_get_job_offer_not_found(self, api_client):
        response = api_client.get("/api/jobs/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestEmployerJobOfferListView:
    def test_get_employer_job_offers_success(self, api_client, common_data):
        employer, _, _, _, _, _, job_offer, _ = common_data
        response = api_client.get(f"/api/jobs/employer/{employer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["position"] == job_offer.position

    def test_get_employer_job_offers_not_found(self, api_client):
        response = api_client.get("/api/jobs/employer/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestJobOfferProfileListView:
    def test_get_job_offers_profile_success(self, api_client, common_data):
        _, user, _, _, _, _, _, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/jobs/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_job_offers_profile_unauthorized(self, api_client):
        response = api_client.get("/api/jobs/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_offer_profile_success(self, api_client, common_data):
        _, user, _, _, _, location, _, skill = common_data
        api_client.force_authenticate(user=user)
        data = {
            "position": "New Job Offer",
            "location": location.id,
            "remoteness": JobOffer.RemotenessLevel.REMOTE,
            "contract": JobOffer.ContractType.EMPLOYMENT_CONTRACT,
            "seniority": JobOffer.Seniority.SENIOR,
            "description": "New role description",
            "wage": 10000,
            "currency": "USD",
            "skills": [skill.id],
        }
        response = api_client.post("/api/jobs/profile/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        new_offer = JobOffer.objects.get(id=response.data["id"])
        assert new_offer.employer == common_data[0]
        skill_names = {entry.skill.name for entry in new_offer.jobofferskill_set.all()}
        assert skill_names == {skill.name}


@pytest.mark.django_db
class TestJobOfferProfileDetailView:
    def test_get_job_offer_profile_success(self, api_client, common_data):
        _, user, _, _, _, _, job_offer, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/jobs/profile/{job_offer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["position"] == job_offer.position

    def test_get_job_offer_profile_unauthorized(self, api_client, common_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        response = api_client.get(f"/api/jobs/profile/{job_offer.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_offer_profile_success(self, api_client, common_data):
        _, user, _, _, _, _, job_offer, _ = common_data
        api_client.force_authenticate(user=user)
        data = {"position": "Updated Job Offer"}
        response = api_client.patch(
            f"/api/jobs/profile/{job_offer.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        job_offer.refresh_from_db()
        assert job_offer.position == "Updated Job Offer"

    def test_delete_job_offer_profile_success(self, api_client, common_data):
        _, user, _, _, _, _, job_offer, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/jobs/profile/{job_offer.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobOffer.objects.filter(id=job_offer.id).exists()


@pytest.mark.django_db
class TestApplyToJobOfferView:
    def test_apply_success(self, api_client, common_data, candidate_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        candidate, user = candidate_data
        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"/api/jobs/{job_offer.id}/apply/", {}, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert OfferResponse.objects.filter(
            offer=job_offer, candidate=candidate
        ).exists()
        assert response.data["offer"]["id"] == job_offer.id
        assert response.data["candidate"]["id"] == candidate.id

    def test_apply_duplicate_returns_400(self, api_client, common_data, candidate_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        candidate, user = candidate_data
        OfferResponse.objects.create(offer=job_offer, candidate=candidate)
        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"/api/jobs/{job_offer.id}/apply/", {}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_apply_unauthorized(self, api_client, common_data):
        _, _, _, _, _, _, job_offer, _ = common_data
        response = api_client.post(
            f"/api/jobs/{job_offer.id}/apply/", {}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_apply_as_employer_forbidden(self, api_client, common_data):
        _, employer_user, _, _, _, _, job_offer, _ = common_data
        api_client.force_authenticate(user=employer_user)
        response = api_client.post(
            f"/api/jobs/{job_offer.id}/apply/", {}, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apply_offer_not_found(self, api_client, candidate_data):
        _, user = candidate_data
        api_client.force_authenticate(user=user)
        response = api_client.post("/api/jobs/999999/apply/", {}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestJobOfferApplicantsListView:
    def test_list_applicants_success(self, api_client, common_data, candidate_data):
        employer, employer_user, _, _, _, _, job_offer, _ = common_data
        candidate, _ = candidate_data
        OfferResponse.objects.create(offer=job_offer, candidate=candidate)

        api_client.force_authenticate(user=employer_user)
        response = api_client.get(f"/api/jobs/profile/{job_offer.id}/applicants/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["offer"]["id"] == job_offer.id
        assert response.data["results"][0]["candidate"]["id"] == candidate.id

    def test_list_applicants_for_other_employer_offer_404(
        self, api_client, common_data, candidate_data
    ):
        _, employer_user, _, city, _, _, job_offer, _ = common_data
        candidate, _ = candidate_data
        OfferResponse.objects.create(offer=job_offer, candidate=candidate)

        other_user = User.objects.create_user(
            email="other_employer@example.com",
            password="password123",
            phone_number="5100000002",
            city=city,
        )
        other_employer = Employer.objects.create(
            user=other_user,
            company_name="Other Employer Inc",
            website_url="https://other-employer.example.com",
            industry=common_data[2],
        )
        api_client.force_authenticate(user=other_user)

        response = api_client.get(f"/api/jobs/profile/{job_offer.id}/applicants/")

        # Must not leak existence of offers belonging to other employers.
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_applicants_as_candidate_forbidden(
        self, api_client, common_data, candidate_data
    ):
        _, _, _, _, _, _, job_offer, _ = common_data
        _, candidate_user = candidate_data
        api_client.force_authenticate(user=candidate_user)

        response = api_client.get(f"/api/jobs/profile/{job_offer.id}/applicants/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
