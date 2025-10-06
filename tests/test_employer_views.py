import pytest
from rest_framework import status
from rest_framework.test import APIClient

from JobApp.models import (
    Benefit,
    City,
    Country,
    Employer,
    EmployerBenefit,
    EmployerLocation,
    Industry,
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
    industry = Industry.objects.create(name="Test Industry")
    user = User.objects.create_user(
        email="test@example.com", password="password123", city=city
    )
    employer = Employer.objects.create(
        user=user,
        company_name="Test Company",
        industry=industry,
        website_url="https://example.com",
    )
    return employer, user, industry, city, country


@pytest.mark.django_db
class TestEmployerListView:
    def test_get_employers_success(self, api_client, common_data):
        employer, _, _, _, _ = common_data
        response = api_client.get("/api/employers/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["company_name"] == employer.company_name


@pytest.mark.django_db
class TestEmployerDetailView:
    def test_get_employer_success(self, api_client, common_data):
        employer, _, _, _, _ = common_data
        response = api_client.get(f"/api/employers/{employer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["company_name"] == employer.company_name

    def test_get_employer_not_found(self, api_client):
        response = api_client.get("/api/employers/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestEmployerProfileView:
    def test_get_employer_profile_success(self, api_client, common_data):
        _, user, _, _, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/employers/profile/")
        assert response.status_code == status.HTTP_200_OK

    def test_get_employer_profile_unauthorized(self, api_client):
        response = api_client.get("/api/employers/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRegisterEmployerView:
    def test_register_employer_success(self, api_client, common_data):
        _, _, industry, city, _ = common_data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "phone_number": "1234567890",
            "city": city.id,
            "company_name": "New Company",
            "industry": industry.id,
        }
        response = api_client.post("/api/employers/register/", data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_employer_invalid_data(self, api_client, common_data):
        _, _, industry, _, _ = common_data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "phone_number": "1234567890",
            "company_name": "New Company",
            "industry": industry.id,
        }
        response = api_client.post("/api/employers/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEmployerLocationListView:
    def test_get_employer_locations_success(self, api_client, common_data):
        employer, _, _, city, _ = common_data
        EmployerLocation.objects.create(employer=employer, city=city)
        response = api_client.get(f"/api/employers/{employer.id}/locations/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestEmployerLocationDetailView:
    def test_get_employer_location_detail_success(self, api_client, common_data):
        employer, user, _, city, _ = common_data
        location = EmployerLocation.objects.create(employer=employer, city=city)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/employers/profile/locations/{location.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_get_employer_location_detail_unauthorized(self, api_client, common_data):
        employer, _, _, city, _ = common_data
        location = EmployerLocation.objects.create(employer=employer, city=city)
        response = api_client.get(f"/api/employers/profile/locations/{location.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestEmployerLocationListProfileView:
    def test_get_employer_locations_profile_success(self, api_client, common_data):
        employer, user, _, city, _ = common_data
        EmployerLocation.objects.create(employer=employer, city=city)
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/employers/profile/locations/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_create_employer_location_profile_success(self, api_client, common_data):
        _, user, _, city, _ = common_data
        api_client.force_authenticate(user=user)
        data = {"city": city.id}
        response = api_client.post("/api/employers/profile/locations/", data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestEmployerProfileBenefitListView:
    def test_get_employer_benefits_profile_success(self, api_client, common_data):
        employer, user, _, _, _ = common_data
        benefit = Benefit.objects.create(name="Test Benefit")
        EmployerBenefit.objects.create(employer=employer, benefit=benefit)
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/employers/profile/benefits/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_create_employer_benefit_profile_success(self, api_client, common_data):
        _, user, _, _, _ = common_data
        benefit = Benefit.objects.create(name="Test Benefit")
        api_client.force_authenticate(user=user)
        data = {"benefit": benefit.id}
        response = api_client.post("/api/employers/profile/benefits/", data)
        assert response.status_code == status.HTTP_201_CREATED
