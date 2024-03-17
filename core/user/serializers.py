from core.user.models import User
from core.abstract.serializers import AbstractSerializer
from django.conf import settings


class UserSerializer(AbstractSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'avatar' in representation and not representation['avatar']:
            representation['avatar'] = settings.DEFAULT_AVATAR_URL
        if settings.DEBUG:
            request = self.context.get("request")
            if request:
                representation["avatar"] = request.build_absolute_uri(
                    representation["avatar"]
                )
        return representation

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "email",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ['is_active']
