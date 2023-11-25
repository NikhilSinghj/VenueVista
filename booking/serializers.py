from django.contrib.auth.models import User
from rest_framework import serializers
from django.core import validators
from django.contrib.auth.password_validation import validate_password
from booking.models import ConferenceHall,HallBooking,ConfHallImages,LeftPannel,UserDepartment
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
    # booked_hall=HallBookingSerializer(many=True,read_only=True)
    class Meta:
        model=ConferenceHall
        # fields="__all__"
        exclude=['deleted_status','deleted_time','created_time']

    
    def validate_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError("Name is too short!")
        
        else:
            return value
        
        
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDepartment
        fields=['dept_name']

class DepartmentSerializer2(serializers.ModelSerializer):
    dept=DepartmentSerializer(read_only=True)
    class Meta:
        model=UserDepartment
        fields=['dept']

class ReportSerializer(serializers.ModelSerializer):
    booked_by=UserSerializer(read_only=True)
    hall = ConferenceHallSerializer(read_only=True)
    hod = UserSerializer(read_only=True)
    ao = UserSerializer(read_only=True)
    avl_hall=ConferenceHallSerializer(read_only=True)
    emp_dept=DepartmentSerializer2(read_only=True)
    class Meta:
        model=HallBooking
        # exclude=('appr_by_hod','hod_remark','appr_timestp_hod','appr_by_ao','ao_remark','appr_timestp_ao','deleted_status','deleted_time','created_time')
        fields="__all__"

class HallBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=HallBooking
        exclude=('appr_by_hod','hod_remark','appr_timestp_hod','appr_by_ao','ao_remark','appr_timestp_ao','deleted_status','deleted_time','created_time')       


class HallApprovalHODSerializer(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        fields=['hod_remark','appr_by_hod','avl_hall']
        read_only_fields = ['hod_remark']


class HallApprovalAOSerializer(serializers.ModelSerializer):

    class Meta:
        model=HallBooking
        fields=['ao_remark']

# class LeftPanelSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=LeftPannel
#         fields=['id','name','route']

class ConferenceHallSerializer2(serializers.ModelSerializer):
    class Meta:
        model=ConferenceHall
        fields=['id','name']
          