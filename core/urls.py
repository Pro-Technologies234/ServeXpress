from django.urls import path
from .views import (
    dashboard,find_jobs,my_jobs,proposals,accept_proposal

)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard" ),
    path("dashboard/", dashboard, name="dashboard" ),
    path("my_jobs/", my_jobs, name="my_jobs" ),
    path("find_jobs/", find_jobs, name="find_jobs" ),
    path("proposals/", proposals, name="proposals" ),
    path("accept_proposal/<int:proposal_id>/", accept_proposal, name="accept_proposal" ),
]
