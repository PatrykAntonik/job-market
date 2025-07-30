from http.client import responses
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from JobApp.views.employer_views import *
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_get_countries():
    country = Country.objects.create(
        name="Country1"
    )
    country2 = Country.objects.create(
        name="Country2"
    )
    client = APIClient()
    expected_data = [
        {'id': country.id, 'name': country.name},
        {'id': country2.id, 'name': country2.name},
    ]
    response = client.get('/api/employers/countries/')
    assert response.status_code == status.HTTP_200_OK, f"Expected: status code 200, but got: {response.status_code}"
    assert response.json() == expected_data, f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_cities():
    client = APIClient()
    country = Country.objects.create(
        name="Country1"
    )
    city = City.objects.create(
        name="City1",
        country=country,
        province='Province1',
        zip_code='12345'
    )
    city2 = City.objects.create(
        name="City2",
        country=country,
        province='Province1',
        zip_code='12345'
    )
    expected_data = [
        {
            'country': country.id,
            'id': city.id,
            'name': city.name,
            'province': city.province,
            'zip_code': city.zip_code
        },
        {
            'country': country.id,
            'id': city2.id,
            'name': city2.name,
            'province': city2.province,
            'zip_code': city2.zip_code
        },
    ]
    response = client.get('/api/employers/cities/')
    assert response.status_code == status.HTTP_200_OK, f"Expected: status code 200, but got: {response.status_code}"
    assert response.json() == expected_data, f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_industries_success():
    industry_1 = Industry.objects.create(name="Test1")
    industry_2 = Industry.objects.create(name="Test2")
    client = APIClient()
    response = client.get('/api/employers/industries/')
    assert response.status_code == status.HTTP_200_OK, f'Expected: status code 200, but got: {response.status_code}'
    expected_data = [
        {"id": industry_1.id, "name": industry_1.name},
        {"id": industry_2.id, "name": industry_2.name},
    ]
    assert response.json() == expected_data, f"Expected: {expected_data}, but got: {response.json()}"


@pytest.mark.django_db
def test_get_industry_success():
    industry_1 = Industry.objects.create(name="Test1")
    client = APIClient()
    response = client.get(f'/api/employers/industries/{industry_1.id}/')
    assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, but got {response.status_code}"
    expected_data = {"id": industry_1.id, "name": industry_1.name}
    assert response.json() == expected_data, f"Expected {expected_data}, but got {response.json()}"


