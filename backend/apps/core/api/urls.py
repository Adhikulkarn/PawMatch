from django.urls import path
from apps.core.api.views import health_check

app_name = "apps.core"

urlpatterns = [
    path("health/", health_check, name="health_check"),
]
