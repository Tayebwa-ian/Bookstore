from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

class ReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsAdminUserOrReadOnly(IsAdminUser):
    """
    Allow other users to view or read data but not post of update it
    unless they are admin users
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)
    
class IsAdminUserOrSellerOrReadOnly(IsAdminUserOrReadOnly):
    """
    Permission to allow access to all request methods if current user
    is either admin or seller otherwise the user can only read data
    """
    def has_permission(self, request, view):
        if request.user.is_seller:
            return True
        return super().has_permission(request, view)
    
class IsCustomerOrAdmin(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_customer or request.user.is_staff:
            return True
        
class CanUpdateCart(ReadOnly):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH'] and (request.user.is_customer or request.user.is_staff):
            return True
        return super().has_permission(request, view)
        
        
class IsAdminOrReadOnly(ReadOnly):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return super().has_permission(request, view)