from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from booking.models import ConferenceHall,HallBooking
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from booking.permissions import HodRolePermission,AoRolePermission
from datetime import datetime
from booking.serializers import (RegistrationSerializer,UserProfileSerializers,
                                 ConferenceHallSerializers,HallBookingSerializers,
                                 HallApprovalHOD,HallApprovalAO)


class RegistrationVS(generics.CreateAPIView):
    serializer_class=RegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserProfileVS(generics.ListAPIView):
    serializer_class=UserProfileSerializers
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id).values('username','email')
    
class LogoutVS(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token=self.request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(token=refresh_token)
            check=token.blacklist()
            # if not check:
            #     return Response({"message": "Already logged out"},status=status.HTTP_200_OK)
            return Response({"message": "Logged out successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "Provide refresh token"},status=status.HTTP_401_UNAUTHORIZED)



class ConferenceHallVS(generics.ListCreateAPIView):
    serializer_class=ConferenceHallSerializers

    def get(self,request,*args, **kwargs):
        return self.list(request,*args,**kwargs)

    def get_queryset(self):
        return ConferenceHall.objects.filter(deleted_status=False)

    def perform_create(self, serializer):
        name=self.request.data['name']
        print(name)
        # print(serializer)
        get_name=ConferenceHall.objects.filter(name=name,deleted_status=False)
        if get_name.exists():
            raise ValidationError("Conference hall for this name already exist")
        serializer.save()

# from rest_framework.parsers import MultiPartParser,FormParser
# class ConferenceHallVS(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         blog_serializer = ConferenceHallSerializers(data = request.data)
#         if blog_serializer.is_valid():
#             blog_serializer.save()
#             return Response(blog_serializer.data)
#         else:
#             return Response(blog_serializer.errors)


class HallBookingVS(generics.ListCreateAPIView):
    serializer_class=HallBookingSerializers
    # permission_classes=[IsAuthenticated]
    # def get_queryset(self):
    #     return HallBooking.objects.all()
    
    def perform_create(self, serializer):
        hall=self.request.data['hall']
        conf_hall=ConferenceHall.objects.get(pk=hall)

        user=self.request.user
        booking=HallBooking.objects.filter(booked_by=user,hall=conf_hall.pk)
        if booking.exists():
            raise ValidationError("You already booked this hall")
        else:
            serializer.save(booked_by=user,hall=conf_hall)
            # return Response()

class HodApprovalVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalHOD    
    permission_classes=[IsAuthenticated,HodRolePermission]

    # def get()

    def get_queryset(self):
        return HallBooking.objects.all()
    # print(HallBooking.objects.all())

    def perform_update(self, serializer):
        serializer.save(appr_by_hod=True,appr_timestp_hod=datetime.now(),hod=self.request.user)

class HodRejectionVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalHOD    
    permission_classes=[IsAuthenticated,HodRolePermission]

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(deleted_status=True,deleted_time=datetime.now(),hod=self.request.user)

class AOApprovalVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalAO    
    permission_classes=[IsAuthenticated,AoRolePermission]

    # def get()

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(appr_by_ao=True,appr_timestp_ao=datetime.now(),ao=self.request.user)

class AORejectionVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalAO    
    permission_classes=[IsAuthenticated,AoRolePermission]

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(deleted_status=True,deleted_time=datetime.now(),ao=self.request.user)
    
        
class