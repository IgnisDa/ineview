from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.VideoUploadView.as_view(), name="upload_video"),
    path(
        "process/<int:video_id>", views.ProcessVideoView.as_view(), name="process_video"
    ),
]
