from django.contrib import admin
from django.urls import include, path
from questions import urls as questions_urls
from video import urls as video_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("video/", include(video_urls)),
    path("questions/", include(questions_urls)),
]
