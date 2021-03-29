
import yaml
from os.path import join
from .settings import BASE_DIR, MENU_CONF

from sensors.models import SensorData_01, SensorData_02
from piheatweb.LoggingSupport import LoggingSupport


class BaseCtrl(LoggingSupport):
    """ common methods for gui """

    def yaml_load(self):
        c = open(join(BASE_DIR, MENU_CONF), encoding='utf8').read()
        self.tree = yaml.load(c, Loader=yaml.BaseLoader)

    def yamlmenu(self):
        """ create datastructure for menu rendering in template
            using menu.yaml config file """

        menudata = []

        for section in self.tree:
            #self.lg.debug('section %s', section )
            sec = list(section.values())[0]
            id = sec['id']
            #self.lg.debug('id %s', id )
            #self.lg.debug('sec %s', sec )
            if True:
                menudata.append( sec )
            else:
                cus_sec = {
                    'href'  :sec['href'],
                    'id'    :sec['id'],
                    'name'  :sec['name'],
                    'links' :[],
                }
                self.lg.debug('sec links %s', sec['links'])
                for item in sec['links']:
                    href = item['href']
                    if self.perm[id][href] == True:
                        cus_sec['links'].append(item)
                menudata.append( cus_sec )

        self.context['menudata'] = menudata
#        self.lg.debug('menudata %s', menudata)



    def access_denied(self):
        self.template = 'access_denied.html'
        return self.render()
