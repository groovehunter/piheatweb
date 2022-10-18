
from django.contrib import admin
from django.urls import include, path
from piheatweb import views
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
#    path('', views.index, name='index'),
    path('', views.DashboardView.as_view()),

    path('admin/', admin.site.urls),
    path('sensors/', include('sensors.urls')),
    path('actors/', include('motors.urls')),
    path('motors/', include('motors.urls')),
#    path('rules/', include('rules.urls')),
    path('users/', include('users.urls')),
    path('cntrl/', include('cntrl.urls')),

]
#urlpatterns += staticfiles_urlpatterns()
