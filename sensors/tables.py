from djflow.FlowBaseTable import FlowBaseTable
from .models import SensorData_01
from .models import SensorInfo
import django_tables2 as tables


class SensorDetailTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    class Meta:
        model = SensorInfo
        exclude = ['id']


class SensorListTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    #link = tables.Column()
    class Meta:
        model = SensorInfo
        exclude = ['id']

class SensorDataTable(FlowBaseTable):
    #name = tables.Column()
    #link = tables.Column()
    class Meta:
        model = SensorData_01
        exclude = ['id']

class AllSensorTable(FlowBaseTable):
   dtime = tables.DateTimeColumn()
   sid01 = tables.Column()
   sid02 = tables.Column()
   sid03 = tables.Column()
   sid04 = tables.Column()



## methode eines tables gewesen??
def render_labelterm(self, value):
    return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))
