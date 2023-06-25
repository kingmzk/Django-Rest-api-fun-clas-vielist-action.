

from rest_framework import status, viewsets
from .models import *
from .serializer import TodoSerializer
from django.urls import path
from .views import *


# Create the router and register the viewset


# Define the initial urlpatterns list
urlpatterns = [
    # Uncomment the desired URL patterns and remove the rest if not needed
    # path('', home, name="home"),
    # path('post-todo', post_todo, name="post_todo"),
    # path('get-todo', get_todo, name="get_todo"),
    # path('patch-todo', patch_todo, name="patch_todo"),
    # path('delete-todo', delete_todo, name="delete-todo"),
    path('todo/',TodoView.as_view())
    
]








# from rest_framework.routers import DefaultRouter
# # from rest_framework import routers
# from .views import TodoViewSet
# from django.urls import path,include


# router = DefaultRouter()
# router.register('todo-view-set', TodoViewSet, basename="TodoViewSet")


# urlpatterns = [
#    path('',include(router.urls)),
   
# ]

# urlpatterns += router.urls