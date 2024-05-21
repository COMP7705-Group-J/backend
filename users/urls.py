from django.urls import path, re_path
from .views import MyUserViewSet

user_list = MyUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = MyUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('register/', user_list),
    path('users/<pk>/', user_detail),
]
