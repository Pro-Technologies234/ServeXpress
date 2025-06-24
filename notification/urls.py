from django.urls import path
from .views import notification, mark_as_read, mark_all_as_read

urlpatterns = [
    path("notification/", notification, name="notification"),
    path("mark_as_read/<int:notification_id>/<str:redirect_url>/", mark_as_read, name="mark_as_read"),
    path("mark_all_as_read/<str:redirect_url>/", mark_all_as_read, name="mark_all_as_read")
]
