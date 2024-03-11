# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
import random
from ironswords.helpers.sms_api import send_sms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.conf import settings
from enum import IntEnum
from django.core.exceptions import ValidationError

#----------------------------------------#

def generate_otp(user):
    otp = random.randint(100000, 999999)
    print("OTP : {0} !!!REMOVE AFTER TESTING".format(otp))
    user.otp = make_password(str(otp))
    user.otp_created_at = timezone.now()
    user.save()
    return otp

#----------------------------------------#

def send_otp(phone):
    user = User.objects.get(phone=phone)
    otp = generate_otp(user)
    res = send_sms(user.phone,otp)
    return res
#----------------------------------------#

def verify_otp(phone, otp):
    try:
        user = User.objects.get(phone=phone)
        if check_password(otp,user.otp):
            # Check if OTP is within validity period (e.g., 5 minutes)
            if user.otp_created_at > timezone.now() - timedelta(minutes=5):
                # OTP is valid, proceed with login or other action
                return True
            else:
                # OTP expired
                return False
        else:
            #OTP incorrect
            return False
    except User.DoesNotExist:
        #phone number incorrect
        return False
#----------------------------------------#

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)
    
#----------------------------------------#
GENDERS = {
     ('M',"Male"),
     ('F',"Female"),
 }
class VolunteerFrequency(IntEnum):
    LESS_THAN_ONCE = 1
    MORE_THAN_ONCE = 2
    WHENEVER = 3
    ONCE_A_WEEK = 0
VOLUNTEER_CATEGORIES = [
    "Packaging", #לארוז חבילות
    "Refurbishing", #לחדש בתים
    "Driving",# להסיע או לשנע
    "Handout",#לתרום ולמסור
    "Recruit",#לגייס
    "Advocacy",#כיכר החטופים
]
MOST_IMPORTANT_PREFRENCE = {
    ("Friends","להתנדב עם חברים"),
    ("Distance","קרוב לבית"),
    ("Profession","לעסוק במקצוע ובכישורים שלי"),
    ("Organization",'החמ"ל שלי')
}
def validate_categories(value):
    if not all(item in VOLUNTEER_CATEGORIES for item in value):
        raise ValidationError(f"All categories must be one of {VOLUNTEER_CATEGORIES}.")
class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=30,blank = True,null = True,default = None)
    last_name = models.CharField(max_length=30,blank = True,null = True,default = None)
    email = models.EmailField(max_length=254,blank = True,null = True,default = None)
    gender = models.CharField(max_length = 6,blank = True,null = True,default = None,choices = GENDERS)
    birth_day = models.DateField(auto_now=False, auto_now_add=False,blank = True,null = True, default = None)
    city = models.CharField(max_length=254,blank = True,null = True,default = None,choices = settings.CITY_LIST)
    volunteer_frequency = models.IntegerField(choices=[(tag, tag.value) for tag in VolunteerFrequency],blank = True,null = True,default = None)
    volunteer_categories = models.JSONField(validators=[validate_categories],blank = True,null = True,default = None)
    most_important = models.CharField(max_length=30,blank = True,null = True,default = None,choices = MOST_IMPORTANT_PREFRENCE)
    allow_notifications = models.BooleanField(default = False)
    finished_onboarding = models.BooleanField(default = False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone