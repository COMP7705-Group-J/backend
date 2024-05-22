from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create),
    path('detail', views.detail),
    path('list', views.list),
    path('delete', views.delete),
]