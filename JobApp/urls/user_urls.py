from django.urls import path
from JobApp.views.user_views import *

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('profile/', getUserProfile, name='profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('profile/update/', updateUserProfile, name='profile-update'),
    path('profile/update/password/', updateUserPassword, name='user-update-password'),
    path('<str:pk>/', getUser, name='user'),
    path('', getUsers, name='users'),
]
