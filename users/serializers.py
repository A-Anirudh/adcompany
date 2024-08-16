from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from users.models import ROLE_CHOICES

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            ),
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'role', 'phone')

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})

        # Ensure role is valid
        if data['role'] not in dict(ROLE_CHOICES):
            raise serializers.ValidationError({"role": "Invalid role selected."})
        
        return data

    def create(self, validated_data):
        # Pop password2 as it's not needed anymore
        validated_data.pop('password2')

        # Create user with the provided validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            phone=validated_data['phone']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
