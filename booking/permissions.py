from rest_framework import permissions
from booking.models import UserRole,Roles,UserDepartment

    
class UserRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        role=Roles.objects.get(deleted_status=False,role_name='Employee')
        user=request.user.id
        if user is None:
            return False
        user_role=UserRole.objects.filter(deleted_status=False,user=user,role=role.pk)
        if user_role:
            return True
        else:
            return False
        
class HodRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        role=Roles.objects.get(deleted_status=False,role_name='HOD')
        user=request.user.id
        if user is None:
            return False
        user_role=UserRole.objects.filter(deleted_status=False,user=user,role=role.pk)
        if user_role:
            return True
        else:
            return False
        
class AoRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        role=Roles.objects.get(deleted_status=False,role_name='AO')
        user=request.user.id
        if user is None:
            return False
        user_role=UserRole.objects.filter(deleted_status=False,user=user,role=role.pk)
        if user_role:
            return True
        else:
            return False
        
# class DepartmentPermission(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         user=request.user.id
#         if user is None:
#             return False
#         # role=Roles.objects.get(deleted_status=False,role_name='AO')
#         dept=UserDepartment.objects.filter(deleted_status=False,user=user)
#         if dept:
#             return True
#         else:
#             return False