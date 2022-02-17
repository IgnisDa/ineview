from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from questions import urls as questions_urls
from rest_auth import urls as rest_auth_urls
from rest_auth.registration import urls as rest_auth_registration_urls
from video import urls as video_urls


def status_check(_request):
    return JsonResponse(True, safe=False)


urlpatterns = [
    path("status", status_check, name="status_check"),
    path("admin/", admin.site.urls),
    path("rest-auth/", include(rest_auth_urls)),
    path("rest-auth/registration/", include(rest_auth_registration_urls)),
    path("video/", include(video_urls)),
    path("questions/", include(questions_urls)),
]
