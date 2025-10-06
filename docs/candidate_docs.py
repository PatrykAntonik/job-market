"""
Documentation for Candidate API Endpoints
"""

from drf_spectacular.utils import extend_schema

from JobApp.serializers import (
    CandidateEducationCreateSerializer,
    CandidateEducationSerializer,
    CandidateExperienceCreateSerializer,
    CandidateExperienceSerializer,
    CandidateRegistrationSerializer,
    CandidateSerializer,
    CandidateSkillCreateSerializer,
    CandidateSkillSerializer,
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

candidate_profile_docs = extend_schema(
    summary="Manage candidate profile",
    description="Allows an authenticated candidate to view and update their own profile.",
    responses={
        200: CandidateSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Candidates"],
)

candidate_skill_profile_docs = extend_schema(
    summary="List authenticated candidate's skills",
    description="Returns a list of skills for the authenticated candidate.",
    request=CandidateSkillCreateSerializer,
    responses={200: CandidateSkillSerializer(many=True)},
    tags=["Candidates"],
)

candidate_education_profile_docs = extend_schema(
    summary="List authenticated candidate's educations",
    description="Returns a list of educations for the authenticated candidate.",
    request=CandidateEducationCreateSerializer,
    responses={200: CandidateEducationSerializer(many=True)},
    tags=["Candidates"],
)

candidate_experience_profile_docs = extend_schema(
    summary="List authenticated candidate's experiences",
    description="Returns a list of experiences for the authenticated candidate.",
    request=CandidateExperienceCreateSerializer,
    responses={200: CandidateExperienceSerializer(many=True)},
    tags=["Candidates"],
)

candidate_experience_detail_docs = extend_schema(
    summary="Manage authenticated candidate's experience",
    description="Allows an authenticated candidate to view, update and delete their own experience.",
    responses={
        200: CandidateExperienceSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Candidates"],
)

candidate_education_detail_docs = extend_schema(
    summary="Manage authenticated candidate's education",
    description="Allows an authenticated candidate to view, update and delete their own education.",
    responses={
        200: CandidateEducationSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Candidates"],
)

candidate_skill_detail_docs = extend_schema(
    summary="Manage authenticated candidate's skill",
    description="Allows an authenticated candidate to view, update and delete their own skill.",
    responses={
        200: CandidateSkillSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Candidates"],
)
