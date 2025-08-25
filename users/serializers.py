from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'employee_id', 'name', 'role', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = UserProfile(
            username=validated_data['username'],
            email=validated_data['email'],
            employee_id=validated_data.get('employee_id'),
            name=validated_data.get('name'),
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance