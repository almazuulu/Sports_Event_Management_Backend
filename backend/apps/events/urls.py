from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet, SportEventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'sport-events', SportEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]