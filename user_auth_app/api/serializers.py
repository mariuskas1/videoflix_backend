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

        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'email']