from rest_framework import generics
from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import generate_activation_token, send_activation_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status


User = get_user_model()  



class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            saved_account.is_active = False 
            saved_account.save()

            token, created = Token.objects.get_or_create(user=saved_account)
            data= {
                'token': token.key,
                'email': saved_account.email,
            }
            
            send_activation_email(request, saved_account)

        else:
            data=serializer.errors
        
        return Response(data)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'email': user.email,
                'id': user.id
            }
        else:
            data = serializer.errors
        
        return Response(data)
    

class UserView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class TokenValidationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"valid": True}, status=200)
    

class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)