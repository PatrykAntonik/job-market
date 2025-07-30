import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from JobApp.views.employer_views import *
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_skills():
    client = APIClient()
    skill1 = Skill.objects.create(name='Python')
    skill2 = Skill.objects.create(name='')
    response = client.get('/api/jobs/skills/')
    expected_data = [
        {
            'id': skill1.id,
            'name': skill1.name
        },
        {
            'id': skill2.id,
            'name': skill2.name
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_contract_types():
    client = APIClient()
    contract_type1 = ContractType.objects.create(name='Full-time')
    contract_type2 = ContractType.objects.create(name='part-time')
    response = client.get('/api/jobs/contract_types/')
    expected_data = [
        {
            'id': contract_type1.id,
            'name': contract_type1.name
        },
        {
            'id': contract_type2.id,
            'name': contract_type2.name
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_remoteness_levels():
    client = APIClient()
    remoteness_level1 = RemotenessLevel.objects.create(name='On-site')
    remoteness_level2 = RemotenessLevel.objects.create(name='Remote')
    response = client.get('/api/jobs/remoteness_levels/')
    expected_data = [
        {
            'id': remoteness_level1.id,
            'name': remoteness_level1.name
        },
        {
            'id': remoteness_level2.id,
            'name': remoteness_level2.name
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_seniority():
    client = APIClient()
    seniority1 = Seniority.objects.create(name='Junior')
    seniority2 = Seniority.objects.create(name='Senior')
    response = client.get('/api/jobs/seniority/')
    expected_data = [
        {
            'id': seniority1.id,
            'name': seniority1.name
        },
        {
            'id': seniority2.id,
            'name': seniority2.name
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_job_offers():
    client = APIClient()
    industry = Industry.objects.create(name='IT')
    country = Country.objects.create(name='Poland')
    city = City.objects.create(name='Warsaw', country=country)
    remoteness = RemotenessLevel.objects.create(name='On-site')
    contract = ContractType.objects.create(name='B2B')
    seniority = Seniority.objects.create(name='Junior')
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
        phone_number='123456789',
        is_employer=True,
        city=city,
    )
    employer1 = Employer.objects.create(
        user=user1,
        company_name='company1',
        industry=industry,
        website_url='https://www.company1.com',
        description='description1'
    )
    employer2 = Employer.objects.create(
        user=user2,
        company_name='company2',
        industry=industry,
        website_url='https://www.company2.com',
        description='description1'
    )
    employer1_location = EmployerLocation.objects.create(
        employer=employer1,
        city=city
    )
    employer2_location = EmployerLocation.objects.create(
        employer=employer2,
        city=city
    )
    job_offer_1 = JobOffer.objects.create(
        employer=employer1,
        description='description1',
        location=employer1_location,
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='position1',
        wage=1000,
        currency='USD',
    )
    job_offer_2 = JobOffer.objects.create(
        employer=employer2,
        description='description1',
        location=employer2_location,
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='position1',
        wage=1000,
        currency='USD',
    )
    response = client.get('/api/jobs/')
    expected_data = [
        {
            'id': job_offer_1.id,
            'employer': {
                'id': employer1.id,
                'user': {
                    'id': user1.id,
                    'first_name': user1.first_name,
                    'last_name': user1.last_name,
                    'email': user1.email,
                    'city': user1.city.id,
                    'phone_number': user1.phone_number,
                    'is_employer': user1.is_employer,
                    'is_candidate': user1.is_candidate,
                },
                'company_name': employer1.company_name,
                'website_url': employer1.website_url,
                'industry': {
                    'id': industry.id,
                    'name': industry.name,
                },
                'description': employer1.description,
                'benefits': []
            },
            'remoteness': {
                'id': job_offer_1.remoteness.id,
                'name': job_offer_1.remoteness.name,
            },
            'seniority': {
                'id': job_offer_1.seniority.id,
                'name': job_offer_1.seniority.name,
            },
            'skills': [],
            'description': job_offer_1.description,
            'position': job_offer_1.position,
            'wage': job_offer_1.wage,
            'currency': job_offer_1.currency,
            'location': employer1_location.id,
            'contract': contract.id,
        },
        {
            'id': job_offer_2.id,
            'employer': {
                'id': employer2.id,
                'user': {
                    'id': user2.id,
                    'first_name': user2.first_name,
                    'last_name': user2.last_name,
                    'email': user2.email,
                    'city': user2.city.id,
                    'phone_number': user2.phone_number,
                    'is_employer': user2.is_employer,
                    'is_candidate': user2.is_candidate,
                },
                'company_name': employer2.company_name,
                'website_url': employer2.website_url,
                'industry': {
                    'id': industry.id,
                    'name': industry.name,
                },
                'description': employer2.description,
                'benefits': []
            },
            'remoteness': {
                'id': job_offer_2.remoteness.id,
                'name': job_offer_2.remoteness.name,
            },
            'seniority': {
                'id': job_offer_2.seniority.id,
                'name': job_offer_2.seniority.name,
            },
            'skills': [],
            'description': job_offer_2.description,
            'position': job_offer_2.position,
            'wage': job_offer_2.wage,
            'currency': job_offer_2.currency,
            'location': employer2_location.id,
            'contract': contract.id,
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_job_offer_success():
    client = APIClient()
    industry = Industry.objects.create(name='IT')
    country = Country.objects.create(name='Poland')
    city = City.objects.create(name='Warsaw', country=country)
    remoteness = RemotenessLevel.objects.create(name='On-site')
    contract = ContractType.objects.create(name='B2B')
    seniority = Seniority.objects.create(name='Junior')
    user1 = User.objects.create_user(
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    employer1 = Employer.objects.create(
        user=user1,
        company_name='company1',
        industry=industry,
        website_url='https://www.company1.com',
        description='description1'
    )
    employer1_location = EmployerLocation.objects.create(
        employer=employer1,
        city=city
    )
    job_offer_1 = JobOffer.objects.create(
        employer=employer1,
        description='description1',
        location=employer1_location,
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='position1',
        wage=1000,
        currency='USD',
    )
    skill1 = Skill.objects.create(name='Python')
    skill2 = Skill.objects.create(name='Java')
    job_offer_1.skills.add(skill1)
    job_offer_1.skills.add(skill2)
    response = client.get(f'/api/jobs/{job_offer_1.id}/')
    expected_data = {
        'id': job_offer_1.id,
        'employer': {
            'id': employer1.id,
            'user': {
                'id': user1.id,
                'first_name': user1.first_name,
                'last_name': user1.last_name,
                'email': user1.email,
                'city': user1.city.id,
                'phone_number': user1.phone_number,
                'is_employer': user1.is_employer,
                'is_candidate': user1.is_candidate,
            },
            'company_name': employer1.company_name,
            'website_url': employer1.website_url,
            'industry': {
                'id': industry.id,
                'name': industry.name,
            },
            'description': employer1.description,
            'benefits': []
        },
        'remoteness': {
            'id': job_offer_1.remoteness.id,
            'name': job_offer_1.remoteness.name,
        },
        'seniority': {
            'id': job_offer_1.seniority.id,
            'name': job_offer_1.seniority.name,
        },
        'skills': [
            {
                'id': skill1.id,
                'name': skill1.name
            },
            {
                'id': skill2.id,
                'name': skill2.name
            },
        ],
        'description': job_offer_1.description,
        'position': job_offer_1.position,
        'wage': job_offer_1.wage,
        'currency': job_offer_1.currency,
        'location': employer1_location.id,
        'contract': contract.id,
    }
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_job_offer_not_found():
    client = APIClient()
    response = client.get('/api/jobs/1/')
    expected_data = {'message': 'Job offer not found'}
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status 404, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_employer_job_offers_success():
    client = APIClient()
    industry = Industry.objects.create(name='IT')
    country = Country.objects.create(name='Poland')
    city = City.objects.create(name='Warsaw', country=country)
    remoteness = RemotenessLevel.objects.create(name='On-site')
    contract = ContractType.objects.create(name='B2B')
    seniority = Seniority.objects.create(name='Junior')
    user1 = User.objects.create_user(
        email='test@gmail.com',
        password='<PASSWORD>',
        phone_number='1234567890',
        is_employer=True,
        city=city,
    )
    employer1 = Employer.objects.create(
        user=user1,
        company_name='company1',
        industry=industry,
        website_url='https://www.company1.com',
        description='description1'
    )
    employer1_location = EmployerLocation.objects.create(
        employer=employer1,
        city=city
    )
    job_offer_1 = JobOffer.objects.create(
        employer=employer1,
        description='description1',
        location=employer1_location,
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='position1',
        wage=1000,
        currency='USD',
    )
    job_offer_2 = JobOffer.objects.create(
        employer=employer1,
        description='description2',
        location=employer1_location,
        remoteness=remoteness,
        contract=contract,
        seniority=seniority,
        position='position2',
        wage=1000,
        currency='USD',
    )
    response = client.get(f'/api/jobs/employer/{employer1.id}/')
    expected_data = [
        {
            'id': job_offer_1.id,
            'employer': {
                'id': employer1.id,
                'user': {
                    'id': user1.id,
                    'first_name': user1.first_name,
                    'last_name': user1.last_name,
                    'email': user1.email,
                    'city': user1.city.id,
                    'phone_number': user1.phone_number,
                    'is_employer': user1.is_employer,
                    'is_candidate': user1.is_candidate,
                },
                'company_name': employer1.company_name,
                'website_url': employer1.website_url,
                'industry': {
                    'id': industry.id,
                    'name': industry.name,
                },
                'description': employer1.description,
                'benefits': []
            },
            'remoteness': {
                'id': job_offer_1.remoteness.id,
                'name': job_offer_1.remoteness.name,
            },
            'seniority': {
                'id': job_offer_1.seniority.id,
                'name': job_offer_1.seniority.name,
            },
            'skills': [],
            'description': job_offer_1.description,
            'position': job_offer_1.position,
            'wage': job_offer_1.wage,
            'currency': job_offer_1.currency,
            'location': employer1_location.id,
            'contract': contract.id,
        },
        {
            'id': job_offer_2.id,
            'employer': {
                'id': employer1.id,
                'user': {
                    'id': user1.id,
                    'first_name': user1.first_name,
                    'last_name': user1.last_name,
                    'email': user1.email,
                    'city': user1.city.id,
                    'phone_number': user1.phone_number,
                    'is_employer': user1.is_employer,
                    'is_candidate': user1.is_candidate,
                },
                'company_name': employer1.company_name,
                'website_url': employer1.website_url,
                'industry': {
                    'id': industry.id,
                    'name': industry.name,
                },
                'description': employer1.description,
            'benefits': []
            },
            'remoteness': {
                'id': job_offer_2.remoteness.id,
                'name': job_offer_2.remoteness.name,
            },
            'seniority': {
                'id': job_offer_2.seniority.id,
                'name': job_offer_2.seniority.name,
            },
            'skills': [],
            'description': job_offer_2.description,
            'position': job_offer_2.position,
            'wage': job_offer_2.wage,
            'currency': job_offer_2.currency,
            'location': employer1_location.id,
            'contract': contract.id,
        },
    ]
    assert response.status_code == HTTP_200_OK, f'Expected status 200, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_employer_job_offers_not_found():
    client = APIClient()
    response = client.get('/api/jobs/employer/1/')
    expected_data = {'message': 'Employer not found'}
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status 404, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'


@pytest.mark.django_db
def test_get_employer_job_offers_non_existent_employer():
    client = APIClient()
    response = client.get('/api/jobs/employer/1/')
    expected_data = {'message': 'Employer not found'}
    assert response.status_code == HTTP_404_NOT_FOUND, f'Expected status 404, but got {response.status_code}'
    assert response.data == expected_data, f'Expected {expected_data}, but got {response.data}'
