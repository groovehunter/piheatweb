from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone

from .settings import BASE_DIR, TMPPATH, DEBUG, DEBUG2
from .BaseCtrl import BaseCtrl
#import logging


class ViewControllerSupport(BaseCtrl):
    """ lightweight ctrl methods to add abilities to django
        generic views:
        - logging
        - navigation blocks
        - custom render method
    """

    def init_ctrl(self):
        self.context = {}
        self.context['now'] = timezone.now()
        self.fields_noshow = []
        if DEBUG2:
            self.context['debug2'] = True
        self.msg = ''
        self.context['logged_in'] = True
        self.context['prefix_static'] = '/static/'
        self.context['common_static'] = '/static/'
        self.yaml_load()
        self.yamlmenu()
        self.now = timezone.now()

        if self.request.GET:
            GET = self.request.GET
            if 'msg' in GET:
                self.context['msg'] = GET['msg']

    def helper_detailview(self):
        modlabel = self.model._meta.label
        try:
            app, modl = modlabel.split('.')
        except:
            app = 'na'
            modl = modlabel

        test = 'BROKEN'
        try:
            url = self.model.get_absolute_url()
            test = 'OK'
        except:
            url = '/{0}/{1}'.format(app,modl.lower())
#            url = 'BROKEN'
        c = {
            'keys'  : self.fields,
            'url'   : url,
        }
        if DEBUG:
            c['debug'] = True
            c['test'] = test
        return c

    def listview_helper(self):
        keys = self.model._meta.get_fields()
        field_names = [k.name for k in keys]
        for f in self.fields_noshow:
            if f in field_names:
                field_names.remove(f)
        field_names.remove('id')
        (app, modl) = self.model._meta.label.split('.')
        try:
            url = self.model.get_absolute_url()
        except:
            url = '/{0}/{1}'.format(app,modl.lower())
        url_detail = url
        c = {
            'app'   : app.capitalize(),
            'modl'  : modl,
            'keys'  : field_names,
            'url'   : url,
            'url_detail': url_detail,
        }
        if DEBUG:
            c['debug'] = True
        return c

    def render(self):
        t = loader.get_template(self.template_name)
        if (hasattr(self, 'msg') and self.msg):
            self.context['msg'] = self.msg
        html = t.render(self.context, request=self.request)
        response = HttpResponse( )
        response.write(html)
        return response
