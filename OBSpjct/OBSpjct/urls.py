from django.contrib import admin
from django.urls import path
from OBSapp import views as obs
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', obs.home, name = "home"),
    path('input/', obs.input, name = "input"),
    path('get_options/', obs.get_options, name = "get_options"),
    path('end/', obs.end, name = "end"),
    path('get_map/', obs.get_map, name = "get_map"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
