from rest_framework.permissions import BasePermission
from .models import Product

class IsSameUser(BasePermission):
    """
    Custom permission to only allow the same users to edit data.
    """
    message = "You need to be the same user to perform this acction."
    
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object
        return obj == request.user



class PostAuth(BasePermission):
    message = "Invalid authentication."
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated
        return super().has_permission(request, view)
    

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = "You need to be the owner of this object to perform this action."

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ['GET']:
            return True
        return obj.seller == request.user
    

    

class IsSeller(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "User Role is not seller"

    def has_object_permission(self, request, view, obj):
        print("IsSeller")
        if request.method in ['GET']:
            return True
        return request.user.role == "seller"
