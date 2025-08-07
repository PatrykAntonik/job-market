from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from docs.user_docs import *
from JobApp.filters import UserFilter
from JobApp.pagination import OptionalPagination
from JobApp.permissions import IsEmployer
from JobApp.serializers import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerToken(self.user)
        data.update(serializer.data)
        return data


@extend_schema(tags=["Users"])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@register_user_docs
class UserRegistrationView(generics.CreateAPIView):
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@update_user_password_docs
class UpdateUserPasswordView(generics.UpdateAPIView):
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
