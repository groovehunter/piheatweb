from piheatweb.FlowBaseTable import FlowBaseTable
from .models import Motor
import django_tables2 as tables



class MotorListTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    class Meta:
        model = Motor
        exclude = ['id']



    def render_labelterm(self, value):
        return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))
