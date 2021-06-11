from rest_framework.permissions import BasePermission, SAFE_METHODS

class PostPermission(BasePermission): 
    """
        The default permission of Post app.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS :
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS :
            return True

        elif not request.user:    
            return False
            
        return bool(request.user.id == obj.user.id)
