from django.contrib.auth.models import User
from rest_framework import serializers
from django.core import validators
from django.contrib.auth.password_validation import validate_password
from booking.models import ConferenceHall,HallBooking

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

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']



class ConferenceHallSerializers(serializers.ModelSerializer):
    class Meta:
        model=ConferenceHall
        fields=['id','name','description','occupancy','booking_days','image']
        # fields="__all__"


class HallBookingSerializers(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        exclude=('appr_by_hod','hod_remark','appr_timestp_hod','appr_by_ao','ao_remark','appr_timestp_ao','deleted_status','deleted_time')
        # fields=['id','hall','']
        # fields="__all__"

class HallApprovalHOD(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        fields=['hod_remark']
        # exclude=('appr_by_hod','hod_remark','appr_timestp_hod','appr_by_ao','ao_remark','appr_timestp_ao','deleted_status','deleted_time')   