from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenBlacklistView
)
from booking.views import (RegistrationVS,ConferenceHallVS,
                           HallBookingVS,UserProfileVS,
                           HodApprovalVS,HodRejectionVS,
                           AOApprovalVS,AORejectionVS,LeftPannelAV,
                           GetConfHallAV,UpdateConferenceHallVS,
                           AvlConfHallAV)

urlpatterns = [
    path('register/',RegistrationVS.as_view(),name='register'), 
    path('profile/',UserProfileVS.as_view(),name='profile'),  
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('conference_hall/',ConferenceHallVS.as_view(),name='conference_hall'),
    path('conference_hall/<int:pk>',UpdateConferenceHallVS.as_view(),name='update_conference_hall'),
    path('hallbooking/',HallBookingVS.as_view(),name='hallbooking'),
    path('hod_approval/<int:pk>',HodApprovalVS.as_view(),name='hod_approval'),
    path('hod_rejection/<int:pk>',HodRejectionVS.as_view(),name='hod_rejection'),
    path('ao_approval/<int:pk>',AOApprovalVS.as_view(),name='ao_approval'),
    path('ao_rejection/<int:pk>',AORejectionVS.as_view(),name='ao_rejection'),
    path('left_panel/',LeftPannelAV.as_view(),name='left_panel'),
    path('drop_conf_hall/',GetConfHallAV.as_view(),name='conference_hall_dropdown'),
    path('avl_conf_hall/',AvlConfHallAV.as_view(),name='avialable_conference_hall'),
]