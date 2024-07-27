from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'messages', MessageViewSet,basename='message')
router.register(r'groups', GroupViewSet)
router.register(r'group-messages', GroupMessageViewSet)
router.register(r'chats',ChatViewSet)
urlpatterns = [
    path('', include(router.urls)),
]