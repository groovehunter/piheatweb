from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .settings import TMPPATH, DEBUG, DEBUG2
from .BaseCtrl import BaseCtrl
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#import logging


class Controller(BaseCtrl):

    def __init__(self, request):
        self.context = {}
        if DEBUG2:
            self.context['debug2'] = True
        self.request = request
        self.init_ctrl()
        self.now = timezone.now()
        self.context['now'] = self.now

    def init_ctrl(self):
        self.msg = ''
        self.context['logged_in'] = True
        self.context['prefix_static'] = '/static/'
        self.context['common_static'] = '/static/'
        self.yaml_load()
        self.yamlmenu()

        if self.request.GET:
            GET = self.request.GET
            if 'msg' in GET:
                self.context['msg'] = GET['msg']


    def render(self):
        t = loader.get_template(self.template)
        html = t.render(self.context, request=self.request)
        if self.msg:
            self.context['msg'] = self.msg
        self.response = HttpResponse( )
        #self.response['Cache-Control'] = 'no-cache'
        self.response.write(html)
        return self.response

    def redirect(self, url, msg=''):
        if msg:
            url = url + '?msg=' + msg
        return HttpResponseRedirect(url)
