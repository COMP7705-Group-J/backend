import re
from pyexpat import model
from rest_framework import serializers
from .models import MyUser

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

    class Meta:
        model=MyUser
        fields=('username', 'email')
