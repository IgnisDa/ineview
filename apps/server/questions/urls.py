from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

basename = r"questions-set"
router.register(basename, views.QuestionSetViewSet, basename=basename)

basename = r"questions"
router.register(basename, views.QuestionViewSet, basename=basename)

urlpatterns = []
urlpatterns.extend(router.urls)
