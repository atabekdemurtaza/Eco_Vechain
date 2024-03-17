from core.user.models import User, HDWallet
from core.abstract.serializers import AbstractSerializer
from django.conf import settings
from rest_framework import serializers


class HDWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDWallet
        fields = ['mnemonic', 'public_key', 'private_key', 'address']


class UserSerializer(AbstractSerializer):
    hd_wallet = HDWalletSerializer(read_only=True)

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
            "hd_wallet",
            "location",
            "wallet_price",
        ]
        read_only_fields = ['is_active']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.increment_total_activities()
        return instance
