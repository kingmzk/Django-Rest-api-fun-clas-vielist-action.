from django.shortcuts import render
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import viewsets


class Todos(viewsets.ReadOnlyModelViewSet):
    queryset = Todo.objects.all()  
    serializer_class = TodoSerializer


