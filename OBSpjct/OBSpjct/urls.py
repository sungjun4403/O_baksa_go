from django.contrib import admin
from django.urls import path
from OBSapp import views as obs
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', obs.home, name = "home"),
    path('input/', obs.input, name = "input"),
    path('get_options/', obs.get_options, name = "get_options"),
    path('end/', obs.end, name = "end"),
    path('get_map/', obs.get_map, name = "get_map"),
    #DEBUG = False 일떄도 collect static 하게 해주는 부분
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
