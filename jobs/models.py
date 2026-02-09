from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant} → {self.job}"
