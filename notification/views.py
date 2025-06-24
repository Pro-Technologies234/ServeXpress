from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
# Create your views here.
def notification(request):
    notifications = Notification.objects.filter(user=request.user,is_read=False)
    return render(request,"notifications.html",{"notifications": notifications})

def mark_as_read(request,notification_id,redirect_url):
    notification = get_object_or_404(Notification,id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect(redirect_url)

def mark_all_as_read(request,redirect_url):
    notifications = Notification.objects.filter(user=request.user)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return redirect(redirect_url)