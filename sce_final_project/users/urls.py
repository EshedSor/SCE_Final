from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"register",PhoneViewSet,basename='phone')
router.register(r"verify-otp",OTPViewSet,basename='otp')
router.register(r"update",PrefrencesViewSet,basename = "update")
#added for cities
router.register(r"cities",CityViewSet, basename='city')
router.register(r'users',UsersViewSet)
router.register(r'friendrequests',FriendRequestViewSet)
urlpatterns = [path('account/', include(router.urls)),
               ]