from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Define a permission.

    Per http://www.django-rest-framework.org/tutorial/4-
    authentication-and-permissions/#object-level-permissions
    """

    def has_object_permission(self, request, view, obj):
        """Define an object permission."""
        # don't require a token for read-only access
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            # per http://stackoverflow.com/a/3889790
            header_token = request.META.get(
                'HTTP_AUTHORIZATION'
            ).strip().split()[1]
        except Exception:
            return False

        return header_token in [obj.x_token, obj.o_token]
