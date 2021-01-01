
from django.contrib import admin
from django.urls import include, path
from piheatweb import views


urlpatterns = [
#    path('', views.index, name='index'),
    path('', views.DashboardView.as_view()),

    path('admin/', admin.site.urls),
    path('sensors/', include('sensors.urls')),
    path('actors/', include('motors.urls')),
    path('users/', include('users.urls')),
]
