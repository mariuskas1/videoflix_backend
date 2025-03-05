from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'A user with this email already exists.'})

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')  
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("Account not activated.")

        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'email']