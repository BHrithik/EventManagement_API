from django.shortcuts import render
from .models import Event, User, Account
from .serializers import SignupSerializer,UserSerializer,EventSerializer,SingleEventSerializer,UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models.signals import post_save

@api_view(['POST',])
def SignUpView(request):
	serializer = SignupSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		Account=serializer.save()
		data['response'] = "sucessfully resgistered"
		data['email']    = Account.email
		data['username'] = Account.username
		token            = Token.objects.get(user=Account).key
		data['token']    = token
	else:
		data = serializer.errors
	return Response(data)

################################################################ Event List ####################################################################################
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def event_list(request):
    if request.method == 'GET':
        return get_request(request)
    elif(request.method == 'POST'):
        return post_request(request)

def post_request(request):
    serializers = EventSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

def get_request(request):
    event = Event.objects.all()
    serializers = EventSerializer(event,many=True)
    return Response(serializers.data)

############################################################## Single Event #########################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_event(request,pk):
    users_all = User.objects.all().filter(userEvents=pk)
    serializers = SingleEventSerializer(users_all,many=True)
    return Response(serializers.data)

############################################################## Event Details #########################################################################
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def event_details(request,pk):
    try:
        event = Event.objects.get(pk=pk)
    except event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user=request.user
    if request.method == 'GET':
       return get_request_event_details(request,event)
    elif request.method == 'PUT':
        return put_request_event_details(request,event) 
    elif request.method == 'DELETE':
        return delete_request_event_details(request,event)


def  get_request_event_details(request,Event):  
    serializers = EventSerializer(Event)
    return Response(serializers.data)  

def  put_request_event_details(request,Event):  
    serializers = EventSerializer(Event,request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

def  delete_request_event_details(request,Event):  
    Event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 
  
############################################################## User List ##############################################################################
@api_view(['GET','POST'])   
@permission_classes([IsAuthenticated])
def users_list(request):
    if request.method == 'GET':
        return get_users_list(request)
    elif(request.method == 'POST'):
        return post_users_list(request)
        
def get_users_list(request):
    users = User.objects.all()
    serializers = UserSerializer(users,many=True)
    return Response(serializers.data)

def post_users_list(request):
    serializers = UserSerializer(data=request.data)
    if serializers.is_valid():
        c=0
        for i in request.data['userEvents']:
            c=c+1
            a=Event.objects.get(eventID=i)
            count=a.eventVacancies
            if count>0:
                count=count-1
                a.eventVacancies=count
                a.save()
            else:
                return Response({"error": "Event capacity is full"}, status=status.HTTP_204_NO_CONTENT)
            if c>3:
                return Response({"userEvents":"User cannot take part in more than 3 events"},status=status.HTTP_204_NO_CONTENT)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
############################################################## User Details #########################################################################
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def user_details(request,pk):
    try:
        user = User.objects.get(userID=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return get_request_user_details(request,user)
    elif request.method == 'PUT':
        return put_request_user_details(request,user)
    elif request.method == 'DELETE':
         return delete_request_user_details(request,user)

def get_request_user_details(request,user):
    serializers = UserSerializer(user)
    return Response(serializers.data)

def put_request_user_details(request,user):
    serializers = UserSerializer(user,request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


def delete_request_user_details(request,user):
    event=User.userEvents.values_list('pk', flat=True)
    for i in event.iterator():
        a=Event.objects.get(eventID=i)
        count=a.eventVacancies
        count=count+1
        a.eventVacancies=count
        a.save()
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

   

