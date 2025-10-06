from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from JobApp.filters import UserFilter
from JobApp.models import City, Country, User
from JobApp.pagination import OptionalPagination
from JobApp.serializers import (
    CitySerializer,
    CountrySerializer,
    UpdateUserPasswordSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserSerializerToken,
)
from docs.user_docs import (
    city_detail_docs,
    city_list_docs,
    country_detail_docs,
    country_list_docs,
    register_user_docs,
    token_obtain_pair_docs,
    update_user_password_docs,
    user_detail_docs,
    user_list_docs,
    user_profile_docs,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens that includes user data in the response.
    """

    username_field = "email"

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerToken(self.user)
        data.update(serializer.data)
        return data


@token_obtain_pair_docs
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view to include user data in the response.
    """

    serializer_class = MyTokenObtainPairSerializer


@register_user_docs
class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_serializer = MyTokenObtainPairSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(serializer.data)
        return Response(
            token_serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@user_list_docs
class UserListView(generics.ListAPIView):
    """
    Retrieve a list of users with optional filtering, searching, and ordering.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilter
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = [
        "city__name",
        "city__country__name",
        "first_name",
        "last_name",
        "email",
    ]
    ordering = ["id"]
    pagination_class = OptionalPagination


@user_profile_docs
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete the authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.data.get("password")
        if not user.check_password(password):
            return Response(
                {"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@user_detail_docs
class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve a user's details.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@update_user_password_docs
class UpdateUserPasswordView(generics.UpdateAPIView):
    """
    Update the authenticated user's password.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserPasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )


@country_list_docs
class CountryListView(generics.ListAPIView):
    """
    Retrieve a list of countries.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    ordering = ["name"]
    pagination_class = OptionalPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]


@city_list_docs
class CityListView(generics.ListAPIView):
    """
    Retrieve a list of cities.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    ordering = ["name"]
    pagination_class = OptionalPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]


@country_detail_docs
class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a country.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]


@city_detail_docs
class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a city.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]
