from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    """
    Allows access to staff members and read-only access to non-staff users.
    
    Permission is granted if the user is a staff member or if the request method
    is one of the safe methods (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):    
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS
    
class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
    """
    Grants permission based on the request method and the user's role.
    
    - For safe methods (GET, HEAD, OPTIONS), access is granted to all users.
    - For DELETE requests, only superusers (admins) can delete the object.
    - For PATCH requests, only staff members can modify the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return bool(request.user and request.user.is_superuser)
        else:
            return bool(request.user and request.user.is_staff)
        
class IsOwnerOrAdmin(BasePermission):
    """
    Allows access to object owners and admins.
    
    - For safe methods (GET, HEAD, OPTIONS), access is granted to all users.
    - For DELETE requests, superusers (admins) can delete the object.
    - For other methods (e.g., PATCH), only the owner of the object or admins can modify it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return bool(request.user and request.user.is_superuser)
        else:
            return bool(request.user and request.user == obj.user)