from piheatweb.FlowBaseTable import FlowBaseTable
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



    def render_labelterm(self, value):
        return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))
