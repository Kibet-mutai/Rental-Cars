from datetime import datetime
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import BookSerializer, Carserializer,SignupSerializer
from rest_framework import filters
from django.contrib.auth.models import User
from .models import Booking, Car
from .filters import CarFilter
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
def Index(request):
    cars = Car.objects.all()
    serializer = Carserializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
def CarView(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = Carserializer(cars,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Carserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','PUT','DELETE'])
def DetailView(request,id):

    """Retrieve, Update, Delete"""
    try:
        cars = Car.objects.get(id=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Carserializer(cars)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Carserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cars.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def booking_detail(request,id):
    """"
Retrieve,Update Cancel Hiring cars"""
    try:
        reserve = Booking.objects.get(id=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(reserve)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            current_date = datetime.now()
            hire_date = serializer.validated_data['hire_date']
            return_date = serializer.validated_data['return_date']
            car = serializer.validated_data['car']
            bookings = Booking.objects.all()
            for i in bookings:
                if i.hire_date <=hire_date <= i.return_date:
                    message = {"message":"car is unavailable at the moment"}
                    return Response(data=json.dumps(message), status = status.HTTP_400_BAD_REQUEST)
            
            if current_date <=hire_date and hire_date <= return_date:
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method =='DELETE':
        reserve.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def book_car(request):
    """reservation list reserve available car"""

    if request.method == 'GET':
        reserve = Booking.objects.all()
        serializer = BookSerializer(reserve, many=True)
        return Response(serializer.data) 
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            current_date = datetime.now()
            hire_date = serializer.validated_data['hire_date']
            return_date = serializer.validated_data['return_date']
            car = serializer.validated_data['car']
            bookings = Booking.objects.all()
            for i in bookings:
                if i.hire_date <=hire_date <= i.return_date:
                    message = {"message":"car is unavailable at the moment"}
                    return Response(data=json.dumps(message), status = status.HTTP_400_BAD_REQUEST)
            
            if current_date <=hire_date and hire_date <= return_date:
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  





@api_view(['POST'])
def login_api(request):
    serializer =  AuthTokenSerializer(data=request.dat)
    serializer.is_valid(raise_exceptions=True)
    user = serializer.validated_data['user']


    created, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
            'id':user.id,
            'username': user.username,
            'email':user.email
            },
        'token': token
    })

@api_view(['GET'])
def get_user_data(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            return Response({
                'user_info': {
                    'id':user.id,
                    'username': user.username,
                    'email':user.email
                    }
        })
    return Response({'errors':'null'},status=status.HTTP_400_BAD_REQUEST) 



@api_view(['POST'])
def register(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exceptions=True)

    user = serializer.save()

    created, token = AuthToken.objects.create(user)
    
    return Response({
        'user_info':{
            'id':user.id,
            'username': user.username,
            'email':user.email
            },
        'token': token
    })




@api_view(['GET'])
def get_car(request):
    params = request.query_params
    print("Parameters", params)
    if "names" in params:
        car_obj = Car.objects.filter(Q(name__icontains=params["name"]) | Q(city__icontains=params["city"]) | Q(capacity__icontains=params["capapcity"]))
        serializer = Carserializer(car_obj, many=True)
        return Response(serializer.data)
    else:
        cars = Car.objects.all()
        serializer = Carserializer(cars, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_objects(request):
    queryset = Car.objects.all()
    filterset = CarFilter(request.GET, queryset=queryset)
    if filterset.is_valid():
        queryset = filterset.qs
        print('city')
    serializer = Carserializer(queryset, many=True)
    return Response(serializer.data)
