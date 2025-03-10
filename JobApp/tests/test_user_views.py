import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from JobApp.views.user_views import *
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_view_success():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    user = User.objects.create_user(
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
            'email': user.email,
            'password': 'testPassword'
        },
        format='json'
    )
    assert response.status_code == HTTP_200_OK, f'Expected status code 200, but got {response.status_code}'
    assert 'access' in response.data, "Expected 'access' token in response"
    assert 'refresh' in response.data, "Expected 'refresh' token in response"
    assert response.data[
               'email'] == 'test@test.com', f"Expected email to be test@test.com, but got {response.data['email']}"


@pytest.mark.django_db
def test_login_view_fail():
    client = APIClient()
    response = client.post(
        '/api/users/login/',
        {
            'email': 'email',
            'password': 'testPassword'
        },
        format='json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
        f"Expected status code 401, but got {response.status_code}")
    assert 'access' not in response.data, "Should not include access token on invalid login"
    assert 'refresh' not in response.data, "Should not include refresh token on invalid login"


@pytest.mark.django_db
def test_register_user_success():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    response = client.post(
        '/api/users/register/',
        {
            'email': 'test@test.com',
            'password': 'testPassword',
            'phone_number': '123456789',
            'city': city.id,
            'first_name': 'name',
            'last_name': 'surname',
            'is_candidate': True
        },
        format='json'
    )
    expected_data = {
        'id': 1,
        'email': 'test@test.com',
    }
    assert response.status_code == HTTP_201_CREATED, f'Expected response code 201, but got {response.status_code}'
    assert 'access' in response.data, "Expected access token in response"
    assert 'refresh' in response.data, "Expected refresh token in response"
    assert response.data[
               'email'] == 'test@test.com', f"Expected email to be 'test@test.com', but got {response.data['email']}"


@pytest.mark.django_db
def test_register_user_fail():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    response1 = client.post(
        '/api/users/register/',
        {
            'email': 'test@test.com',
            'password': 'firstPassword',
            'phone_number': '123456789',
            'city': city.id,
            'first_name': 'name1',
            'last_name': 'surname1',
            'is_candidate': True
        },
        format='json'
    )
    assert response1.status_code == 201, f"Expected status 201, got {response1.status_code}"
    response2 = client.post(
        '/api/users/register/',
        {
            'email': 'test@test.com',
            'password': 'secondPassword',
            'phone_number': '987654321',
            'city': city.id,
            'first_name': 'name2',
            'last_name': 'surname2',
            'is_candidate': True
        },
        format='json'
    )
    assert response2.status_code == 400, f"Expected status 400, got {response2.status_code}"
    assert 'message' in response2.data
    assert response2.data['message'] == 'User with this email already exists'


@pytest.mark.django_db
def test_get_user_success():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    user = User.objects.create_superuser(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='testPassword',
        phone_number='123456789',
        city=city,
    )
    client.force_authenticate(user=user)
    expected_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'city': user.city.id,
        'is_employer': user.is_employer,
        'is_candidate': user.is_candidate
    }
    response = client.get(f'/api/users/{user.id}/')
    assert response.status_code == HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
    assert response.json() == expected_data, f'Expected {expected_data}, got {response.json()}'


@pytest.mark.django_db
def test_get_user_not_found():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    user = User.objects.create_superuser(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='testPassword',
        phone_number='123456789',
        city=city,
    )

    client.force_authenticate(user=user)
    expected_data = {
        'message': 'User not found'
    }
    response = client.get(f'/api/users/{user.id + 1}/')
    assert response.status_code == HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"
    assert response.json() == expected_data, f'Expected {expected_data}, got {response.json()}'


@pytest.mark.django_db
def test_get_user_unauthorized():
    client = APIClient()
    country = Country.objects.create(name='TestCountry')
    city = City.objects.create(name='TestCity', country=country, zip_code='12345', province='TestProvince')
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='testPassword',
        phone_number='123456789',
        city=city,
    )
    client.force_authenticate(user=user)
    expected_data = {'detail': 'You do not have permission to perform this action.'}
    response = client.get(f'/api/users/{user.id}/')
    assert response.status_code == HTTP_403_FORBIDDEN, f"Expected status code 403, got {response.status_code}"
    assert response.json() == expected_data, f'Expected {expected_data}, got {response.json()}'


