from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Benefit,
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
    City,
    Country,
    Employer,
    EmployerBenefit,
    EmployerLocation,
    Industry,
    JobOffer,
    JobOfferSkill,
    OfferResponse,
    Skill,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "city", "phone_number"]
        # fields = '__all__'


class UserSerializerToken(UserSerializer):
    """
    Serializer for the User model, including access and refresh tokens.
    """

    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "refresh", "access"]

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "city",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        return UserSerializerToken(instance).data


class EmployerRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for employer registration.
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())
    description = serializers.CharField(required=False)
    website_url = serializers.CharField(required=False)

    class Meta:
        model = Employer
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "city",
            "company_name",
            "website_url",
            "industry",
            "description",
        ]

    def validate(self, data):
        errors = {}
        email = data.get("email")
        phone_number = data.get("phone_number")
        website_url = data.get("website_url")

        if User.objects.filter(email=email).exists():
            errors["email"] = "User with this email already exists."

        if User.objects.filter(phone_number=phone_number).exists():
            errors["phone_number"] = "User with this phone number already exists."

        if website_url and Employer.objects.filter(website_url=website_url).exists():
            errors["website_url"] = "Employer with this website URL already exists."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            phone_number=validated_data.pop("phone_number"),
            city=validated_data.pop("city"),
        )
        employer = Employer.objects.create(user=user, **validated_data)
        return employer

    def to_representation(self, instance):
        data = EmployerSerializer(instance, context=self.context).data
        tokens = RefreshToken.for_user(instance.user)
        data["refresh"] = str(tokens)
        data["access"] = str(tokens.access_token)
        return data


class CandidateRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for candidate registration.
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Candidate
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "city",
            "resume",
            "about",
        ]

    def validate_resume(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("Resume must be a PDF file")
        return value

    def validate(self, data):
        errors = {}
        email = data.get("email")
        phone_number = data.get("phone_number")

        if User.objects.filter(email=email).exists():
            errors["email"] = "User with this email already exists."

        if User.objects.filter(phone_number=phone_number).exists():
            errors["phone_number"] = "User with this phone number already exists."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            phone_number=validated_data.pop("phone_number"),
            city=validated_data.pop("city"),
        )
        candidate = Candidate.objects.create(user=user, **validated_data)
        return candidate

    def to_representation(self, instance):
        data = CandidateSerializer(instance, context=self.context).data
        tokens = RefreshToken.for_user(instance.user)
        data["refresh"] = str(tokens)
        data["access"] = str(tokens.access_token)
        return data


class CandidateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Candidate model.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "user", "resume", "about"]


class CandidateSerializerWithTotalExp(serializers.ModelSerializer):
    """
    Serializer for the Candidate model, including total experience.
    """

    user = UserSerializer(read_only=True)
    total_experience = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "user", "resume", "about", "total_experience"]

    def get_total_experience(self, obj):
        days = obj.total_experience_days.days if obj.total_experience_days else 0
        years = days / 365.25
        return round(years * 2) / 2


class CandidateSimlifiedSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for the Candidate model.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "user"]


class IndustrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Industry model.
    """

    class Meta:
        model = Industry
        fields = ["id", "name"]


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Country model.
    """

    class Meta:
        model = Country
        # fields = ['id', 'name']
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for the City model.
    """

    class Meta:
        model = City
        # fields = ['id', 'name', 'country', 'province', 'zip_code']
        fields = "__all__"


class BenefitSerializer(serializers.ModelSerializer):
    """
    Serializer for the Benefit model.
    """

    class Meta:
        model = Benefit
        fields = "__all__"


class EmployerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employer model.
    """

    user = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = Employer
        fields = [
            "id",
            "user",
            "company_name",
            "website_url",
            "industry",
            "description",
        ]


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for the Skill model.
    """

    class Meta:
        model = Skill
        # fields = ['id', 'name']
        fields = "__all__"


class CandidateSkillSerializer(serializers.ModelSerializer):
    """
    Serializer for the CandidateSkill model.
    """

    candidate = CandidateSimlifiedSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CandidateSkill
        fields = ["id", "skill", "candidate"]


class CandidateSkillCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating CandidateSkill instances.
    """

    class Meta:
        model = CandidateSkill
        fields = ["skill"]


class JobOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobOffer model.
    """

    employer = EmployerSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOffer
        # fields = ['id', 'employer', 'description', 'city', 'remoteness', 'seniority', 'position',
        #          'wage', 'currency', 'skills', 'contract_type']
        fields = "__all__"


class JobOfferSkillSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobOfferSkill model.
    """

    offer = JobOfferSerializer(read_only=True)
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = JobOfferSkill
        # fields = ['id', 'offer', 'skill']
        fields = "__all__"


class CandidateExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for the CandidateExperience model.
    """

    candidate = CandidateSimlifiedSerializer(read_only=True)

    class Meta:
        model = CandidateExperience
        fields = "__all__"


class CandidateExperienceCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating CandidateExperience instances.
    """

    class Meta:
        model = CandidateExperience
        exclude = ["candidate"]


class CandidateEducationSerializer(serializers.ModelSerializer):
    """
    Serializer for the CandidateEducation model.
    """

    candidate = CandidateSimlifiedSerializer(read_only=True)

    class Meta:
        model = CandidateEducation
        fields = "__all__"


class CandidateEducationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating CandidateEducation instances.
    """

    class Meta:
        model = CandidateEducation
        exclude = ["candidate"]


class OfferResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferResponse model.
    """

    offer = JobOfferSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = OfferResponse
        # fields = ['id', 'offer', 'candidate']
        fields = "__all__"


class EmployerLocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmployerLocation model.
    """

    employer = EmployerSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = EmployerLocation
        fields = "__all__"


class EmployerLocationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating EmployerLocation instances.
    """

    class Meta:
        model = EmployerLocation
        fields = ["city"]


class EmployerBenefitSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmployerBenefit model.
    """

    benefit = BenefitSerializer(read_only=True)

    class Meta:
        model = EmployerBenefit
        fields = ["id", "benefit"]


class EmployerBenefitCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating EmployerBenefit instances.
    """

    class Meta:
        model = EmployerBenefit
        fields = ["benefit"]


class UpdateUserPasswordSerializer(serializers.Serializer):
    """
    Serializer for updating user password.
    """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                "Your old password was entered incorrectly. Please enter it again."
            )
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User profile.
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "city"]


class CandidateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Candidate profile.
    """

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=False
    )

    class Meta:
        model = Candidate
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "resume",
            "about",
        ]

    def to_representation(self, instance):
        return CandidateSerializer(instance).data
