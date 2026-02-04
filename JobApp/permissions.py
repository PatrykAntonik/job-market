from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):
    """
    Allows access only to users that are marked as employers.
    """

    message = "Access restricted to employers only"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "employer")
        )


class IsCandidate(BasePermission):
    """
    Allows access only to users that are marked as candidates.
    """

    message = "Access restricted to candidates only"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "candidate")
        )
