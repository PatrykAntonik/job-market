import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    user2 = User.objects.create_user(
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
            },
        },
    ]

    assert response.status_code == HTTP_200_OK, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidates_without_permission():
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
    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    client.force_authenticate(user=user)
    response = client.get(f'/api/candidates/')
    expected_data = {'detail': 'Access restricted to employers only'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_success():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    reponse = client.get(f'/api/candidates/{candidate.id}/')
    expected_data = {
        "id": candidate.id,
        "about": "about candidate",
        "resume": "/PDFs/" + candidate.resume.name,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "city": user.city.id,
            "phone_number": user.phone_number,
        },
    }
    assert reponse.status_code == HTTP_200_OK, f'Expected status code 200 but got {reponse.status_code}'
    assert reponse.json() == expected_data, f'Expected: {expected_data}, but got: {reponse.json()}'


@pytest.mark.django_db
def test_get_candidate_not_found():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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
    response = client.get('/api/candidates/1/')
    expected_data = {'message': 'Candidate not found'}
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status code 404 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_without_permission():
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
    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    client.force_authenticate(user=user)
    response = client.get(f'/api/candidates/{candidate.id}/')
    expected_data = {'detail': 'Access restricted to employers only'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_skills_success():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    skill = Skill.objects.create(
        name='Test Skill',
    )
    skill2 = Skill.objects.create(
        name='Test Skill2',
    )
    candidate_skill = CandidateSkill.objects.create(
        candidate=candidate,
        skill=skill,
    )
    candidate_skill2 = CandidateSkill.objects.create(
        candidate=candidate,
        skill=skill2,
    )
    response = client.get(f'/api/candidates/{candidate.id}/skills/')
    expected_data = [
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'id': 1,
            'skill':
                {
                    'id': 1, 'name': 'Test Skill'
                }
        },
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'id': 2,
            'skill':
                {
                    'id': 2, 'name': 'Test Skill2'
                }
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_skills_not_found():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    response = client.get(f'/api/candidates/{candidate.id}/skills/')
    expected_data = {
        'message': 'Candidate skills not found'
    }
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_skills_without_permission():
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
    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    client.force_authenticate(user=user)
    response = client.get(f'/api/candidates/{candidate.id}/skills/')
    expected_data = {'detail': 'Access restricted to employers only'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_experience_success():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    experience = CandidateExperience.objects.create(
        candidate=candidate,
        company_name='Test Company',
        date_from='2021-01-01',
        date_to='2022-01-01',
        is_current=False,
        job_position='Test Position',
        description='Test Description',
    )
    experience2 = CandidateExperience.objects.create(
        candidate=candidate,
        company_name='Test Company2',
        date_from='2021-01-01',
        date_to='2022-01-01',
        is_current=False,
        job_position='Test Position2',
        description='Test Description2',
    )
    response = client.get(f'/api/candidates/{candidate.id}/experience/')
    expected_data = [
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'company_name': experience.company_name,
            'date_from': experience.date_from,
            'date_to': experience.date_to,
            'description': experience.description,
            'id': experience.id,
            'is_current': experience.is_current,
            'job_position': experience.job_position
        },
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'company_name': experience2.company_name,
            'date_from': experience2.date_from,
            'date_to': experience2.date_to,
            'description': experience2.description,
            'id': experience2.id,
            'is_current': experience2.is_current,
            'job_position': experience2.job_position
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_experience_not_found():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    response = client.get(f'/api/candidates/{candidate.id}/experience/')
    expected_data = {
        'message': 'Candidate experience not found'
    }
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status code 404 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_experience_without_permission():
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
    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    client.force_authenticate(user=user)
    response = client.get(f'/api/candidates/{candidate.id}/experience/')
    expected_data = {'detail': 'Access restricted to employers only'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_education_success():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    education = CandidateEducation.objects.create(
        candidate=candidate,
        school_name='Test School',
        degree='Test Degree',
        field_of_study='Test Field',
        date_from='2021-01-01',
        date_to='2022-01-01',
        is_current=False,
    )
    education2 = CandidateEducation.objects.create(
        candidate=candidate,
        school_name='Test School2',
        degree='Test Degree',
        field_of_study='Test Field',
        date_from='2021-01-01',
        date_to='2022-01-01',
        is_current=False,
    )
    response = client.get(f'/api/candidates/{candidate.id}/education/')
    expected_data = [
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'id': education.id,
            'school_name': education.school_name,
            'degree': education.degree,
            'field_of_study': education.field_of_study,
            'date_from': education.date_from,
            'date_to': education.date_to,
            'is_current': education.is_current,
        },
        {
            'candidate':
                {
                    'about': candidate.about,
                    'id': candidate.id,
                    'resume': f'/PDFs/{candidate.resume.name}',
                    'user':
                        {
                            'city': city.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'id': user.id,
                            'last_name': user.last_name,
                            'phone_number': user.phone_number
                        }
                },
            'id': education2.id,
            'school_name': education2.school_name,
            'degree': education2.degree,
            'field_of_study': education2.field_of_study,
            'date_from': education2.date_from,
            'date_to': education2.date_to,
            'is_current': education2.is_current,
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_education_not_found():
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
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
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

    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    response = client.get(f'/api/candidates/{candidate.id}/education/')
    expected_data = {
        'message': 'Candidate education not found'
    }
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status code 200 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'


@pytest.mark.django_db
def test_get_candidate_education_without_permission():
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
    user = User.objects.create_user(
        email='test1@gmail.com',
        password='<PASSWORD>',
        phone_number='123456789',
        is_candidate=True,
        city=city,
    )
    candidate = Candidate.objects.create(
        user=user,
        about='about candidate',
        resume=SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
    )
    client.force_authenticate(user=user)
    response = client.get(f'/api/candidates/{candidate.id}/education/')
    expected_data = {'detail': 'Access restricted to employers only'}
    assert response.status_code == HTTP_403_FORBIDDEN, f'Expected status code 403 but got {response.status_code}'
    assert response.json() == expected_data, f'Expected: {expected_data}, but got: {response.json()}'
