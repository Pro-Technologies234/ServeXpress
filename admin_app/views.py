from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from authentication.models import User
from .forms import UserCreateForm, UserUpdateForm, PostJobForm, UpdateJobForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from core.models import Job, Category
from notification.models import Notification

# Create your views here.
def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
    }
    return render(request,"admin_app/dashboard.html",context)




@login_required
def manage_users(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    users = User.objects.all()
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'users': users,
    }
    return render(request, 'admin_app/manage_users.html', context)

@login_required
def user_detail(request, pk):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    user = get_object_or_404(User, pk=pk)
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'user': user,
    }
    return render(request, 'admin_app/user_detail.html', context)

@login_required
def create_user(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"User {user.username} Created successfully")
            return redirect('manage_users')
    else:
        form = UserCreateForm()
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'form': form,
    }
    return render(request, 'admin_app/create_user.html', context)

@login_required
def update_user(request, pk):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.username} updated successfully")
            return redirect('manage_users')
    else:
        form = UserUpdateForm(instance=user)
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'form': form, 
        'user': user,
    }
    return render(request, 'admin_app/edit_user.html', context)

@login_required
def delete_user(request, pk):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('manage_users')
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'user': user,
    }
    return render(request, 'admin_app/user_confirm_delete.html', context)


def manage_jobs(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("dashboard")
    jobs = Job.objects.all()
    categories = Category.objects.filter()
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    if request.method == "POST":
        category = request.POST.getlist("categories")
        post_job_form = PostJobForm(request.POST)
        if post_job_form.is_valid():
            job = post_job_form.save(commit=False)
            job.client = request.user
            job.save()
            job.categories.set(category)
            job.save()
            messages.success(request,f"Your Job was Posted Successfully.")
            return redirect("manage_jobs")
    else:
        post_job_form = PostJobForm()

    context = {
        "notifications": notifications,
        "jobs": jobs,
        "post_job_form": post_job_form,
        "categories": categories,
    }
    return render(request, "admin_app/manage_jobs.html", context)

def delete_job(request,pk,redirect_page):
    job = get_object_or_404(Job, pk=pk)
    deleted_job = job.delete()
    messages.success(request, f"Job #{job.pk} {job.title} by {job.client} ")
    return redirect(redirect_page)

def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job {job.title} updated successfully.")
            return redirect('manage_jobs')
    else:
        form = UpdateJobForm(instance=job)
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    context = {
        "notifications": notifications,
        'form': form,
        'job': job,
    }
    return render(request, 'admin_app/update_job.html', context)