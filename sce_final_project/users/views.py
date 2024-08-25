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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.db.models import Q
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
                refresh = RefreshToken.for_user(user)
                return Response({"message": "Successfully logged in" ,"refresh": str(refresh), "token": str(refresh.access_token),"user_id":"{0}".format(user.id),"onboarding":"{0}".format(user.finished_onboarding)}, status=status.HTTP_200_OK)
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
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def update(self, request, *args, **kwargs):
        print(request.headers)
        return super().update(request, *args, **kwargs)
    def get_permissions(self):
        if self.action in []:
            print('here')
            permission_classes = [permissions.IsAuthenticated,]
        else:
            permission_classes =   [permissions.AllowAny,]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def friends(self,request):
        friends = request.user.friends.all()
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def friendrequest(self,request,pk=None):
        friend = self.get_object()
        pending_friend_request = FriendRequest.objects.filter(
            Q(sender=request.user, receiver=friend) | Q(sender=friend, receiver=request.user),
            status="pending"
        )
        # Check if they are already friends
        if self.request.user != friend:
            if not pending_friend_request.exists():
                if (not friend.friends.filter(id=self.request.user.id).exists()) and (not self.request.user.friends.filter(id=friend.id).exists()):
                    FriendRequest.objects.create(sender = request.user,receiver = friend)
                    print("friend request sent succesfully")
                    return HttpResponse({"message":"friend request sent succesfully"},status = status.HTTP_200_OK)
                print("already friends")
                return HttpResponse({"message":"already friends"},status = status.HTTP_400_BAD_REQUEST)
            print("friend request already pending")
            return HttpResponse({"message":"friend request already pending"},status = status.HTTP_400_BAD_REQUEST)
        print("cant add self")
        return HttpResponse({"message":"cant add self"},status = status.HTTP_400_BAD_REQUEST)
class FriendRequestViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(status = "pending",receiver = request.user)
        serializer = self.serializer_class(qs,many = True)
        return HttpResponse(serializer.data,status = status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def accept(self,request,pk = None):
        fr = self.get_object()
        if fr.receiver == request.user and fr.status == "pending":
            fr.receiver.friends.add(fr.sender)
            fr.sender.friends.add(fr.receiver)
            fr.status = "accepted"
            fr.save()
            return HttpResponse({"message":"friend request accepted succesfully"},status = status.HTTP_200_OK)
        return HttpResponse({"message":"invalid friend request"},status = status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def reject(self,request,pk = None):
        fr = self.get_object()
        if fr.receiver == request.user and fr.status == "pending":
            fr.status = "rejected"
            fr.save()
            return HttpResponse({"message":"friend request rejected succesfully"},status = status.HTTP_200_OK)
        return HttpResponse({"message":"invalid friend request"},status = status.HTTP_400_BAD_REQUEST)