from django.shortcuts import render
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.auth import login
from .helpers import cities_api #added for cities
from django.conf import settings
from rest_framework.authtoken.models import Token

class PhoneViewSet(viewsets.ViewSet):
    authentication_classes = []
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
    authentication_classes = []  # No authentication required to access

    def create(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            # Assume the serializer provides a valid 'phone' field
            try:
                user = User.objects.get(phone = serializer.validated_data['phone'])
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message": "Successfully logged in", "token": token.key,"user_id":"{0}".format(user.id),"onboarding":"{0}".format(user.finished_onboarding)}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrefrencesViewSet(mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = PrefrencesSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        print(request.data)
        return super().update(request, *args, **kwargs)
    

#added for cities
class CityViewSet(viewsets.ViewSet): #viewset for handling city-related API request
    def list(self, request): #handle Get request to retrieve the list of cities
        cities = settings.CITY_LIST
        cityList = []  
        for i in cities: 
            cityList.append(i[0])  
        if cities is not None: #return the list of cities as a Json response
            return Response(cityList)
        else: #if cities data retrueval failed, return an error response
            return Response({"message":"error retrieving cities data"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    