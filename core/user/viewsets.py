from rest_framework.permissions import IsAuthenticated, AllowAny
from core.auth.permissions import UserPermissions

from core.user.serializers import UserSerializer
from core.user.models import User
from core.abstract.viewsets import AbstractViewSet

from rest_framework.response import Response
from rest_framework import status


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def http_method_not_allowed(self, request, *args, **kwargs):
        allowed_methods = ', '.join(self.http_method_names)
        return Response(
            {
                "detail": f"Only {allowed_methods} method(s) are/is allowed."
            },
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
