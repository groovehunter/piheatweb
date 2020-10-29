from django.urls import path
from .views import SignUpView, LoginView, login, logout


urlpatterns = [
    path('signup/',     SignUpView.as_view(), name='signup'),
    path('login', login),
    path('logout', logout),

#    path('login', LoginView.as_view())
]
