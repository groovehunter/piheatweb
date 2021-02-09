import inspect

suffix_wanted = 'Rule'

class KlassLoader:
  """ load all classes from a file """
  def get_klasslist(self, module):
    klass_list = []
    for name, obj in inspect.getmembers(module):
      if not name.endswith(suffix_wanted):
        continue
      if inspect.isclass(obj):
        #print(name, obj)
        klass_list.append(obj.__name__)
#    if 'LightPattern' in pattern_list:
#        pattern_list.remove('LightPattern')
    return klass_list
