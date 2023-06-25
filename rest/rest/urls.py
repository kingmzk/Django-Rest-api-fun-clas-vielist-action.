

from rest_framework.routers import DefaultRouter
from api.views import *
from django.urls import path,include
from django.contrib import admin


router = DefaultRouter()
router.register('Todos', Todos, basename="TodoViewSet")


urlpatterns = [
    
   path('',include(router.urls)),
   path('admin/',admin.site.urls)
]
