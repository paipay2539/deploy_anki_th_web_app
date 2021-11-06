from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100) # normal text
    body = models.TextField() # box text
    
def __str__(self) : # to convert return value to title name each Post
        return self.title