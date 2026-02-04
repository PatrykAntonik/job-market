"""
Documentation for Job API Endpoints
"""

from drf_spectacular.utils import extend_schema

from JobApp.serializers import (
    ChoiceSerializer,
    IndustrySerializer,
    JobOfferCreateSerializer,
    JobOfferSerializer,
    JobOfferUpdateSerializer,
    OfferResponseSerializer,
    SkillSerializer,
)


skill_list_docs = extend_schema(
    summary="List all skills",
    description="Returns a list of all skills.",
    responses={200: SkillSerializer(many=True)},
    tags=["Jobs"],
)

industry_list_docs = extend_schema(
    summary="List all industries",
    description="Returns a list of all industries.",
    responses={200: IndustrySerializer(many=True)},
    tags=["Jobs"],
)

job_offer_list_docs = extend_schema(
    summary="List all job offers",
    description="Returns a list of all job offers.",
    responses={200: JobOfferSerializer(many=True)},
    tags=["Jobs"],
)

seniority_list_docs = extend_schema(
    summary="List all seniority levels",
    description="Returns a list of all seniority levels.",
    responses={200: ChoiceSerializer(many=True)},
    tags=["Jobs"],
)

contract_type_list_docs = extend_schema(
    summary="List all contract types",
    description="Returns a list of all contract types.",
    responses={200: ChoiceSerializer(many=True)},
    tags=["Jobs"],
)

remoteness_level_list_docs = extend_schema(
    summary="List all remoteness levels",
    description="Returns a list of all remoteness levels.",
    responses={200: ChoiceSerializer(many=True)},
    tags=["Jobs"],
)

job_offer_detail_docs = extend_schema(
    summary="Get job offer details",
    description="Returns the details of a specific job offer.",
    responses={200: JobOfferSerializer},
    tags=["Jobs"],
)

job_offer_list_profile_docs = extend_schema(
    summary="List authenticated employer's job offers",
    description="Returns a list of job offers for the authenticated employer.",
    request=JobOfferCreateSerializer,
    responses={200: JobOfferSerializer(many=True)},
    tags=["Jobs"],
)

job_offer_profile_detail_docs = extend_schema(
    summary="Manage authenticated employer's job offer",
    description="Allows an authenticated employer to view, update and delete their own job offer.",
    request=JobOfferUpdateSerializer,
    responses={
        200: JobOfferSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Jobs"],
)

employer_job_offer_list_docs = extend_schema(
    summary="List all job offers for a specific employer",
    description="Returns a list of all job offers for a specific employer.",
    responses={200: JobOfferSerializer(many=True)},
    tags=["Jobs"],
)

apply_to_job_offer_docs = extend_schema(
    summary="Apply to a job offer",
    description="Creates an application (OfferResponse) for the authenticated candidate.",
    responses={
        201: OfferResponseSerializer,
        400: {"description": "Bad request / already applied"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden (candidates only)"},
        404: {"description": "Job offer not found"},
    },
    tags=["Jobs"],
)

job_offer_applicants_docs = extend_schema(
    summary="List applicants for an employer job offer",
    description="Returns applications (OfferResponse) for the authenticated employer's job offer.",
    responses={
        200: OfferResponseSerializer(many=True),
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden (employers only)"},
        404: {"description": "Job offer not found"},
    },
    tags=["Jobs"],
)