@pytest.mark.django_db
def test_get_industry_not_found():
    non_existent_id = 999
    client = APIClient()
    response = client.get(f'/api/industry/{non_existent_id}/', HTTP_ACCEPT='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, but got {response.status_code}"


@pytest.mark.django_db
def test_get_employers_success():
    industry = Industry.objects.create(
        name='Test Industry',
    )
    country = Country.objects.create(
        name='Test Country',
    )
    city = City.objects.create(
        name='Test City',
        country=country,
        province='Test Province',
        zip_code='12345'
    )
    user1 = User.objects.create_user(
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    user2 = User.objects.create_user(
        email='test2@gmail.com',
        password='<PASSWORD>',
        phone_number='01234567890',
        is_employer=True,
        city=city,
    )
    employer1 = Employer.objects.create(
        user=user1,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )
    employer2 = Employer.objects.create(
        user=user2,
        company_name='Test Employer2',
        website_url='www.test2.com',
        description='Test employer 2',
        industry=industry
    )

    client = APIClient()

    response = client.get('/api/employers/')

    expected_data = [
        {
            "id": employer1.id,
            "user": {
                "id": user1.id,
                "first_name": "",
                "last_name": "",
                "email": "test@gmail.com",
                "city": user1.city.id,
                "phone_number": "1234567890",
                "is_employer": True,
                "is_candidate": False
            },
            "company_name": "Test Employer",
            "website_url": "www.test.com",
            "industry": {
                "id": industry.id,
                "name": "Test Industry"
            },
            "description": "Test employer",
            "benefits": []
        },
        {
            "id": employer2.id,
            "user": {
                "id": user2.id,
                "first_name": "",
                "last_name": "",
                "email": "test2@gmail.com",
                "city": user2.city.id,
                "phone_number": "01234567890",
                "is_employer": True,
                "is_candidate": False
            },
            "company_name": "Test Employer2",
            "website_url": "www.test2.com",
            "industry": {
                "id": industry.id,
                "name": "Test Industry"
            },
            "description": "Test employer 2",
            "benefits": []
        }
    ]
    assert response.status_code == HTTP_200_OK, f"Expected status code 200, but got {response.status_code}"
    assert response.json() == expected_data, f"Expected {expected_data}, but got {response.json()}"


@pytest.mark.django_db
def test_get_employer_success():
    industry = Industry.objects.create(
        name='Test Industry',
    )
    country = Country.objects.create(
        name='Test Country',
    )
    city = City.objects.create(
        name='Test City',
        country=country,
        province='Test Province',
        zip_code='12345'
    )
    user = User.objects.create_user(
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )
    client = APIClient()
    response = client.get(f'/api/employers/{employer.id}/')

    expected_data = {
        "id": employer.id,
        "user": {
            "id": user.id,
            "first_name": "",
            "last_name": "",
            "email": "test@gmail.com",
            "city": user.city.id,
            "phone_number": "1234567890",
            "is_employer": True,
            "is_candidate": False
        },
        "company_name": "Test Employer",
        "website_url": "www.test.com",
        "industry": {
            "id": industry.id,
            "name": "Test Industry"
        },
        "description": "Test employer",
        "benefits": []
    }

    assert response.status_code == HTTP_200_OK, f"Expected status code 200, but got {response.status_code}"
    assert response.json() == expected_data, f"Expected {expected_data}, but got {response.json()}"


@pytest.mark.django_db
def test_get_employer_not_found():
    non_existent_employer_id = 999
    client = APIClient()
    response = client.get(f'/api/employers/{non_existent_employer_id}/')
    assert response.status_code == HTTP_404_NOT_FOUND, f"Expected status code 404, but got {response.status_code}"


@pytest.mark.django_db
def test_employer_locations():
    industry = Industry.objects.create(
        name='Test Industry',
    )
    country = Country.objects.create(
        name='Test Country',
    )
    city = City.objects.create(
        name='Test City',
        country=country,
        province='Test Province',
        zip_code='12345'
    )
    city2 = City.objects.create(
        name='Test City2',
        country=country,
        province='Test Province',
        zip_code='12345'
    )
    user = User.objects.create_user(
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    employer = Employer.objects.create(
        user=user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )
    employer_location = EmployerLocation.objects.create(
        employer=employer,
        city=city,
    )
    employer_location2 = EmployerLocation.objects.create(
        employer=employer,
        city=city2,
    )
    expected_data = [
        {
            'id': 1,
            'employer': {
                "id": employer.id,
                "user": {
                    "id": user.id,
                    "first_name": "",
                    "last_name": "",
                    "email": "test@gmail.com",
                    "city": user.city.id,
                    "phone_number": "1234567890",
                    "is_employer": True,
                    "is_candidate": False
                },
                "company_name": "Test Employer",
                "website_url": "www.test.com",
                "industry": {
                    "id": industry.id,
                    "name": "Test Industry"
                },
                "description": "Test employer",
                "benefits": []
            },
            'city': 1
        },
        {
            'id': 2,
            'employer': {
                "id": employer.id,
                "user": {
                    "id": user.id,
                    "first_name": "",
                    "last_name": "",
                    "email": "test@gmail.com",
                    "city": user.city.id,
                    "phone_number": "1234567890",
                    "is_employer": True,
                    "is_candidate": False
                },
                "company_name": "Test Employer",
                "website_url": "www.test.com",
                "industry": {
                    "id": industry.id,
                    "name": "Test Industry"
                },
                "description": "Test employer",
                "benefits": []
            },
            'city': 2
        },

    ]
    client = APIClient()
    response = client.get(f'/api/employers/{employer.id}/locations/')
    assert response.status_code == HTTP_200_OK, f"Expected status code 200, but got {response.status_code}"
    assert response.json() == expected_data, f"Expected {expected_data}, but got {response.json()}"
