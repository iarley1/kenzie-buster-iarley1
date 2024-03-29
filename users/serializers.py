from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=151)
    email = serializers.EmailField(max_length=127)
    birthdate = serializers.DateField(default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:
        email_message = "email already registered."
        username_message = "username already taken."

        if (
            User.objects.filter(email=validated_data["email"]).exists()
            and User.objects.filter(username=validated_data["username"])
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    "email": [email_message],
                    "username": [username_message],
                }
            )

        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": [email_message]})

        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": [username_message]})

        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)
        
    def update(self, instance: User, validated_data: dict):
        if validated_data["password"]:
            validated_data["password"] = make_password(validated_data['password'])
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()    

        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=151, write_only=True)
    password = serializers.CharField(write_only=True)