from tkinter import E
from django.shortcuts import render

# Create your views here.
from .models import MyUser
from .serializer import MyUserRegSerializer, MyUserUpdateSerializer
from .custommodelviewset import CustomModelViewSet
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# from notebook.auth.security import set_password
from django.contrib.auth import authenticate, get_user_model, login, logout

from rest_framework_extensions.cache.mixins import CacheResponseMixin
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication  
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework import permissions

myuser = get_user_model()
class MyUserViewSet(CacheResponseMixin, CustomModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserRegSerializer

    authentication_classes = (
        JWTAuthentication,
        SessionAuthentication,
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return MyUserRegSerializer
        elif self.action == 'retrieve':
            return MyUserUpdateSerializer
        elif self.action == 'update':
            return MyUserUpdateSerializer
        
        return MyUserUpdateSerializer
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update':
            return [permissions.IsAuthenticated()]
        else:
            return []

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            myuser = MyUser.objects.get(Q(username=username) | Q(email=username))
            if myuser.check_password(password):
                return myuser
        except Exception as e:
            return None

