from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from JobApp.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.db import IntegrityError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerToken(self.user).data
        for i, j in serializer.items():
            data[i] = j
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# USERS
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            city=data['city'],
            zip_code=data['zip_code'],
            phone_number=data['phone_number'],
            country=data['country'],
            province=data['province'],
            is_employer=data.get('is_employer', False),
            is_candidate=data.get('is_candidate', False),
        )
        serializer = UserSerializerToken(user, many=False)
        return Response(serializer.data)
    except IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            message = {'detail': 'User with this email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'detail': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = {'detail': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.city = data.get('city', user.city)
    user.zip_code = data.get('zip_code', user.zip_code)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.country = data.get('country', user.country)
    user.province = data.get('province', user.province)
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    serializer = UserSerializerToken(user, many=False)
    data = request.data
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.city = data.get('city', user.city)
    user.zip_code = data.get('zip_code', user.zip_code)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.country = data.get('country', user.country)
    user.province = data.get('province', user.province)
    user.is_employer = data.get('is_employer', user.is_employer)
    user.is_candidate = data.get('is_candidate', user.is_candidate)
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)
