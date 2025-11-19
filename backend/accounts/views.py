from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm

# --- NEW API IMPORTS ---
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


# Optional: Keep your existing HTML views (e.g., for testing)
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created!")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@csrf_exempt
def api_signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        form = UserRegisterForm({
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "password1": data.get("password", ""),
            "password2": data.get("password", ""),
            "country": data.get("country", ""),
        })
        if form.is_valid():
            user = form.save()

            # Send verification email
            verification_url = request.build_absolute_uri(
                f"/accounts/api/verify-email/{user.verification_token}/"
            )
            send_mail(
                subject="Verify your ZaraiLink account",
                message=f"Welcome to ZaraiLink!\n\nPlease verify your email by clicking the link below:\n{verification_url}\n\nThis link will expire in 24 hours.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return JsonResponse({
                "success": True,
                "message": "Account created! Please check your email to verify your account.",
                "email": user.email
            })
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    except Exception as e:
        return JsonResponse({"error": "Invalid request", "details": str(e)}, status=400)


@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                "success": True,
                "user": {
                    "name": f"{user.first_name} {user.last_name}".strip(),
                    "email": user.email
                }
            })
        else:
            return JsonResponse({"error": "Invalid email or password"}, status=401)
    except Exception:
        return JsonResponse({"error": "Invalid request"}, status=400)


def api_logout(request):
    logout(request)
    return JsonResponse({"success": True})


@csrf_exempt
def api_forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        data = json.loads(request.body)
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse("accounts:password_reset_confirm", args=[uid, token])
            )
            send_mail(
                subject="Reset your ZaraiLink password",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass
        return JsonResponse({"success": True})
    except Exception:
        return JsonResponse({"error": "Invalid request"}, status=400)


def api_verify_email(request, token):
    """
    Verify user's email using the token sent via email
    """
    try:
        user = User.objects.get(verification_token=token)

        if user.email_verified:
            return JsonResponse({
                "success": True,
                "message": "Email already verified. You can now login.",
                "already_verified": True
            })

        if not user.is_verification_token_valid():
            return JsonResponse({
                "error": "Verification link has expired. Please request a new one.",
                "expired": True
            }, status=400)

        # Mark email as verified and activate user
        user.email_verified = True
        user.is_active = True
        user.save(update_fields=['email_verified', 'is_active'])

        return JsonResponse({
            "success": True,
            "message": "Email verified successfully! You can now login.",
            "verified": True
        })

    except User.DoesNotExist:
        return JsonResponse({
            "error": "Invalid verification link.",
            "invalid": True
        }, status=400)


@csrf_exempt
def api_resend_verification(request):
    """
    Resend verification email to the user
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)

            if user.email_verified:
                return JsonResponse({
                    "error": "Email is already verified",
                    "already_verified": True
                }, status=400)

            # Generate new token
            user.regenerate_verification_token()

            # Send new verification email
            verification_url = request.build_absolute_uri(
                f"/accounts/api/verify-email/{user.verification_token}/"
            )
            send_mail(
                subject="Verify your ZaraiLink account",
                message=f"Welcome to ZaraiLink!\n\nPlease verify your email by clicking the link below:\n{verification_url}\n\nThis link will expire in 24 hours.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return JsonResponse({
                "success": True,
                "message": "Verification email resent successfully!"
            })

        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return JsonResponse({
                "success": True,
                "message": "If that email is registered, a verification email has been sent."
            })

    except Exception as e:
        return JsonResponse({"error": "Invalid request", "details": str(e)}, status=400)