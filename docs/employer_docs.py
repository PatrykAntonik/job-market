"""
Documentation for Employer API Endpoints
"""

from drf_spectacular.utils import extend_schema

from JobApp.serializers import (
    BenefitSerializer,
    EmployerBenefitCreateSerializer,
    EmployerBenefitSerializer,
    EmployerLocationCreateSerializer,
    EmployerLocationSerializer,
    EmployerRegistrationSerializer,
    EmployerSerializer,
)


benefit_list_docs = extend_schema(
    summary="List all benefits",
    description="Returns a list of all benefits.",
    responses={200: BenefitSerializer(many=True)},
    tags=["Employers"],
)


register_employer_docs = extend_schema(
    summary="Register a new employer",
    description="Creates a new employer account.",
    request=EmployerRegistrationSerializer,
    responses={
        201: EmployerRegistrationSerializer,
        400: {"description": "Bad request"},
    },
    tags=["Employers"],
)

employer_list_docs = extend_schema(
    summary="List all employers",
    description="Returns a list of all employers.",
    responses={200: EmployerSerializer(many=True)},
    tags=["Employers"],
)

employer_detail_docs = extend_schema(
    summary="Get employer details",
    description="Returns the details of a specific employer.",
    responses={200: EmployerSerializer},
    tags=["Employers"],
)

employer_profile_docs = extend_schema(
    summary="Manage employer profile",
    description="Allows an authenticated employer to view and update their own profile.",
    responses={
        200: EmployerSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Employers"],
)

employer_location_list_docs = extend_schema(
    summary="List employer locations",
    description="Returns a list of locations for a specific employer.",
    responses={200: EmployerLocationSerializer(many=True)},
    tags=["Employers"],
)

employer_location_detail_docs = extend_schema(
    summary="Manage employer location",
    description="Allows an authenticated employer to view, update and delete their own location.",
    responses={
        200: EmployerLocationSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Employers"],
)

employer_location_list_profile_docs = extend_schema(
    summary="List authenticated employer's locations",
    description="Returns a list of locations for the authenticated employer.",
    request=EmployerLocationCreateSerializer,
    responses={200: EmployerLocationSerializer(many=True)},
    tags=["Employers"],
)

employer_benefit_list_profile_docs = extend_schema(
    summary="List authenticated employer's benefits",
    description="Returns a list of benefits for the authenticated employer.",
    request=EmployerBenefitCreateSerializer,
    responses={200: EmployerBenefitSerializer(many=True)},
    tags=["Employers"],
)

employer_benefit_detail_docs = extend_schema(
    summary="Manage employer benefit",
    description="Allows an authenticated employer to view, update and delete their own benefit.",
    responses={
        200: EmployerBenefitSerializer,
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["Employers"],
)

employer_list_benefit_docs = extend_schema(
    summary="List employer benefits",
    description="Returns a list of benefits for a specific employer.",
    responses={200: EmployerBenefitSerializer(many=True)},
    tags=["Employers"],
)
