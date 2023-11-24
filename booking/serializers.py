from django.contrib.auth.models import User
from rest_framework import serializers
from django.core import validators
from django.contrib.auth.password_validation import validate_password
from booking.models import ConferenceHall,HallBooking,ConfHallImages,LeftPannel
from rest_framework.validators import UniqueValidator
class RegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(validators=[validate_password],write_only=True)
    email = serializers.EmailField()
    # email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists!")
        return value

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        password=self.validated_data['password']
        user.set_password(password)
        user.save()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']

class ConfHallImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConfHallImages
        fields = ["image"]

class ConferenceHallSerializer(serializers.ModelSerializer):
    confhall = ConfHallImagesSerializer(many = True,read_only=True)
    class Meta:
        model=ConferenceHall
        # fields="__all__"
        exclude=['deleted_status','deleted_time','created_time']

    # def validate_name(self,value):
    #     # if len(value)<2:
    #     #     raise serializers.ValidationError("Name is too short!")
    #     print(value)
    #     if self.context.get('is_create'):
    #         print(value)
    #         if ConferenceHall.objects.filter(name=value,deleted_status=False).exists():
    #             raise serializers.ValidationError("Conference hall for this name already exist")
    #         else:
    #             return value
        
    # def create(self, validated_data):
    #     print(validated_data)
    #     image = validated_data.pop("image")
    #     print(image)
    #     # image=validated_data.FILE.getlist('image')
    #     print(image)
    #     conf_hall = ConferenceHall.objects.create(**validated_data)
    #     ConfHallImages.objects.create(conf_hall=conf_hall, **image)
    #     # for f in image:
    #     #     ConfHallImages.objects.create(conf_hall = conf_hall, **f)

    #     return conf_hall


class HallBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        exclude=('appr_by_hod','hod_remark','appr_timestp_hod','appr_by_ao','ao_remark','appr_timestp_ao','deleted_status','deleted_time')
        # fields=['id','hall','']
        # fields="__all__"

class HallApprovalHODSerializer(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        fields=['hod_remark']

class HallApprovalAOSerializer(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        fields=['ao_remark']

# class LeftPanelSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=LeftPannel
#         fields=['id','name','route']


          