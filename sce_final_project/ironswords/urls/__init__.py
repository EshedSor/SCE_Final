from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('account/', include("ironswords.urls.account_urls")),
    path('events/', include("ironswords.urls.event_urls")),
    path('organizations/',include("ironswords.urls.organization_urls")),
    path('shifts/', include("ironswords.urls.shift_urls")),
]