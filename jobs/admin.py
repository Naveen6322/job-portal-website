from django.contrib import admin
from .models import Job
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Job._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.recruiter = request.user
        super().save_model(request, obj, form, change)

 
@admin.register(JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in JobApplication._meta.fields]
   