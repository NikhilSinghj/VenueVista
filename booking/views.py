from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from booking.models import ConferenceHall,HallBooking,LeftPannel,Roles,UserRole,ConfHallImages,UserDepartment
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from booking.permissions import HodRolePermission,AoRolePermission,UserRolePermission
from datetime import datetime
from booking.serializers import (RegistrationSerializer,UserProfileSerializer,
                                 ConferenceHallSerializer,HallBookingSerializer,
                                 HallApprovalHODSerializer,HallApprovalAOSerializer,
                                 ConferenceHallSerializer2,ReportSerializer)


class RegistrationVS(generics.CreateAPIView):
    serializer_class=RegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserProfileVS(generics.ListAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id).values('username','email')
    
# class LogoutVS(generics.CreateAPIView):
#     # permission_classes=[IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         refresh_token=self.request.data.get('refresh')
#         if refresh_token:
#             token = RefreshToken(token=refresh_token)
#             check=token.blacklist()
#             print(check)
#             if not check:
#                 return Response({"message": "Already logged out"},status=status.HTTP_200_OK)
#             return Response({"message": "Logged out successfully"},status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Provide refresh token"},status=status.HTTP_401_UNAUTHORIZED)


class ConferenceHallVS(generics.ListCreateAPIView):
    # permission_classes=[IsAuthenticated,AoRolePermission]
    serializer_class=ConferenceHallSerializer
    def get_queryset(self):
        return ConferenceHall.objects.filter(deleted_status=False)


    def post(self, request, *args, **kwargs):
        hall_serializer = ConferenceHallSerializer(data = request.data)
        if hall_serializer.is_valid():
            name=request.data.get('name')
            if ConferenceHall.objects.filter(name=name,deleted_status=False).exists():
                raise ValidationError("Conference hall for this name already exist")
            images=request.data.pop('image')
            conf_hall=hall_serializer.save()
            for image in images:
                ConfHallImages.objects.create(conf_hall=conf_hall,image=image)
            return Response({'message':'Hall added successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(hall_serializer.errors)
        
    def perform_update(self, serializer):
        serializer.save()

class UpdateConferenceHallVS(generics.RetrieveUpdateAPIView):
    serializer_class=ConferenceHallSerializer

    def get_queryset(self):
        return ConferenceHall.objects.filter(deleted_status=False)

    def perform_update(self, serializer):
        serializer.save()
        


class HallBookingVS(generics.ListCreateAPIView):
    serializer_class=HallBookingSerializer
    permission_classes=[IsAuthenticated]
    queryset=HallBooking.objects.filter()
    def get(self,request,*args, **kwargs):
        queryset=HallBooking.objects.filter(deleted_status=False)
        return Response(ReportSerializer(queryset,many=True).data)
    
    def perform_create(self, serializer):
        hall=self.request.data['hall']
        conf_hall=ConferenceHall.objects.get(pk=hall)
        user=self.request.user
        booking=HallBooking.objects.filter(booked_by=user,hall=conf_hall.pk)
        if booking.exists():
            raise ValidationError("You already booked this hall")
        else:
            serializer.save(booked_by=user,hall=conf_hall)

    def perform_update(self,serializer):
        serializer.save(deleted_status=True,deleted_time=datetime.now())


class HodApprovalVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalHODSerializer  
    permission_classes=[IsAuthenticated,HodRolePermission]
    # def get(self,request,*args, **kwargs):
    #     queryset=HallBooking.objects.filter(deleted_status=False)
    #     return Response(ReportSerializer(queryset,many=True).data)

    def get_queryset(self):
        return HallBooking.objects.filter(pk=self.kwargs.get('pk'))
    # print(HallBooking.objects.all())
    

    def perform_update(self, serializer):
        # avl_hall=self.request.
        # conf_hall=ConferenceHall.objects.get(pk=)
        # hall=HallBooking.objects.get(deleted_status=False,pk=self.kwargs.get('pk'))
        # empl_dept=UserDepartment.objects.filter(dept=hall.emp_dept.id,user=self.request.user.pk)
        # print(hall)
        # print(empl_dept)
        # print(self.request.user.pk)
        # if empl_dept.exists():
        #     return Response({'message':'You are from another department'},status=status.HTTP_403_FORBIDDEN)
        serializer.save(appr_by_hod=True,appr_timestp_hod=datetime.now(),hod=self.request.user)

class HodRejectionVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalHODSerializer   
    permission_classes=[IsAuthenticated,HodRolePermission]

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(deleted_status=True,deleted_time=datetime.now(),hod=self.request.user)

class AOApprovalVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalAOSerializer    
    permission_classes=[IsAuthenticated,AoRolePermission]

    # def get()

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(appr_by_ao=True,appr_timestp_ao=datetime.now(),ao=self.request.user)

class AORejectionVS(generics.RetrieveUpdateAPIView):
    serializer_class=HallApprovalAOSerializer  
    permission_classes=[IsAuthenticated,AoRolePermission]

    def get_queryset(self):
        return HallBooking.objects.all()

    def perform_update(self, serializer):
        serializer.save(deleted_status=True,deleted_time=datetime.now(),ao=self.request.user)
    
        
class LeftPannelAV(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args, **kwargs):
        check_user_role=list(UserRole.objects.filter(user=self.request.user.id).values_list('role__role_name',flat=True))
        for role in check_user_role:
            if role=='Employee':
                role=Roles.objects.filter(role_name='Employee').first()
                data=list(LeftPannel.objects.filter(deleted_status=False,role=role.pk).values('name','route'))
                return Response(data)
            elif role=='HOD':
                role=Roles.objects.filter(role_name='HOD').first()
                data=list(LeftPannel.objects.filter(deleted_status=False,role=role.pk).values('name','route'))
                return Response(data)
            elif role=='AO':
                role=Roles.objects.filter(role_name='AO').first()
                data=list(LeftPannel.objects.filter(deleted_status=False,role=role.pk).values('name','route'))
                return Response(data)
            else:
                return Response({'message':'You not have any role'},status=status.HTTP_400_BAD_REQUEST)
        

class ReportAV(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self,request,*args, **kwargs):
        data=list(ConferenceHall.objects.filter(deleted_status=False).values('name','route'))
        return Response(data)

class AvlConfHallAV(generics.ListAPIView):
    # permission_classes=[IsAuthenticated,AoRolePermission]
    serializer_class=ConferenceHallSerializer
    def get(self,request,*args, **kwargs):
        to_date=self.request.query_params['to_date']
        from_date=self.request.query_params['from_date']

        booked=list(HallBooking.objects.filter(deleted_status=False,from_date=from_date,to_date=to_date).values_list('avl_hall',flat=True))
        avl=list(ConferenceHall.objects.filter(deleted_status=False).values_list('id',flat=True))
        queryset=[]
        for a_id in avl:
            if a_id not in booked:
                obj=ConferenceHall.objects.filter(pk=a_id)
                queryset.extend(obj)
        return Response(ConferenceHallSerializer2(queryset,many=True).data)
    
class GetConfHallAV(APIView):
    permission_classes=[IsAuthenticated,UserRolePermission]

    def get(self,request,*args, **kwargs):
        data=list(ConferenceHall.objects.filter(deleted_status=False).values('id','name'))
        return Response(data)