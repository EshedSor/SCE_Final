from ironswords.models import User
from ironswords.models.user_model import verify_otp
import io
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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