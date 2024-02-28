# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
import random
from ironswords.helpers.sms_api import send_sms

#----------------------------------------#

def generate_otp(user):
    otp = random.randint(100000, 999999)
    user.otp = str(otp)
    user.otp_created_at = timezone.now()
    user.save()
    return otp

#----------------------------------------#

def send_otp(phone):
    user = User.objects.get(phone=phone)
    otp = generate_otp(user)
    res = send_sms(user.phone,user.otp)
    return res
#----------------------------------------#

def verify_otp(phone, otp):
    try:
        user = User.objects.get(phone=phone)
        if user.otp == otp:
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
    
class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone