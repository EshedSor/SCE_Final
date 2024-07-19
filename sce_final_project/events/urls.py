from django.urls import path,include
from .views import *
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r"events",EventViewset,basename="event")
router.register(r"shifts",ShiftViewSet,basename="shift")

urlpatterns = [
            path('', include(router.urls)),
    ]