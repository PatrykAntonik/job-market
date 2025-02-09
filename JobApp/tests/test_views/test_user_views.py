import pytest
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from JobApp.views.user_views import *
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_view_success():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    user = User.objects.create_user(
        username='testUser',
        email='test@test.com',
        password='testPassword',
        is_candidate=True,
        phone_number='123456789',
        city=city,
        first_name='name',
        last_name='surname',
    )
    response = client.post(
        '/api/users/login/',
        {
            'username': user.username,
            'password': 'testPassword'
        },
        format='json'
    )
    assert response.status_code == HTTP_200_OK, f'Expected Response Code 200, but got {response.status_code}'
    assert 'access' in response.data, "Expected 'access' token in response"
    assert 'refresh' in response.data, "Expected 'refresh' token in response"
    assert response.data[
               'email'] == 'test@test.com', f"Expected email to be test@test.com, but got {response.data['email']}"


@pytest.mark.django_db
def test_login_view_success():
    client = APIClient()
    response = client.post(
        '/api/users/login/',
        {
            'username': 'userName',
            'password': 'testPassword'
        },
        format='json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
        f"Expected status code 401, but got {response.status_code}")
    assert 'access' not in response.data, "Should not include access token on invalid login"
    assert 'refresh' not in response.data, "Should not include refresh token on invalid login"
