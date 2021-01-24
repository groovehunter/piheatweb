from piheatweb.FlowBaseTable import FlowBaseTable
from .models import Motor, MainValveHistory, WarmwaterPumpHistory
from .models import Rule, RuleHistory

import django_tables2 as tables



class MotorListTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    class Meta:
        model = Motor
        exclude = ['id']



    def render_labelterm(self, value):
        return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))


class MainValveListTable(FlowBaseTable):
  class Meta:
    model = MainValveHistory

class WarmwaterPumpListTable(FlowBaseTable):
  class Meta:
    model = WarmwaterPumpHistory


class RulesListTable(FlowBaseTable):
  class Meta:
    model = Rule
