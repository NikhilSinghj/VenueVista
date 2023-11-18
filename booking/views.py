from django.shortcuts import render
from booking.serializers import RegistrationSerializer
from rest_framework import generics,status
from rest_framework.response import Response

class Registration(generics.CreateAPIView):
    serializer_class=RegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()