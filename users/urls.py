from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    # Register Endpoint
   path('register/', RegisterAPIView.as_view(), name='user_register'),

   # Login Endpoint
   path('login/', LoginAPIView.as_view(), name='user_login'),

   # GET - Update User Profile Endpoint
   path('profile/', RetrieveUpdateUserProfileAPIView.as_view(), name='get_update_profile'),

   # Update Password Endpoint
   path('profile/password/', ChangePasswordView.as_view(), name='change_password'),
]