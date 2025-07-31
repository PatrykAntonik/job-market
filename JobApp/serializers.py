from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'city', 'phone_number']
        # fields = '__all__'


class UserSerializerToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'refresh', 'access']

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'resume', 'about']


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        # fields = ['id', 'name']
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # fields = ['id', 'name', 'country', 'province', 'zip_code']
        fields = '__all__'


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'


class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    benefits = BenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'user', 'company_name', 'website_url', 'industry', 'description', 'benefits']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        # fields = ['id', 'name']
        fields = '__all__'


class CandidateSkillSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CandidateSkill
        # fields = ['id', 'candidate', 'skill']
        fields = '__all__'


class JobOfferSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOffer
        # fields = ['id', 'employer', 'description', 'city', 'remoteness', 'seniority', 'position',
        #          'wage', 'currency', 'skills', 'contract_type']
        fields = '__all__'


class JobOfferSkillSerializer(serializers.ModelSerializer):
    offer = JobOfferSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = JobOfferSkill
        # fields = ['id', 'offer', 'skill']
        fields = '__all__'


class CandidateExperienceSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateExperience
        # fields = ['id', 'candidate', 'company_name', 'job_position', 'date_from', 'date_to', 'description',
        #         'is_current']
        fields = '__all__'


class CandidateEducationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateEducation
        # fields = ['id', 'candidate', 'school_name', 'field_of_study', 'degree']
        fields = '__all__'


class OfferResponseSerializer(serializers.ModelSerializer):
    offer = JobOfferSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = OfferResponse
        # fields = ['id', 'offer', 'candidate']
        fields = '__all__'


class EmployerLocationSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)

    class Meta:
        model = EmployerLocation
        # fields = ['id', 'employer', 'city']
        fields = '__all__'
