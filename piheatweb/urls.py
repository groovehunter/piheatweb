
from django.contrib import admin
from django.urls import include, path
from piheatweb import views


urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', admin.site.urls),
    path('sensors/', include('sensors.urls')),
    path('motors/', include('motors.urls')),
    path('users/', include('users.urls')),
]
