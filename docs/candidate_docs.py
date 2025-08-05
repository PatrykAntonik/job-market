from drf_spectacular.utils import extend_schema
from JobApp.serializers import (
    CandidateSerializer,
    CandidateSkillSerializer,
    CandidateExperienceSerializer,
    CandidateEducationSerializer,
    CandidateRegistrationSerializer,
)

register_candidate_docs = extend_schema(
    summary="Register a new candidate",
    description="Creates a new candidate account.",
    request=CandidateRegistrationSerializer,
    responses={
        201: CandidateRegistrationSerializer,
        400: {"description": "Bad request"},
    },
    tags=["Candidates"],
)

candidate_list_docs = extend_schema(
    summary="List all candidates",
    description="Returns a list of all candidates. Only accessible by employers.",
    responses={200: CandidateSerializer(many=True)},
    tags=["Candidates"],
)

candidate_detail_docs = extend_schema(
    summary="Get candidate details",
    description="Returns the details of a specific candidate. Only accessible by employers.",
    responses={200: CandidateSerializer},
    tags=["Candidates"],
)

candidate_skill_list_docs = extend_schema(
    summary="List candidate skills",
    description="Returns a list of skills for a specific candidate. Only accessible by employers.",
    responses={200: CandidateSkillSerializer(many=True)},
    tags=["Candidates"],
)

candidate_experience_list_docs = extend_schema(
    summary="List candidate experiences",
    description="Returns a list of experiences for a specific candidate. Only accessible by employers.",
    responses={200: CandidateExperienceSerializer(many=True)},
    tags=["Candidates"],
)

candidate_education_list_docs = extend_schema(
    summary="List candidate educations",
    description="Returns a list of educations for a specific candidate. Only accessible by employers.",
    responses={200: CandidateEducationSerializer(many=True)},
    tags=["Candidates"],
)
