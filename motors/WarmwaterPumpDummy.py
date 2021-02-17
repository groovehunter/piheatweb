import time
import sys


class WarmwaterPumpCtrlDummy(object):

    def __init__(self):
      self.count = 0

    def setup(self):
      pass

    def get_status(self):
      return True

    def enable(self):
      pass

    def disable(self):
      pass

    def cleanup(self):
      pass

    def work(self, status):
      pass
