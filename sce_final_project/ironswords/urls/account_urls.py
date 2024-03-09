from django.urls import path,include
from ironswords.views.account_views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("register",PhoneViewSet,basename='phone')
router.register("verify-otp",OTPViewSet,basename='otp')
router.register("update",PrefrencesViewSet,basename = "update")
urlpatterns = router.urls