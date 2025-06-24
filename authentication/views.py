from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, PasswordResetForm, SetNewPasswordForm, ChangePasswordForm, ProfileUpdateForm
from .models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.
def register(request):
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "This Email is already exist.")
            elif User.objects.filter(username=username).exists():
                messages.error(request,"User Name is already taken")
            else:
                try:
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data["password"])
                    user.save()
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    return redirect("admin_dashboard")
                except IntegrityError:
                    messages.error(request, "An error occurred during registration. Please try again.")
        else:
            messages.error(request, "Please Correct your Details")
    else:
        form = RegisterForm()
    context = {
        "form": form,
    }
    return render(request, "authentication/registration.html", context)




def log_in(request):
    isLoading = False
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            isLoading = True
            login(request, user)
            isLoading = False
            messages.success(request, f"You have been logged in successfully " )
            return redirect("admin_dashboard")
            # No redirect, just display message
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form,"isLoading": isLoading})



def logout_view(request):
    logout(request)
    return redirect('log_in')


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('set_new_password', kwargs={'uidb64': uid, 'token': token})
            )

            # Send email
            send_mail(
                subject="Reset your password",
                message=f"Click the link below to reset your password:\n{reset_url}",
                from_email=None,  # Use default from settings
                recipient_list=[user.email],
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('sign_in')
    else:
        form = PasswordResetForm()
    return render(request, 'authentication/password_reset.html', {'form': form})


def set_new_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Your password has been reset. You can now log in.")
                return redirect('sign_in')
        else:
            form = SetNewPasswordForm()
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('password_reset_request')

    return render(request, 'authentication/set_new_password.html', {'form': form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, "Your password was successfully changed.")
            return redirect('sign_in')  # Or redirect to profile/dashboard
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'authentication/change_password.html', {'form': form})


def user_profile(request):
    user = request.user
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        password_form = ChangePasswordForm(user=user)
        if "update_profile" in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("user_profile")
        elif "change_password" in request.POST:
            password_form = ChangePasswordForm(user=user, data=request.POST)
            profile_form = ProfileUpdateForm(instance=user)
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data["new_password"])
                user.save()
                messages.success(request, "Password changed successfully. Please Login again")
                return redirect("login")
    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = ChangePasswordForm(user=user)
        
    context = {
        "profile_form" : profile_form,
        "password_form" : password_form,
    }
    return render(request, "authentication/profile.html", context)