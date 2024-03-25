from django.urls import path,include
from ironswords.views.event_views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register("",EventViewset,basename="event")

urlpatterns = router.urls