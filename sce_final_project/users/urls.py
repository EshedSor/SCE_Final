from django.urls import path,include
from .views import *
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r"register",PhoneViewSet,basename='phone')
router.register(r"verify-otp",OTPViewSet,basename='otp')
router.register(r"update",PrefrencesViewSet,basename = "update")
#added for cities
router.register(r"cities",CityViewSet, basename='city')
urlpatterns = [path('', include(router.urls)),
               ]