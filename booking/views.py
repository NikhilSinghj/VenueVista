from django.shortcuts import render
import json
from booking.serializers import RegistrationSerializer,ConferenceHallSerializers,HallBookingSerializers
from rest_framework import generics,status
from rest_framework.response import Response
from booking.models import ConferenceHall,HallBooking
from rest_framework.validators import ValidationError
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegistrationVS(generics.CreateAPIView):
    serializer_class=RegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()


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
    def get_queryset(self):
        return HallBooking.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        print(pk)
        conf_hall=ConferenceHall.objects.get(pk=pk)

        user=self.request.user
        booking=HallBooking.objects.filter(booked_by=user,hall=conf_hall)
        if booking.exists():
            raise ValidationError("You have already reviewed this movie")
        else:
            serializer.save(booked_by=user,hall=conf_hall)
            # return Response()




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
        return Response(data, status=status.HTTP_200_OK)