
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from accounts.views import login_view
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("jobs/", include("jobs.urls")),

    # FIXED LOGIN & LOGOUT
    path("login/", login_view, name="login"),
  path(
    "logout/",
    LogoutView.as_view(next_page="login"),
    name="logout"
),


    path("", RedirectView.as_view(url="/jobs/", permanent=False)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



