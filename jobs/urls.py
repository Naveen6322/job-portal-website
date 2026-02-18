from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    # job seeker
    path("", views.job_list, name="job_list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),

    # recruiter
    path("recruiter/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_job, name="create"),
    path("applications/<int:job_id>/", views.job_applications, name="job_applications"),
    path("application/accept/<int:app_id>/", views.accept_application, name="accept_application"),
    path("application/reject/<int:app_id>/", views.reject_application, name="reject_application"),
    path("application/<int:app_id>/<str:status>/", views.update_application_status, name="update_application_status"),
]
