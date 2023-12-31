from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class User(AbstractUser):
#     pass

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True)
    deleted_status=models.BooleanField(default=False)
    class Meta:
        abstract = True

class UserDepartment(BaseModel):
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='user')
    dept_name=models.CharField(max_length=50,null=True)
    dept=models.ForeignKey("UserDepartment",null=True,on_delete=models.SET_NULL,related_name='user_dept')

class LeftPannel(BaseModel):
    name=models.CharField(max_length=50)
    icon=models.CharField(max_length=50)
    route=models.CharField(max_length=50)
    order=models.PositiveIntegerField(null=True)
    role= models.PositiveIntegerField(null=True)
    
class Roles(BaseModel):
    role_name=models.CharField(max_length=50)

class UserRole(BaseModel):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_idty')
    role=models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True)

class ConferenceHall(BaseModel):
    name=models.TextField(max_length=50)
    description=models.TextField(max_length=200)
    occupancy=models.PositiveIntegerField()
    booking_days=models.PositiveIntegerField()

class ConfHallImages(BaseModel):
    conf_hall=models.ForeignKey(ConferenceHall,on_delete=models.SET_NULL,null=True,related_name='confhall')
    image=models.ImageField(upload_to='')

class HallBooking(BaseModel):
    hall=models.ForeignKey(ConferenceHall,null=True,on_delete=models.SET_NULL,related_name='booked_hall')
    booked_by=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='empl_idty')
    from_date=models.DateField()
    f_time=models.TimeField()
    to_date=models.DateField()
    t_time=models.TimeField()
    participants=models.PositiveIntegerField()
    purpose=models.CharField(max_length=100)
    emp_dept=models.ForeignKey(UserDepartment,null=True,on_delete=models.SET_NULL,related_name='empl_dept')
    emp_remark=models.TextField(max_length=200)
    hod=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='hod_idty')
    appr_by_hod=models.BooleanField(default=False)
    hod_remark=models.TextField(max_length=200)
    appr_timestp_hod=models.DateTimeField(null=True)
    ao=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='ao_idty')
    appr_by_ao=models.BooleanField(default=False)
    ao_remark=models.TextField(max_length=200)
    appr_timestp_ao=models.DateTimeField(null=True)
    avl_hall=models.ForeignKey(ConferenceHall,null=True,on_delete=models.SET_NULL,related_name='avl_hall')
    reject_status=models.BooleanField(default=False)
    reject_time = models.DateTimeField(null=True)
    



