from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from booking.views import Registration

urlpatterns = [
    path('register/',Registration.as_view(),name='register'), 
    # path('login/',obtain_auth_token,name='login'),  
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]