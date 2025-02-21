from rest_framework import serializers
from django.contrib.auth.models import User


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

    def save(self):
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']

        if password != repeated_password:
            raise serializers.ValidationError({'error': 'Passwords do not match.'}) 
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        account = User(email=self.validated_data['email'], username=self.validated_data['email'])
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'email']