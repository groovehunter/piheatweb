from piheatweb.FlowBaseTable import FlowBaseTable
from .models import Sensor, Measurement
import django_tables2 as tables


class SensorTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    class Meta:
        model = Sensor
        exclude = ['id']


class SensorListTable(FlowBaseTable):
    class Meta:
        model = Sensor
        exclude = ['id']


 
    def render_labelterm(self, value):
        return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))
