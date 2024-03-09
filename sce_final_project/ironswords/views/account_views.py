from django.shortcuts import render
from rest_framework import status
from ironswords.models.user_model import *
from django.shortcuts import get_object_or_404
from ironswords.serializers.account_serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.auth import login

class PhoneViewSet(viewsets.ViewSet):
    def create(self,request, *args, **kwargs):
        serializer = PhoneSerializer(data = request.data)
        if serializer.is_valid():
                user, created = User.objects.get_or_create(phone=serializer.validated_data['phone'])
                res = send_otp(user.phone)
                if 0 == res['status']:
                    status_code = status.HTTP_201_CREATED if created else status.HTTP_202_ACCEPTED
                    return Response({"message": "OTP sent."})
                else:
                    return Response("error with sending OTP",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
class OTPViewSet(viewsets.ViewSet):
    authentication_classes = []
    def create(self,request,*args, **kwargs):
        serializer = OTPSerializer(data = request.data)
        print(request.data)
        if serializer.is_valid():
            user = User.objects.get(phone = serializer.validated_data['phone'])
            login(request,user)
            request.session.cycle_key()
            session_key = request.session.session_key
            request.session.set_expiry(90 * 24 * 60 * 60)  # 90 days, in seconds
            return Response({"message":"Succesfully logged in","token":session_key},status=status.HTTP_200_OK)
        else:
            return Response({"message":"wrong otp"},status = status.HTTP_400_BAD_REQUEST)

class PrefrencesViewSet(viewsets.ModelViewSet):
    serializer_class = PrefrencesSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    http_method_names = ['patch']
    