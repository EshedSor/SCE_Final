from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'messages', MessageViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'group-messages', GroupMessageViewSet)
urlpatterns = [
    path('', include(router.urls)),
]