from django.shortcuts import render
import json
from booking.serializers import RegistrationSerializer,UserProfileSerializers,ConferenceHallSerializers,HallBookingSerializers,HallApprovalHOD
from rest_framework import generics,status
from rest_framework.response import Response
from booking.models import ConferenceHall,HallBooking
from rest_framework.validators import ValidationError
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from booking.permissions import HodRolePermission
from datetime import datetime


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

    def get_queryset(self):
        return ConferenceHall.objects.filter(deleted_status=False)

    def perform_create(self, serializer):
        name=self.request.data['name']
        print(name)
        get_name=ConferenceHall.objects.filter(name=name,deleted_status=False)
        if get_name.exists():
            raise ValidationError("Conference hall for this name already exist")
        serializer.save()

class HallBookingVS(generics.ListCreateAPIView):
    serializer_class=HallBookingSerializers
    permission_classes=[IsAuthenticated]
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
    permission_classes=[IsAuthenticated]
    permission_classes=[HodRolePermission]
    def get_queryset(self):
        return HallBooking.objects.all()
    print(HallBooking.objects.all())

    def perform_update(self, serializer):
        pk=self.kwargs.get('pk')
        try:
            hall=HallBooking.objects.get(deleted_status=False,pk=pk)
        except:
            return Response({'error':'No hall found'},status=status.HTTP_204_NO_CONTENT)
        serializer.save(appr_by_hod=True,appr_timestp_hod=datetime.now())
        return Response({'message':'Hall approved'},status=status.HTTP_200_OK)
        
        



        




@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
    })

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user
    }

def login(request):
    load=json.loads(request.body)
    email=load.get('email')
    password=load.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        user_id = User.objects.get(email=email)
        data = get_tokens_for_user(user_id)
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'message':'jdcn'}, status=status.HTTP_200_OK)