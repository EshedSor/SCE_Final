from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from organizations.models import Organization
from users.models import User
class Event(models.Model):
    name = models.CharField(max_length = 50,blank = False,null = False)
    description = models.TextField(blank = True, null = False, default = "")
    recurring = models.BooleanField(blank = False,null = False, default = False) #True  = Recurring, False = one Time
    max_volunteers = models.IntegerField(blank = False,null = False, default = 1)
    start_date = models.DateTimeField(blank = False,null = False)
    duration = models.DurationField(blank = False,null = False,default = 2) #duration in hours
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE) #Many to one relation - many events related to a single organization
    volunteers = models.ManyToManyField(User,blank = True,related_name='volunteered_events')
    shift_manager = models.ForeignKey(User,blank = True,null = True,on_delete=models.PROTECT,related_name='shift_managed_events')
application_status = (
('Pending','Pending'),
('Approved','Approved'),
('Confirmed','Confirmed'),
('Declined','Declined'),
('Canceled','Canceled')
)
class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    status = models.CharField(max_length = 10,blank = False,null = False, choices = application_status,default="Pending")
    class Meta:
        unique_together = (('user', 'event'),)