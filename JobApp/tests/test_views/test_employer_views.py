from http.client import responses

import pytest
from JobApp.views.employer_views import *
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_get_industries_success():
    industry_1 = Industry.objects.create(name="Test1")
    industry_2 = Industry.objects.create(name="Test2")

    client = APIClient()

    response = client.get('/api/employers/industries/')

    assert response.status_code == status.HTTP_200_OK
    expected_data = [
        {"id": industry_1.id, "name": industry_1.name},
        {"id": industry_2.id, "name": industry_2.name},
    ]
    assert response.json() == expected_data


@pytest.mark.django_db
def test_get_industry_success():
    industry_1 = Industry.objects.create(name="Test1")

    client = APIClient()

    response = client.get(f'/api/employers/industries/{industry_1.id}/')

    assert response.status_code == status.HTTP_200_OK
    expected_data = {"id": industry_1.id, "name": industry_1.name}

    assert response.json() == expected_data