@pytest.mark.django_db
def test_get_user_profile_success():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    expected_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'city': user.city.id,
        'is_employer': user.is_employer,
        'is_candidate': user.is_candidate,
    }
    response = client.get('/api/users/profile/')
    assert response.status_code == HTTP_200_OK, f'Expected status code to be 200, but got {response.code}'
    assert response.json() == expected_data, f'Expected {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_get_user_profile_unauthenticated():
    client = APIClient()
    response = client.get('/api/users/profile/')
    expected_data = {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == HTTP_401_UNAUTHORIZED, f'Expected status code to be 401, but got {response.code}'
    assert response.json() == expected_data, f'Expected {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_get_users_success():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_superuser(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='testPassword',
        phone_number='123456789',
        city=city,
    )
    user_1 = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        city=city,
    )
    user_2 = User.objects.create_user(
        email='test2@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567891',
        city=city,
    )
    client.force_authenticate(user=user)
    response = client.get('/api/users/')
    expected_data = {
        'count': 3,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'city': user.city.id,
                'is_employer': user.is_employer,
                'is_candidate': user.is_candidate,
            },
            {
                'id': user_1.id,
                'first_name': user_1.first_name,
                'last_name': user_1.last_name,
                'email': user_1.email,
                'phone_number': user_1.phone_number,
                'city': user_1.city.id,
                'is_employer': user_1.is_employer,
                'is_candidate': user_1.is_candidate,
            },
            {
                'id': user_2.id,
                'first_name': user_2.first_name,
                'last_name': user_2.last_name,
                'email': user_2.email,
                'phone_number': user_2.phone_number,
                'city': user_2.city.id,
                'is_employer': user_2.is_employer,
                'is_candidate': user_2.is_candidate,
            },
        ],
    }
    assert response.status_code == HTTP_200_OK, f'Expected status code 200, got {response.status_code}'
    assert response.json() == expected_data, f'Expected {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_get_users_without_permissions():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='testPassword',
        phone_number='123456789',
        city=city,
    )
    client.force_authenticate(user=user)
    response = client.get('/api/users/')
    expected_data = {'detail': 'You do not have permission to perform this action.'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403, got {response.status_code}'
    assert response.json() == expected_data, f'Expected {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_profile_success():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    new_city = City.objects.create(
        country=country,
        name='new city name',
        province='province name',
        zip_code='41-800'
    )
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': 'password',
        'phone_number': user.phone_number,
        'city': new_city.id
    }
    response = client.put(
        '/api/users/profile/',
        data,
        format='json'
    )
    expected_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'city': user.city.id,
        'is_employer': user.is_employer,
        'is_candidate': user.is_candidate,
    }
    assert response.status_code == HTTP_201_CREATED, f'Expected status code to be 201, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_profile_unique_email_fail():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    user_2 = User.objects.create(
        first_name='name',
        last_name='surname',
        email='tes2t@test.com',
        password='password',
        phone_number='1234567890',
        city=city
    )
    client.force_authenticate(user=user)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user_2.email,
        'password': 'password',
        'phone_number': user.phone_number,
        'city': user.city.id
    }
    response = client.put(
        '/api/users/profile/',
        data,
        format='json'
    )
    expected_data = {
        'message': 'This email address is already in use by another account'
    }
    assert response.status_code == HTTP_400_BAD_REQUEST, f'Expected status code to be 400, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_profile_unique_phone_fail():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    user_2 = User.objects.create(
        first_name='name',
        last_name='surname',
        email='tes2t@test.com',
        password='password',
        phone_number='1234567890',
        city=city
    )
    client.force_authenticate(user=user)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': 'password',
        'phone_number': user_2.phone_number,
        'city': user.city.id
    }
    response = client.put(
        '/api/users/profile/',
        data,
        format='json'
    )
    expected_data = {
        'message': 'This phone number is already in use by another account'
    }
    assert response.status_code == HTTP_400_BAD_REQUEST, f'Expected status code to be 400, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_profile_unauthenticated():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': 'password',
        'phone_number': user.phone_number,
        'city': user.city.id
    }
    response = client.put(
        '/api/users/profile/',
        data,
        format='json'
    )
    expected_data = {
        'detail': 'Authentication credentials were not provided.'
    }
    assert response.status_code == HTTP_401_UNAUTHORIZED, f'Expected status code to be 401, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_password_success():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    data = {
        'old_password': 'password',
        'new_password': 'newPassword',
        'confirm_password': 'newPassword'
    }
    response = client.put(
        '/api/users/profile/password/',
        data,
        format='json'
    )
    expected_data = {
        'message': 'Password updated successfully'
    }
    assert response.status_code == HTTP_201_CREATED, f'Expected status code to be 201, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_password_wrong_old_password():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    data = {
        'old_password': 'wrong_old_password',
        'new_password': 'newPassword',
        'confirm_password': 'newPassword'
    }
    response = client.put(
        '/api/users/profile/password/',
        data,
        format='json'
    )
    expected_data = {
        'message': 'Old password is incorrect'
    }
    assert response.status_code == HTTP_400_BAD_REQUEST, f'Expected status code to be 400, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_update_user_password_mismatched_confirm_new_password():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    data = {
        'old_password': 'password',
        'new_password': 'newPassword',
        'confirm_password': 'wrong_newPassword'
    }
    response = client.put(
        '/api/users/profile/password/',
        data,
        format='json'
    )
    expected_data = {
        'message': 'New passwords do not match'
    }
    assert response.status_code == HTTP_400_BAD_REQUEST, f'Expected status code to be 400, but got {response.status_code}'
    assert response.json() == expected_data, f'Expected  {expected_data}, but got {response.json()}'


@pytest.mark.django_db
def test_delete_user_success():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    response = client.delete(
        '/api/users/profile/',
        data={'password': 'password'},
        format='json'
    )
    assert response.status_code == HTTP_204_NO_CONTENT, f'Expected status code to be 204, but got {response.status_code}'


@pytest.mark.django_db
def test_delete_user_unauthenticated():
    client = APIClient()
    country = Country.objects.create(name='country')
    city = City.objects.create(
        country=country,
        name='city name',
        province='province name',
        zip_code='43-300'
    )
    user = User.objects.create_user(
        first_name='name',
        last_name='surname',
        email='test@test.com',
        password='password',
        phone_number='123456789',
        city=city
    )
    client.force_authenticate(user=user)
    response = client.delete(
        '/api/users/profile/',
        data={'password': 'wrong_password'},
        format='json'
    )
    assert response.status_code == HTTP_400_BAD_REQUEST, f'Expected status code to be 400, but got {response.status_code}'
