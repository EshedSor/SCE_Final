from django.urls import path,include
from events.views import *
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r"events",EventViewset,basename="event")
router.register(r"shifts",ShiftViewSet,basename="shift")
router.register(r"applications",OrganizationApplicationViewSet,basename="shift")
urlpatterns = [
            path('', include(router.urls)),
    ]