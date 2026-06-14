from rest_framework import serializers
from authentication.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "created_at",
            "updated_at",
            "role",
            "is_active",
        ]