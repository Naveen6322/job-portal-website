from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Job,JobApplication
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .decorators import recruiter_required
from django.contrib import messages
from django.db.models import Count


@login_required
def recruiter_dashboard(request):
  if request.user.role != "candidate":
    return HttpResponse("Access Denied")

    return HttpResponse("Welcome Recruiter")


@login_required
def job_list(request):
    if request.user.role != "candidate":
        return render(request, "jobs/not_allowed.html")

    jobs = Job.objects.all().order_by("-created_at")

    applied_jobs = JobApplication.objects.filter(
        applicant=request.user
    ).values_list("job_id", flat=True)

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "applied_jobs": applied_jobs,
        }
    )

@login_required
def apply_job(request, job_id):
   if request.user.role != "candidate":

    return render(request, "403.html")

    job = get_object_or_404(Job, id=job_id)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    JobApplication.objects.get_or_create(
        job=job,
        applicant=request.user
    )

    return render(request, "jobs/applied.html")

@login_required
def dashboard(request):
    return render(request, "jobs/dashboard.html")



@login_required
@recruiter_required
def dashboard(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, "jobs/dashboard.html", {"jobs": jobs})

@login_required
@recruiter_required
def create_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Job.objects.create(
            title=title,
            description=description,
            recruiter=request.user
        )
        return redirect("jobs:dashboard")

    return render(request, "jobs/create_job.html")

@login_required
def apply_job(request, job_id):
    if request.user.role != "candidate":
        return redirect("jobs:list")

    job = get_object_or_404(Job, id=job_id)

    JobApplication.objects.get_or_create(
        job=job,
        applicant=request.user
    )

    return redirect("jobs:list")

@login_required
def apply_job(request, job_id):
    if request.user.role != "candidate":
        return redirect("jobs:job_list")

    if request.method == "POST":
        job = get_object_or_404(Job, id=job_id)

        JobApplication.objects.get_or_create(
            job=job,
            applicant=request.user
        )

        messages.success(request, "Applied successfully!")
        return redirect("jobs:job_list")

@login_required
def apply_job(request, job_id):
    if request.user.role != "candidate":
        return render(request, "jobs/not_allowed.html")

    job = get_object_or_404(Job, id=job_id)

    # ❌ Prevent duplicate application
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You already applied for this job.")
        return redirect("jobs:job_list")

    JobApplication.objects.create(
        job=job,
        applicant=request.user
    )

    messages.success(request, "Job applied successfully!")
    return redirect("jobs:job_list")
    
@login_required
def job_applications(request, job_id):
    if request.user.role != "recruiter":
        return render(request, "jobs/not_allowed.html")

    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = JobApplication.objects.filter(job=job)

    return render(
        request,
        "jobs/job_applications.html",
        {
            "job": job,
            "applications": applications
        }
    )

@login_required
def dashboard(request):
    if request.user.role != "recruiter":
        return render(request, "jobs/not_allowed.html")

    jobs = Job.objects.filter(recruiter=request.user)

    return render(request, "jobs/dashboard.html", {
        "jobs": jobs
    })

@login_required
def dashboard(request):
    if request.user.role != "recruiter":
        return render(request, "jobs/not_allowed.html")

    jobs = (
        Job.objects.filter(recruiter=request.user)
        .annotate(application_count=Count("applications"))
    )

    return render(request, "jobs/dashboard.html", {"jobs": jobs})

@login_required
def my_applications(request):
    if request.user.role != "candidate":
        return render(request, "jobs/not_allowed.html")

    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related("job")

    return render(
        request,
        "jobs/my_applications.html",
        {"applications": applications}
    )


@login_required
def accept_application(request, app_id):
    application = get_object_or_404(
        JobApplication,
        id=app_id,
        job__recruiter=request.user
    )
    application.status = "accepted"
    application.save()
    return redirect("jobs:job_applications", job_id=application.job.id)


@login_required
def reject_application(request, app_id):
    application = get_object_or_404(
        JobApplication,
        id=app_id,
        job__recruiter=request.user
    )
    application.status = "rejected"
    application.save()
    return redirect("jobs:job_applications", job_id=application.job.id)

@login_required
def my_applications(request):
    if request.user.role != "candidate":
        return render(request, "jobs/not_allowed.html")

    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related("job").order_by("-applied_at")

    return render(
        request,
        "jobs/my_applications.html",
        {"applications": applications}
    )

    messages.success(request, "Job applied successfully!")
    return redirect("jobs:job_list")

@login_required
def apply_job(request, job_id):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can apply.")
        return redirect("jobs:job_list")

    job = get_object_or_404(Job, id=job_id)

    already_applied = JobApplication.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if already_applied:
        messages.warning(request, "You already applied for this job.")
        return redirect("jobs:job_list")

    JobApplication.objects.create(
        job=job,
        applicant=request.user,
        status="pending"
    )

    messages.success(request, "Job applied successfully!")
    return redirect("jobs:job_list")

@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(JobApplication, id=app_id)

    if request.user != application.job.recruiter:
        messages.error(request, "Not authorized.")
        return redirect("jobs:dashboard")

    application.status = status
    application.save()

    messages.success(request, f"Application {status.capitalize()}!")
    return redirect("jobs:dashboard")

