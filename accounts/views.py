from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == "recruiter":
                return redirect("jobs:dashboard")
            elif user.role == "candidate":
                return redirect("jobs:job_list")
            else:
                return redirect("jobs:list")

        else:
            messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html")
