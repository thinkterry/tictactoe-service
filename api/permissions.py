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

        header_token = self._parse_header_token(request)
        return header_token and header_token in [obj.x_token, obj.o_token]

    # @DRY views.py
    def _parse_header_token(self, request):
        """Extract authorization token from request headers."""
        try:
            # per http://stackoverflow.com/a/3889790
            return request.META.get(
                'HTTP_AUTHORIZATION'
            ).strip().split()[1]
        except Exception:
            return None
