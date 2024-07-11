from django.urls import path,include
from ironswords.views.organization_views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register("",OrganizationViewset,basename="event")

urlpatterns = router.urls