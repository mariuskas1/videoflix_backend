from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

def generate_activation_token(user):
    return urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)



def send_activation_email(request, user):
    """Send an account activation email."""
    uid, token = generate_activation_token(user)
    # activation_url = f"{request.scheme}://{request.get_host()}/api/activate/{uid}/{token}/"
    activation_url = f"https://videoflix.marius-kasparek.de/activate/{uid}/{token}/"

    send_mail(
        "Activate your account",
        f"Click the link to activate your account: {activation_url}",
        "info@videoflix.marius-kasparek.de", 
        [user.email],
        fail_silently=False,
    )