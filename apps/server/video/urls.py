from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

basename = r"attempt-set"
router.register(basename, views.AttemptSetViewSet, basename=basename)

urlpatterns = [
    path(
        "attempt/<int:question_set_id>/<int:attempt_set_id>/",
        views.CreateAttemptView.as_view(),
        name="create_attempt",
    ),
    path(
        "process/<int:attempt_set_id>/",
        views.ProcessAttemptSetView.as_view(),
        name="process_attempt",
    ),
]

urlpatterns.extend(router.urls)
