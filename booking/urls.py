from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from booking.views import RegistrationVS,ConferenceHallVS,HallBookingVS,current_user,login

urlpatterns = [
    path('register/',RegistrationVS.as_view(),name='register'), 
    path('currentuser/',current_user,name='currentuser'),  
    path('login/',login,name='login'), 
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('conferencehall/',ConferenceHallVS.as_view(),name='conferencehall'),
    path('hallbooking/',HallBookingVS.as_view(),name='hallbooking'),
]