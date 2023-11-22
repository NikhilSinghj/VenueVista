from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from booking.views import (RegistrationVS,ConferenceHallVS,
                           HallBookingVS,UserProfileVS,LogoutVS,
                           HodApprovalVS,HodRejectionVS,
                           AOApprovalVS,AORejectionVS)

urlpatterns = [
    path('register/',RegistrationVS.as_view(),name='register'), 
    path('profile/',UserProfileVS.as_view(),name='profile'),  
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('logout/', LogoutVS.as_view(), name='token_blacklist'),
    path('conference_hall/',ConferenceHallVS.as_view(),name='conference_hall'),
    path('hallbooking/',HallBookingVS.as_view(),name='hallbooking'),
    path('hod_approval/<int:pk>',HodApprovalVS.as_view(),name='hod_approval'),
    path('hod_rejection/<int:pk>',HodRejectionVS.as_view(),name='hod_rejection'),
    path('ao_approval/<int:pk>',AOApprovalVS.as_view(),name='ao_approval'),
    path('ao_rejection/<int:pk>',AORejectionVS.as_view(),name='ao_rejection'),
]