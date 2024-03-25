from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError

class Organization(models.Model):
    name = models.CharField(max_length = 50,blank = False,null = False)
    description = models.TextField(blank = True, null = False, default = "")
    contact_name = models.CharField(max_length = 50,blank = True,null = True,default = "")
    contact_phone = models.CharField(max_length = 10,blank = True,null = True,default = "")