import re
from pyexpat import model
from rest_framework import serializers
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyUserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'email') 
    
    def validate_username(self, username):
        if MyUser.objects.filter(username=username).count():
            raise serializers.ValidationError("Username already exists")
        
        return username
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class MyUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        read_only=True,
        error_messages={
            'required': "Please enter a username",
            'blank': "Username cannot be empty",
            'min_length': "Username must be at least 6 characters",
        }
    )

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model=MyUser
        fields=('username', 'email', 'password')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        old_data = super().validate(attrs)
        data = {
            'code': 200,
            'msg': 'OK',
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'access': old_data['access'],
            'refresh': old_data['refresh']
        }
        return data
    