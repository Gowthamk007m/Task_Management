from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'SUPERADMIN']

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'profile') and request.user.profile.role == 'SUPERADMIN'

class IsTaskOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

class IsTaskAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.profile.role == 'SUPERADMIN':
            return True
        if request.user.profile.role == 'ADMIN':
            # Check if the task is assigned to a user this admin can manage
            # For simplicity, we're assuming admins can access all tasks
            return True
        return False
    

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'SUPERADMIN']

def is_super_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'SUPERADMIN'
