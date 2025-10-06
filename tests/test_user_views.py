import pytest
from rest_framework import status
from rest_framework.test import APIClient

from JobApp.models import City, Country, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_data():
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(
        name="Test City", country=country, province="Test Province", zip_code="12345"
    )
    other_city = City.objects.create(
        name="Alt City", country=country, province="Alt Province", zip_code="54321"
    )
    admin_user = User.objects.create_superuser(
        email="admin@example.com",
        password="password123",
        phone_number="600000000",
        city=city,
        first_name="Admin",
        last_name="User",
    )
    user1 = User.objects.create_user(
        email="user1@example.com",
        password="password123",
        phone_number="600000001",
        city=city,
        first_name="Test",
        last_name="User1",
    )
    user2 = User.objects.create_user(
        email="user2@example.com",
        password="password123",
        phone_number="600000002",
        city=other_city,
        first_name="Test",
        last_name="User2",
    )
    return admin_user, user1, user2, city, other_city, country


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        response = api_client.post(
            "/api/users/login/",
            {"email": user.email, "password": "password123"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["email"] == user.email

    def test_login_failure(self, api_client):
        response = api_client.post(
            "/api/users/login/",
            {"email": "missing@example.com", "password": "badpass"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.data
        assert "refresh" not in response.data


@pytest.mark.django_db
class TestRegisterUserView:
    def test_register_user_success(self, api_client, common_data):
        _, _, _, city, _, _ = common_data
        payload = {
            "email": "test@test.com",
            "password": "testPassword",
            "phone_number": "123456789",
            "city": city.id,
            "first_name": "Test",
            "last_name": "User",
        }
        response = api_client.post("/api/users/register/", payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data and "refresh" in response.data
        assert response.data["email"] == payload["email"]


@pytest.mark.django_db
class TestUserDetailView:
    def test_get_user_success(self, api_client, common_data):
        admin_user, target_user, _, _, _, _ = common_data
        api_client.force_authenticate(user=admin_user)

        response = api_client.get(f"/api/users/{target_user.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == target_user.id
        assert response.data["email"] == target_user.email

    def test_get_user_not_found(self, api_client, common_data):
        admin_user, _, _, _, _, _ = common_data
        api_client.force_authenticate(user=admin_user)
        response = api_client.get("/api/users/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_forbidden_for_regular_user(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/users/{user.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )


@pytest.mark.django_db
class TestUserProfileView:
    def test_get_profile_success(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/users/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get("/api/users/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


@pytest.mark.django_db
class TestUserListView:
    def test_list_users_success(self, api_client, common_data):
        admin_user, user1, user2, _, _, _ = common_data
        api_client.force_authenticate(user=admin_user)
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        emails = {item["email"] for item in response.data["results"]}
        assert emails == {admin_user.email, user1.email, user2.email}

    def test_list_users_forbidden(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )


@pytest.mark.django_db
class TestUserProfileUpdateView:
    def test_update_profile_success(self, api_client, common_data):
        _, user, _, _, other_city, _ = common_data
        api_client.force_authenticate(user=user)

        payload = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": "password123",
            "phone_number": user.phone_number,
            "city": other_city.id,
        }
        response = api_client.put("/api/users/profile/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["city"] == other_city.id

    def test_update_profile_unauthenticated(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        payload = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": "password123",
            "phone_number": user.phone_number,
            "city": user.city.id,
        }
        response = api_client.put("/api/users/profile/", payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


@pytest.mark.django_db
class TestUserPasswordUpdateView:
    def test_update_password_success(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        user.set_password("password")
        user.save()
        api_client.force_authenticate(user=user)
        payload = {
            "old_password": "password",
            "new_password": "newPassword",
            "confirm_password": "newPassword",
        }
        response = api_client.put(
            "/api/users/profile/password/", payload, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"message": "Password updated successfully"}

    def test_update_password_wrong_old_password(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        user.set_password("password")
        user.save()
        api_client.force_authenticate(user=user)
        payload = {
            "old_password": "wrong_password",
            "new_password": "newPassword",
            "confirm_password": "newPassword",
        }
        response = api_client.put(
            "/api/users/profile/password/", payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "old_password": [
                "Your old password was entered incorrectly. Please enter it again."
            ]
        }

    def test_update_password_mismatched_confirmation(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        user.set_password("password")
        user.save()
        api_client.force_authenticate(user=user)
        payload = {
            "old_password": "password",
            "new_password": "newPassword",
            "confirm_password": "mismatch",
        }
        response = api_client.put(
            "/api/users/profile/password/", payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"non_field_errors": ["New passwords do not match"]}


@pytest.mark.django_db
class TestDeleteUserView:
    def test_delete_user_success(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        user.set_password("password")
        user.save()
        api_client.force_authenticate(user=user)
        response = api_client.delete(
            "/api/users/profile/", data={"password": "password"}, format="json"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_wrong_password(self, api_client, common_data):
        _, user, _, _, _, _ = common_data
        user.set_password("password")
        user.save()
        api_client.force_authenticate(user=user)
        response = api_client.delete(
            "/api/users/profile/", data={"password": "wrong"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
