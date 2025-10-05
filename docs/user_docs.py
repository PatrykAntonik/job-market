"""
Documentation for User API Endpoints
"""

from drf_spectacular.utils import extend_schema

from JobApp.serializers import (
    CitySerializer,
    CountrySerializer,
    UpdateUserPasswordSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserSerializerToken,
)


user_list_docs = extend_schema(
    summary="List all users",
    description="Returns a list of all users. Only accessible by admin users.",
    responses={200: UserSerializer(many=True)},
    tags=["Users"],
)

user_profile_docs = extend_schema(
    summary="Get, update or delete user profile",
    description="Allows authenticated users to retrieve, update or delete their profile information.",
    responses={
        200: UserSerializer,
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        204: {"description": "User profile deleted successfully"},
    },
    tags=["Users"],
)

register_user_docs = extend_schema(
    summary="Register a new user",
    description="Creates a new user account.",
    request=UserRegistrationSerializer,
    responses={201: UserSerializerToken, 400: {"description": "Bad request"}},
    tags=["Users"],
)

user_detail_docs = extend_schema(
    summary="Get user details",
    description="Returns the details of a specific user. Only accessible by admin users.",
    responses={200: UserSerializer},
    tags=["Users"],
)

update_user_password_docs = extend_schema(
    summary="Update user password",
    description="Allows authenticated users to update their password.",
    request=UpdateUserPasswordSerializer,
    responses={
        200: {"description": "Password updated successfully"},
        400: {"description": "Bad request"},
    },
    tags=["Users"],
)

token_obtain_pair_docs = extend_schema(
    summary="Obtain JWT token",
    description="Obtain JWT token by providing user credentials.",
    responses={200: UserSerializerToken},
    tags=["Users"],
)

token_obtain_pair_docs = extend_schema(
    summary="Obtain JWT token",
    description="Obtain JWT token by providing user credentials.",
    responses={200: UserSerializerToken},
    tags=["Users"],
)

country_list_docs = extend_schema(
    summary="List all countries",
    description="Returns a list of all countries.",
    responses={200: CountrySerializer(many=True)},
    tags=["Locations"],
)

country_detail_docs = extend_schema(
    summary="Get, update or delete a country",
    description="Allows admin users to retrieve, update or delete a country.",
    responses={200: CountrySerializer},
    tags=["Locations"],
)

city_list_docs = extend_schema(
    summary="List all cities",
    description="Returns a list of all cities.",
    responses={200: CitySerializer(many=True)},
    tags=["Locations"],
)

city_detail_docs = extend_schema(
    summary="Get, update or delete a city",
    description="Allows admin users to retrieve, update or delete a city.",
    responses={200: CitySerializer},
    tags=["Locations"],
)
