from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('view/<str:method>', views.action),
]



