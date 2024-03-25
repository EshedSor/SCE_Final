from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from ironswords.models.organization_model import Organization
from ironswords.models.user_model import User
class Event(models.Model):
    name = models.CharField(max_length = 50,blank = False,null = False)
    description = models.TextField(blank = True, null = False, default = "")
    recurring = models.BooleanField(blank = False,null = False, default = False) #True  = Recurring, False = one Time
    max_volunteers = models.IntegerField(blank = False,null = False, default = 1)
    start_date = models.DateTimeField(blank = False,null = False)
    duration = models.DurationField(blank = False,blank = False,default = 2) #duration in hours
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE) #Many to one relation - many events related to a single organization
    volunteers = models.ManyToManyField(User)