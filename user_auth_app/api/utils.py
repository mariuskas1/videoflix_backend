from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.html import format_html


def generate_activation_token(user):
    return urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)



def send_activation_email(request, user):

    uid, token = generate_activation_token(user)
    activation_url = f"http://localhost:4200/activate/{uid}/{token}/"

    html_message = format_html(f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: white;">
            
            <img src="https://i.postimg.cc/YCbNt72J/Logo.png" alt="Videoflix Logo" width="150" style="margin-bottom: 32px;">
            
            <p style="font-size: 16px; color: #555; margin-bottom: 24px;">Dear <span style="color: rgb(46, 62, 223);">{user.email}</span>,</p>
            
            <p style="font-size: 16px; color: #555;">
                Thank you for registering with <span style="color: rgb(46, 62, 223); font-weight: bold;">Videoflix</span>. 
                To complete your registration and verify your email address, please click the button below:
            </p>

            <!-- Button -->
            <a href="{activation_url}" 
                style="display: inline-block; padding: 12px 24px; margin: 32px 0; border-radius: 40px;
                font-size: 16px; color: white; background-color: rgb(46, 62, 223); text-decoration: none;
                font-weight: bold; cursor: pointer;">
                Activate Account
            </a>

            <p style="font-size: 14px; color: #777;">
                If you did not create an account with us, please disregard this email.
            </p>
            <p style="font-size: 16px; color: #777; margin-top: 20px;">
                Best regards, <br><br>
                <strong>Your Videoflix Team</strong>
            </p>
        </div>
    """)

    send_mail(
        "Confirm your email",
        "",  
        "info@videoflix.marius-kasparek.de", 
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )






