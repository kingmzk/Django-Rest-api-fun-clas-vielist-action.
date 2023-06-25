from rest_framework import serializers
from .models import TimingTodo, Todo  
import re
from django.utils.text import slugify

class TodoSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Todo
        # fields = '__all__'
        fields = ['user','todo_title','slug','todo_description','is_done','uid']
        # exclude = ['created_at','updated_at']
        
        
    def get_slug(self,obj):
        return slugify(obj.todo_title)
        
    def validate_todo_title(self, value):
        regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        
        if len(value)<3:
            raise serializers.ValidationError("Title should be more then 3 characters")
        
        if regex.search(value):
            raise serializers.ValidationError("Todo Title cannot contain a special character")
        
        return value
            
  
class TimingTodoSerializer(serializers.ModelSerializer):
    todo = TodoSerializer()           # it removes unwanted createdat and updated at
    class  Meta: 
        model = TimingTodo  
        exclude = ['created_at', 'updated_at']    
       # depth = 1   