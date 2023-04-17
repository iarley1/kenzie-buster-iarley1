from rest_framework import permissions
from rest_framework.views import Request, View


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        if obj == request.user:
            return True

        if request.user.is_superuser:
            return True

        return False
    
class IsAuthenticatedGet(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return(request.user.is_authenticated)    