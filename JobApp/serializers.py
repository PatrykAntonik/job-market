from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'city', 'phone_number', 'is_employer', 'is_candidate']
        # fields = '__all__'

    def get_id(self, obj):
        return obj.id


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
    id = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'resume', 'about']

    def get_id(self, obj):
        return obj.id


class IndustrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Industry
        fields = ['id', 'name']

    def get_id(self, obj):
        return obj.id


class CountrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        # fields = ['id', 'name']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class CitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        # fields = ['id', 'name', 'country', 'province', 'zip_code']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class EmployerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'user', 'company_name', 'website_url', 'industry', 'description']

    def get_id(self, obj):
        return obj.id


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Skill
        # fields = ['id', 'name']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class CandidateSkillSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    candidate = CandidateSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CandidateSkill
        # fields = ['id', 'candidate', 'skill']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class ContractTypeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContractType
        # fields = ['id', 'name']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class RemotenessLevelSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RemotenessLevel
        # fields = ['id', 'remote_type']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class SenioritySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Seniority
        # fields = ['id', 'seniority_level']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class JobOfferSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    employer = EmployerSerializer(read_only=True)
    contract_type = ContractTypeSerializer(read_only=True)
    remoteness = RemotenessLevelSerializer(read_only=True)
    seniority = SenioritySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOffer
        # fields = ['id', 'employer', 'description', 'city', 'remoteness', 'seniority', 'position',
        #          'wage', 'currency', 'skills', 'contract_type']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class JobOfferSkillSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    offer = JobOfferSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = JobOfferSkill
        # fields = ['id', 'offer', 'skill']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class CandidateExperienceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateExperience
        # fields = ['id', 'candidate', 'company_name', 'job_position', 'date_from', 'date_to', 'description',
        #         'is_current']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class CandidateEducationSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateEducation
        # fields = ['id', 'candidate', 'school_name', 'field_of_study', 'degree']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class OfferResponseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    offer = JobOfferSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = OfferResponse
        # fields = ['id', 'offer', 'candidate']
        fields = '__all__'

    @staticmethod
    def get_id(obj):
        return obj.id


class EmployerBenefitSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    employer = EmployerSerializer(read_only=True)

    class Meta:
        model = EmployerBenefit
        # fields = ['id', 'employer', 'benefit_name']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id


class EmployerLocationSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    employer = EmployerSerializer(read_only=True)

    class Meta:
        model = EmployerLocation
        # fields = ['id', 'employer', 'city']
        fields = '__all__'

    def get_id(self, obj):
        return obj.id
