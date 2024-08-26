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
    
    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')

        # Fetch the user and print their OTP for debugging
        try:
            user = User.objects.get(phone=phone)
            print(f"User OTP: {user.otp}")  # Add this for debugging

            if user.otp is None:
                raise serializers.ValidationError("OTP has not been set for this user.")
            
            if verify_otp(phone, otp):
                return data
            else:
                raise serializers.ValidationError("OTP incorrect or timed out.")
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this phone does not exist.")
        
 #added for cities
class CityField(serializers.CharField): 
    def __init__(self, **kwargs): #initialize the CityField
        super().__init__(**kwargs)
        self.cities =  [city[0].strip().lower() for city in  settings.CITY_LIST] #load cities data when initializing the field

    def to_internal_value(self,data): #validate the provided city name
        if data not in self.cities: #check if the provided city name is in the loaded cities list
            print("invalid city")
            raise serializers.ValidationError("Invalid city")
        return data.city
    
    def refresh_cities(self): #refresh the list of cities
        self.cities =[city[0].strip().lower() for city in  settings.CITY_LIST] #load cities data when initializing the field

class PrefrencesSerializer(serializers.ModelSerializer):
    #city = CityField() #use the custom CityField for the 'city' field
    class Meta:
        model = User
        fields = ['first_name','last_name','email','gender','birth_day','city','volunteer_frequency','volunteer_categories','most_important','allow_notifications','finished_onboarding','phone']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","last_name"]

class FriendRequestSerializer(serializers.ModelSerializer):
    receiver = UserFriendRequestSerializer()
    sender = UserFriendRequestSerializer()
    class Meta:
        model = FriendRequest
        fields = ["id", "receiver", "sender", "status"]