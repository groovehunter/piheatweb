
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
#from users.models import CustomUser

#from .forms import CustomUserCreationForm, CustomUserEditForm
from .UserController import UserController


def login(request):
    ctrl = UserController(request)
    return ctrl.login_user()

def logout(request):
    ctrl = UserController(request)
    return ctrl.logout_user()

class SignUpView(CreateView):
#    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('users/login.html')
    else:
        form = AuthenticationForm()
    return render(request,'user/login.html', {'form':form})
