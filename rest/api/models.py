from django.db import models

class Todo(models.Model):
      todo_title = models.CharField(max_length=100)
      todo_description = models.TextField()
      is_done = models.BooleanField(default=False)