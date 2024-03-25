from django.contrib import admin
from ironswords.models.user_model import User
from ironswords.models.event_model import Event,Application
from ironswords.models.organization_model import Organization
# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Application)