from djflow.Controller import Controller
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout

class UserController(Controller):

    def __init__(self, request):
        Controller.__init__(self, request)

    def login_user(self):
        request = self.request
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return self.redirect('/')
        else:
            form = AuthenticationForm()
        self.context['form'] = form
        self.template_name = 'users/login.html'
        return self.render()


    def logout_user(self):
        request = self.request
        logout(request)
        return self.redirect('/', msg='succesful logout')
