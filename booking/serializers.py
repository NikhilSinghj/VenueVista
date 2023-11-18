from django.contrib.auth.models import User
from rest_framework import serializers
from django.core import validators
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(validators=[validate_password],write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

    def save(self):
        password=self.validated_data['password']
        email=self.validated_data['email']
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        account=User(first_name=self.validated_data['first_name'],last_name=self.validated_data['last_name'],email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()