from distutils.command.upload import upload
from django.db import models
from django.forms import CharField

# Create your models here.
class map_data(models.Model):
    map_name = models.CharField(max_length = 100, null = True, blank = True)
    map_graph = models.TextField()
    map_image = models.ImageField(upload_to = "", null = True, blank = True)
    
    def __str__ (self):
        return self.map_name

    class Meta:
        pass