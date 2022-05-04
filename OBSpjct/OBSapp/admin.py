from django.contrib import admin
from .models import *

@admin.register(map_data)
class map_dataAdmin(admin.ModelAdmin):
    list_display = ['map_name', 'map_graph', 'id']

