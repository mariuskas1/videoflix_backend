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
from .utils import generate_activation_token, send_activation_email, send_pw_reset_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from django.utils.encoding import force_str


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
    """
    This view checks if a provided authentication token is valid. If the token is
    valid and the user is authenticated, it returns a confirmation response.

    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"valid": True}, status=200)
    

class ActivateAccountView(APIView):
    """
    This view handles account activation by verifying a user's identity using a
    base64-encoded user ID (`uidb64`) and an activation token. If the token is valid,
    the user's account is activated.

    Methods:
        get(request, uidb64, token): Activates the user account if the token is valid.
    """

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
        


class RequestPasswordResetView(APIView):
    """
    This view allows users to initiate a password reset by providing their email address.
    If the email is associated with a registered user, a password reset link is sent to their email.

    Methods:
        post(request): Handles password reset requests by sending an email with a reset link.
    """

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

        send_pw_reset_mail(request,user)

        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
    


class PasswordResetConfirmView(APIView):
    """
    This view handles password reset confirmation by verifying the user's identity
    using a UID and token, ensuring the provided email matches, and validating 
    the new password before updating it.

    """

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            email = request.data.get("email")
            new_password = request.data.get("password")
            repeated_password = request.data.get("repeated_password")

            if not email or user.email != email:
                return Response({"error": "The email you entered is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            if not new_password or len(new_password) < 6:
                return Response({"error": "Password must be at least 6 characters long."}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != repeated_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password has been reset successfully!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)



class CheckEmailView(APIView):
    """
    This view checks if a account with a given mail is already registered.

    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(email=email).exists()

        return Response({"exists": user_exists}, status=status.HTTP_200_OK)