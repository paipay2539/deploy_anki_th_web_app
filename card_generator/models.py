from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True) # มันจะไปหยุด gen id เองทำให้เราคุม idได้เอง
    
    title = models.CharField(max_length=100) # normal text
    body = models.TextField() # box text
    
    auth_name  = models.CharField(max_length=100)
    deck_name  = models.CharField(max_length=100)
    comment    = models.TextField()
    output_box = models.TextField()
    output_num = models.IntegerField()
    apkg_file  = models.BinaryField (blank = True, null = True, editable = True)
    lang_log   = models.CharField(max_length=2)
    sound_log  = models.BooleanField()
    exact_log  = models.BooleanField()
    timestamp  = models.CharField(max_length=100)
    
def __str__(self) : # to convert return value to deck_name each Post
    return self.deck_name