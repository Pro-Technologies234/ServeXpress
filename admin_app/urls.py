from django.urls import path
from .views import (
    admin_dashboard,manage_jobs, delete_job, update_job,
    manage_users, user_detail, create_user,
    update_user, delete_user

)

urlpatterns = [
    path("admin_app/dashboard", admin_dashboard, name="admin_dashboard"),
    path('manage_users/', manage_users, name='manage_users'),
    path('manage_user/users/create_user/', create_user, name='create_user'),
    path('manage_user/users/<int:pk>/', user_detail, name='user-detail'),
    path('manage_user/users/<int:pk>/edit_user/', update_user, name='edit_user'),
    path('manage_user/users/<int:pk>/delete/', delete_user, name='user-delete'),
    path('manage_jobs/', manage_jobs, name='manage_jobs'),
    path('manage_jobs/delete_job/<int:pk>/<str:redirect_page>/', delete_job, name='delete_job'),
    path('manage_jobs/update_job/<int:pk>/', update_job, name='update_job'),
]
