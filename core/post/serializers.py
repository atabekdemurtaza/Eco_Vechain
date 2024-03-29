from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


class PostSerializer(AbstractSerializer):

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'name',
            'description',
            'images',
            'eco_type',
            'weight',
            'approved',
            'qr_code',
            'last_updates',
            'author',
        ]

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You cannot create a post for another user.")
        return value

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep

    def has_private_key(self, author):
        return hasattr(author.hd_wallet, 'private_key') and isinstance(author.hd_wallet.private_key, str)

