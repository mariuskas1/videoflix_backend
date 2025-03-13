from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.html import format_html


def generate_activation_token(user):
    return urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)



def send_activation_email(request, user):
    """This function sends a mail to every newly registered user on which he can click on to activate his account."""

    uid, token = generate_activation_token(user)
    activation_url = f"https://videoflix.marius-kasparek.de/activate/{uid}/{token}/"

    html_message = format_html(f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: white;">
            
            <img src="https://videoflix.marius-kasparek.de/Logo.png" alt="Videoflix Logo" width="150" style="margin-bottom: 32px;">
            
            <p style="font-size: 16px; color: #555; margin-bottom: 24px;">Dear <span style="color: rgb(46, 62, 223);">{user.email}</span>,</p>
            
            <p style="font-size: 16px; color: #555;">
                Thank you for registering with <span style="color: rgb(46, 62, 223);">Videoflix</span>. 
                To complete your registration and activate your account, please click on the link below:
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



def send_pw_reset_mail(request, user):
        """This function sends a mail to a user who has requested a password reset. It contains a link on which he can click on
        that will redirect him to the reset-password page, with authentication tokens in the url."""
    
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://videoflix.marius-kasparek.de/reset-password/{uidb64}/{token}/"

        html_message = format_html(f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: white;">
                
                <img src="https://videoflix.marius-kasparek.de/Logo.png" alt="Videoflix Logo" width="150" style="margin-bottom: 32px;">
                
                <p style="font-size: 16px; color: #555; margin-bottom: 24px;">Dear <span style="color: rgb(46, 62, 223);">{user.email}</span>,</p>
                
                <p style="font-size: 16px; color: #555;">
                    Please click on the link below to reset your password:
                </p>

                <!-- Button -->
                <a href="{reset_url}" 
                    style="display: inline-block; padding: 12px 24px; margin: 32px 0; border-radius: 40px;
                    font-size: 16px; color: white; background-color: rgb(46, 62, 223); text-decoration: none;
                    font-weight: bold; cursor: pointer;">
                    Reset Password
                </a>

                <p style="font-size: 14px; color: #777;">
                    If you did not request a password reset, please disregard this email.
                </p>
                <p style="font-size: 16px; color: #777; margin-top: 20px;">
                    Best regards, <br><br>
                    <strong>Your Videoflix Team</strong>
                </p>
            </div>
        """)
        
       
        send_mail(
            "Password Reset",
            "",
            "info@videoflix.marius-kasparek.de",
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )



