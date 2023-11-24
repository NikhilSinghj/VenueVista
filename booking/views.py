from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from booking.models import ConferenceHall,HallBooking,LeftPannel,Roles,UserRole,ConfHallImages
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from booking.permissions import HodRolePermission,AoRolePermission,UserRolePermission
from datetime import datetime
from booking.serializers import (RegistrationSerializer,UserProfileSerializer,
                                 ConferenceHallSerializer,HallBookingSerializer,
                                 HallApprovalHODSerializer,HallApprovalAOSerializer)


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



# class ConferenceHallVS(generics.ListCreateAPIView):
#     serializer_class=ConferenceHallSerializer
#     # permission_classes=[IsAuthenticated,AoRolePermission]

#     def get_queryset(self):
#         return ConferenceHall.objects.filter(deleted_status=False)

#     def perform_create(self, serializer):
#         name=self.request.data['name']
#         print(name)
#         print(serializer)
#         get_name=ConferenceHall.objects.filter(name=name,deleted_status=False)
#         if get_name.exists():
#             raise ValidationError("Conference hall for this name already exist")
#         serializer.save()

# class ConferenceHallVS(generics.ListCreateAPIView):
#     serializer_class=ConferenceHallSerializer
#     # permission_classes=[IsAuthenticated,AoRolePermission]

#     def get_queryset(self):
#         return ConferenceHall.objects.filter(deleted_status=False)

#     def post(self, request, *args, **kwargs):
#         data=request.data
#         pop=request.data.pop('image')
#         images=request.FILES.getlist('image')

#         print(images)
#         print(data)
#         print(pop)
#         return Response({'dbnss'})


class ConferenceHallVS(generics.ListCreateAPIView):
    # permission_classes=[IsAuthenticated,AoRolePermission]
    serializer_class=ConferenceHallSerializer
    def get_queryset(self):
        return ConferenceHall.objects.filter(deleted_status=False)


    def post(self, request, *args, **kwargs):
        hall_serializer = ConferenceHallSerializer(data = request.data)
        if hall_serializer.is_valid():
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
    serializer_class=HallApprovalHODSerializer  
    permission_classes=[IsAuthenticated,HodRolePermission]

    # def get()

    def get_queryset(self):
        return HallBooking.objects.all()
    # print(HallBooking.objects.all())

    def perform_update(self, serializer):
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

class AvlConfHallAV(APIView):
    permission_classes=[IsAuthenticated,AoRolePermission]
    def get(self,request,*args, **kwargs):
        # avl_hall=
        data=list(ConferenceHall.objects.filter(deleted_status=False).values('name','route'))
        return Response(data)
    
class GetConfHallAV(APIView):
    permission_classes=[IsAuthenticated,UserRolePermission]
    def get(self,request,*args, **kwargs):
        data=list(ConferenceHall.objects.filter(deleted_status=False).values('id','name'))
        return Response(data)