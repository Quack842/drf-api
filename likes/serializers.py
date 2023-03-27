from rest_framework import serializers
from .models import Like
from django.db import IntegrityError


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Likes model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except InterruptedError:
            raise serializers.ValidationError({
                'details': 'possible deuplicate'
            })
