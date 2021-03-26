import logging
from piheatweb.settings import BASE_DIR


class LoggingSupport:
  def init_logging(self):
      self.lg = logging.getLogger('test')
      if not getattr(self.lg, 'handler_set', None):
          fh = logging.handlers.TimedRotatingFileHandler(BASE_DIR+'/log/debug.log', when='midnight')
          fmt = '%(module)s,%(lineno)d - %(levelname)s - %(message)s'
          form = logging.Formatter(fmt=fmt)
          fh.setFormatter(form)
          self.lg.addHandler(fh)
          self.lg.setLevel(logging.DEBUG)
      self.handler_set = True
