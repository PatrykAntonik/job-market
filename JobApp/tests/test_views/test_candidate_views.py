import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from JobApp.views.employer_views import *
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_candidates_success():
    client = APIClient()
    country = Country.objects.create(
        name='Test Country',
    )
    city = City.objects.create(
        name='Test City',
        country=country,
        province='Test Province',
        zip_code='12345'
    )
    employer_user = User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    industry = Industry.objects.create(
        name='Test Industry',
    )
    employer = Employer.objects.create(
        user=employer_user,
        company_name='Test Employer',
        website_url='www.test.com',
        description='Test employer',
        industry=industry
    )
    client.force_authenticate(user=employer_user)
    user1 = User.objects.create_user(
        username='testuser1',
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    user2 = User.objects.create_user(
        username='testuser2',
        email='test2@gmail.com',
        password='<PASSWORD>',
        phone_number='012345678900',
        is_candidate=True,
        city=city,
    )
    candidate1 = Candidate.objects.create(
        user=user1,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    candidate2 = Candidate.objects.create(
        user=user2,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    response = client.get('/api/candidates/')
    expected_data = [
        {
            "id": candidate1.id,
            "about": "about candidate",
            "resume": "/PDFs/" + candidate1.resume.name,
            "user": {
                "id": user1.id,
                "first_name": user1.first_name,
                "last_name": user1.last_name,
                "email": user1.email,
                "city": user1.city.id,
                "phone_number": user1.phone_number,
                "is_employer": user1.is_employer,
                "is_candidate": user1.is_candidate,
            },
        },
        {
            "id": candidate2.id,
            "about": "about candidate",
            "resume": "/PDFs/" + candidate2.resume.name,
            "user": {
                "id": user2.id,
                "first_name": user2.first_name,
                "last_name": user2.last_name,
                "email": user2.email,
                "city": user2.city.id,
                "phone_number": user2.phone_number,
                "is_employer": user2.is_employer,
                "is_candidate": user2.is_candidate,
            },
        },
    ]

    assert response.status_code == HTTP_200_OK, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'
