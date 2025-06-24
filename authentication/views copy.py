from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User
from django.db import IntegrityError

# Create your views here.
def register(request):
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data("email")
            username = form.cleaned_data("username")
            
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
                except IntegrityError:
                    messages.error(request, "An error occurred during registration. Please try again.")
        else:
            messages.error(request, "Please Correct your Details")
    else:
        form = RegisterForm()
    context = {
        "form": form,
    }
    return render(request, "authentication/create_an_account.html", context)