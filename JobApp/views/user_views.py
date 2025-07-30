from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from JobApp.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.db import IntegrityError
from JobApp.permissions import IsEmployer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from JobApp.pagination import OptionalPagination


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerToken(self.user)
        data.update(serializer.data)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'city__country', 'is_employer', 'is_candidate']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['city']
    pagination_class = OptionalPagination


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data
        city_data = data.get('city')
        if city_data is not None:
            if isinstance(city_data, dict):
                city_id = city_data.get('id')
            else:
                city_id = city_data
            user.city_id = city_id
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        try:
            user.save()
        except Exception as e:
            if 'UNIQUE constraint failed: JobApp_user.email' in str(e):
                return Response({'message': 'This email address is already in use by another account'}, status=400)
            elif 'UNIQUE constraint failed: JobApp_user.phone_number' in str(e):
                return Response({'message': 'This phone number is already in use by another account'}, status=400)
            else:
                return Response({'message': str(e)}, status=400)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=200)

    def delete(self, request):
        user = request.user
        old_password = request.data.get('password')
        if not user.check_password(old_password):
            return Response({'message': 'Invalid password'}, status=400)
        user.delete()
        return Response(status=204)


class RegisterUserView(APIView):
    def post(self, request):
        data = request.data
        try:
            city_data = data.get('city')
            if isinstance(city_data, dict):
                city_id = city_data.get('id')
            else:
                city_id = city_data
            user = User.objects.create(
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data['email'],
                password=make_password(data['password']),
                phone_number=data['phone_number'],
                city_id=city_id,
                is_employer=data.get('is_employer', False),
                is_candidate=data.get('is_candidate', False),
            )
            serializer = UserSerializerToken(user, many=False)
            return Response(serializer.data, status=201)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                return Response({'message': 'User with this email already exists'}, status=400)
            else:
                return Response({'message': str(e)}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UpdateUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not user.check_password(old_password):
            return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'message': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
