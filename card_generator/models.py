from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100) # normal text
    body = models.TextField() # box text
    
    auth_name  = models.CharField(max_length=100)
    deck_name  = models.CharField(max_length=100)
    comment    = models.TextField()
    input_box  = models.TextField()
    output_box = models.TextField()
    apkg_file  = models.BinaryField (blank = True, null = True, editable = True)
    
def __str__(self) : # to convert return value to deck_name each Post
    return self.deck_name