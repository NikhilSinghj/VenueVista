from rest_framework import permissions,status
from booking.models import UserRole,Roles
from rest_framework.response import Response

    
class UserRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        role=Roles.objects.filter(deleted_status=False,role_name='Employee')
        user_role=UserRole.objects.filter(deleted_status=False,user=self.request.user,role=role.pk)
        if user_role:
            return True
        else:
            return False
        
class HodRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        role=Roles.objects.filter(deleted_status=False,role_name='HOD')
        print(role.id)
        user=request.user.id
        print(user)
        if request.user.id is None:
            return False
            return Response({'error':'No hall found'},status=status.HTTP_204_NO_CONTENT)
        user_role=UserRole.objects.filter(deleted_status=False,user=user,role=role.pk)
        if user_role:
            return True
        else:
            return False