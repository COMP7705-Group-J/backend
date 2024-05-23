from django.urls import path
from . import views

urlpatterns = [
    path('history', views.loadhistory),
    path('new_chat', views.newchat),
    path('list', views.list_chat),
]
