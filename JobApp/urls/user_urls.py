from django.urls import path
from JobApp.views.user_views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    # path('profile/update/', updateUserProfile, name='profile-update'),
    path('profile/password/', UpdateUserPasswordView.as_view(), name='user-update-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('<int:pk>/', UserDetailView.as_view(), name='user'),
    path('', UserListView.as_view(), name='users'),
]
