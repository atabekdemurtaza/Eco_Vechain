from core.user.models import User, HDWallet
from core.abstract.serializers import AbstractSerializer
from django.conf import settings
from rest_framework import serializers


class UserSerializer(AbstractSerializer):
    mnemonic = serializers.CharField(source='hd_wallet.mnemonic', read_only=True)
    public_key = serializers.CharField(source='hd_wallet.public_key', read_only=True)
    private_key = serializers.CharField(source='hd_wallet.private_key', read_only=True)
    address = serializers.CharField(source='hd_wallet.address', read_only=True)

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
            "mnemonic",  # Добавляем поля кошелька пользователя
            "public_key",
            "private_key",
            "address"
        ]
        read_only_fields = ['is_active']
