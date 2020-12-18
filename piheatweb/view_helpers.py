from sstkvideo.settings import DEBUG, TMPPATH
import logging

class GenericFlow:
    def listview_helper(self):
        keys = self.model._meta.get_fields()
        field_names = [k.name for k in keys]
        for f in self.fields_noshow:
            field_names.remove(f)
        (app, modl) = self.model._meta.label.split('.')
        c = {
            'app'   : app.capitalize(),
            'modl'  : modl,
            'keys'  : field_names,
        }
        if DEBUG:
            c['debug'] = True
        return c


def init_logging():
    lg = logging.getLogger('test')
    return lg

    fh = logging.handlers.TimedRotatingFileHandler(TMPPATH+'/log/debug.log', when='midnight')
    fmt = '%(module)s,%(lineno)d - %(levelname)s - %(message)s'
    form = logging.Formatter(fmt=fmt)
    fh.setFormatter(form)
    lg.addHandler(fh)

    lg.setLevel(logging.DEBUG)
    return lg
