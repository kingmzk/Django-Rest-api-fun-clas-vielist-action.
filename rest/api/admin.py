from django.contrib import admin

from .models import Todo



class adminTodo(admin.ModelAdmin): 
    list_display = ['id','todo_title','todo_description','is_done']
   
admin.site.register(Todo,adminTodo)  