from django.core.management.base import BaseCommand
from JobApp.models import *
from faker import Faker
import random


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        records_num = 50
        self.stdout.write('Populating database...')
        fake = Faker()

        self.clear_data()

        countries = []
        for _ in range(records_num):
            country = Country.objects.create(name=fake.unique.country())
            countries.append(country)
        self.stdout.write(self.style.SUCCESS(f'Created {len(countries)} countries.'))

        cities = []
        for _ in range(records_num):
            city = City.objects.create(
                name=fake.city(),
                province=fake.state(),
                zip_code=fake.postcode(),
                country=random.choice(countries)
            )
            cities.append(city)
        self.stdout.write(self.style.SUCCESS(f'Created {len(cities)} cities.'))

        industries = []
        for _ in range(records_num):
            industry = Industry.objects.create(name=fake.unique.job())
            industries.append(industry)
        self.stdout.write(self.style.SUCCESS(f'Created {len(industries)} industries.'))

        candidates = []
        for _ in range(records_num):  # Candidates
            user = User.objects.create_user(
                email=fake.unique.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.unique.phone_number(),
                city=random.choice(cities),
            )
            candidate = Candidate.objects.create(
                user=user,
                resume=f'resumes/{fake.file_name(extension="pdf")}',
                about=fake.paragraph()
            )
            candidates.append(candidate)
        self.stdout.write(self.style.SUCCESS(f'Created {len(candidates)} candidates.'))

        employers = []
        for _ in range(records_num):  # Employers
            user = User.objects.create_user(
                email=fake.unique.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.unique.phone_number(),
                city=random.choice(cities),
            )
            employer = Employer.objects.create(
                user=user,
                company_name=fake.unique.company(),
                website_url=fake.unique.url(),
                description=fake.paragraph(),
                industry=random.choice(industries)
            )
            employers.append(employer)
        self.stdout.write(self.style.SUCCESS(f'Created {len(employers)} employers.'))

        benefits = []
        for _ in range(records_num):
            benefit = Benefit.objects.create(name=fake.unique.word())
            benefits.append(benefit)
        self.stdout.write(self.style.SUCCESS(f'Created {len(benefits)} benefits.'))

        for employer in employers:
            employer.benefits.set(random.sample(benefits, k=random.randint(1, len(benefits))))
        self.stdout.write(self.style.SUCCESS(f'Assigned benefits to employers.'))

        skills = []
        for _ in range(records_num):
            skill = Skill.objects.create(name=fake.unique.word())
            skills.append(skill)
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills)} skills.'))

        candidate_skills = []
        for _ in range(records_num):
            candidate_skill = CandidateSkill.objects.create(
                candidate=random.choice(candidates),
                skill=random.choice(skills)
            )
            candidate_skills.append(candidate_skill)
        self.stdout.write(self.style.SUCCESS(f'Created {len(candidate_skills)} candidate skills.'))

        candidate_experiences = []
        for _ in range(records_num):
            start_date = fake.date_between(start_date='-5y', end_date='today')
            is_current = fake.boolean()
            end_date = None
            if not is_current:
                end_date = fake.date_between(start_date=start_date, end_date='today')

            experience = CandidateExperience.objects.create(
                candidate=random.choice(candidates),
                company_name=fake.company(),
                date_from=start_date,
                date_to=end_date,
                is_current=is_current,
                job_position=fake.job(),
                description=fake.paragraph()
            )
            candidate_experiences.append(experience)
        self.stdout.write(self.style.SUCCESS(f'Created {len(candidate_experiences)} candidate experiences.'))

        candidate_educations = []
        for _ in range(records_num):
            start_date = fake.date_between(start_date='-5y', end_date='today')
            is_current = fake.boolean()
            end_date = None
            if not is_current:
                end_date = fake.date_between(start_date=start_date, end_date='today')

            education = CandidateEducation.objects.create(
                candidate=random.choice(candidates),
                school_name=fake.word(),
                field_of_study=fake.word(),
                degree=fake.word(),
                date_from=start_date,
                date_to=end_date,
                is_current=is_current
            )
            candidate_educations.append(education)
        self.stdout.write(self.style.SUCCESS(f'Created {len(candidate_educations)} candidate educations.'))

        employer_locations = []
        for _ in range(records_num):
            employer_location = EmployerLocation.objects.create(
                employer=random.choice(employers),
                city=random.choice(cities)
            )
            employer_locations.append(employer_location)
        self.stdout.write(self.style.SUCCESS(f'Created {len(employer_locations)} employer locations.'))

        job_offers = []
        for _ in range(records_num):
            job_offer = JobOffer.objects.create(
                employer=random.choice(employers),
                description=fake.paragraph(),
                location=random.choice(employer_locations),
                remoteness=random.choice(JobOffer.RemotenessLevel.values),
                contract=random.choice(JobOffer.ContractType.values),
                seniority=random.choice(JobOffer.Seniority.values),
                position=fake.job(),
                wage=random.randint(30000, 120000),
                currency=fake.currency_code()
            )
            job_offers.append(job_offer)
        self.stdout.write(self.style.SUCCESS(f'Created {len(job_offers)} job offers.'))

        job_offer_skills = []
        for _ in range(records_num):
            job_offer_skill = JobOfferSkill.objects.create(
                offer=random.choice(job_offers),
                skill=random.choice(skills)
            )
            job_offer_skills.append(job_offer_skill)
        self.stdout.write(self.style.SUCCESS(f'Created {len(job_offer_skills)} job offer skills.'))

        offer_responses = []
        for _ in range(records_num):
            offer_response = OfferResponse.objects.create(
                offer=random.choice(job_offers),
                candidate=random.choice(candidates)
            )
            offer_responses.append(offer_response)
        self.stdout.write(self.style.SUCCESS(f'Created {len(offer_responses)} offer responses.'))

        self.stdout.write(self.style.SUCCESS('Database population complete!'))

    def clear_data(self):
        self.stdout.write('Clearing existing data...')
        OfferResponse.objects.all().delete()
        JobOfferSkill.objects.all().delete()
        JobOffer.objects.all().delete()
        EmployerLocation.objects.all().delete()
        CandidateEducation.objects.all().delete()
        CandidateExperience.objects.all().delete()
        CandidateSkill.objects.all().delete()
        Skill.objects.all().delete()
        Benefit.objects.all().delete()
        Employer.objects.all().delete()
        Industry.objects.all().delete()
        Candidate.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))