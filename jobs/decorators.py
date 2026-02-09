from django.shortcuts import redirect
from django.contrib import messages

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "recruiter":
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Recruiter only.")
        return redirect("login")
    return wrapper
