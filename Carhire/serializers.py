from .models import Booking, Car
from rest_framework import serializers, validators
from django.contrib.auth.models import User


class Carserializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        extra_kwargs ={
            "password1":{"write_only":True},
            "password2":{"write_only":True},
             'email':{
                'required ': True,
                'allow_blank': False,
                'validators':[
                    validators.UniqueValidator(
                        User.objects.all(), 'User with that email already exist.'
                    )
                ]
             }
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password1 = validated_data.get('password1')
        password2 = validated_data.get('password2')

        user = User.objects.create(
            username = username,
            email = email,
            passowrd1 = password1,
            password2 = password2
        )
        return user