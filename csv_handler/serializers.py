from rest_framework import serializers
from .models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name must be a non-empty string.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email must be valid.")
        return value

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be an integer between 0 and 120.")
        return value
