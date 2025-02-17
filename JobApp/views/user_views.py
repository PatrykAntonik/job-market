from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from JobApp.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.db import IntegrityError
from JobApp.permissions import IsEmployer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerToken(self.user).data
        for i, j in serializer.items():
            data[i] = j
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)


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
def updateUserProfile(request):
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
    return Response(serializer.data, status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserPassword(request):
    user = request.user
    data = request.data

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect'}, status=400)

    if new_password != confirm_password:
        return Response({'message': 'New passwords do not match'}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully'}, status=201)
