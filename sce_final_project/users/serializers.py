from .models import verify_otp
from rest_framework import serializers
from .models import User,FriendRequest
from django.conf import settings

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    def validate_phone(self,value):
        if not len(value) == 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value
    def to_internal_value(self, data):
        known_keys = set(self.fields.keys())
        input_keys = set(data.keys())
        if not known_keys.issuperset(input_keys):
            extra_keys = input_keys - known_keys
            raise serializers.ValidationError(f"Unexpected fields: {', '.join(extra_keys)}")
        return super().to_internal_value(data)
    
class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length = 6)
    class Meta:
            fields = ['phone','otp']

    def validate_phone(self,value):
        if not len(value) == 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value
    
    def validate(self,value):
        phone = value.get('phone')
        otp = value.get('otp')
        if verify_otp(phone,otp):
            return value
        else:
            raise serializers.ValidationError("OTP incorrect or timed out")
        
 #added for cities
class CityField(serializers.CharField): 
    def __init__(self, **kwargs): #initialize the CityField
        super().__init__(**kwargs)
        self.cities = settings.CITY_LIST #load cities data when initializing the field

    def to_internal_value(self,data): #validate the provided city name
        if data not in self.cities: #check if the provided city name is in the loaded cities list
            raise serializers.ValidationError("Invalid city")
        return data
    
    def refresh_cities(self): #refresh the list of cities
        self.cities = settings.CITY_LIST  

class PrefrencesSerializer(serializers.ModelSerializer):
    #city = CityField() #use the custom CityField for the 'city' field
    class Meta:
        model = User
        fields = ['first_name','last_name','email','gender','birth_day','city','volunteer_frequency','volunteer_categories','most_important','allow_notifications','finished_onboarding']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'