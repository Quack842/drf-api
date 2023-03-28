from rest_framework import serializers
from .models import Followers
from django.db import IntegrityError


class FollowersSerializer(serializers.ModelSerializer):
    """
    Serializer for the Followers model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Followers
        fields = [
            'id', 'owner', 'created_at',
            'followed_name', 'followed'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IndentationError:
            raise serializers.ValidationError({
                'details': 'possible duplicate'
            })
