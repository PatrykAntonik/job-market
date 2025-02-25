from django.urls import path
from JobApp.views.user_views import *

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    # path('profile/update/', updateUserProfile, name='profile-update'),
    path('profile/password/', updateUserPassword, name='user-update-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('<str:pk>/', getUser, name='user'),
    path('', UserListView.as_view(), name='users'),
]
