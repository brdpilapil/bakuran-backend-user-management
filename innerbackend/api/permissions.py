from rest_framework.permissions import BasePermission

class IsOwnerOrAdminForUserManagement(BasePermission):
    """
    - Owner: full access to user management (including creating admins/owners).
    - Admin: can manage waiter/cashier only.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "role", None) in ("owner", "admin"))

    def has_object_permission(self, request, view, obj):
        user = request.user
        if getattr(user, "role", None) == "owner":
            return True
        if getattr(user, "role", None) == "admin":
            return getattr(obj, "role", None) in ("waiter", "cashier")
        return False
