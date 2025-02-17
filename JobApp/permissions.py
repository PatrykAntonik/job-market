from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):
    """
    Allows access only to users that are marked as employers.
    """
    message = "Access restricted to employers only."

    def has_permission(self, request, view):
        if (
                request.user and
                request.user.is_authenticated and
                request.user.is_employer and
                hasattr(request.user, 'employer')):
            return True

        raise exceptions.PermissionDenied(self.message)