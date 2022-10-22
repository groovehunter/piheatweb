from django.urls import path

from . import views
from .views import MotorListView, MotorDetailView, MotorController
from .views import MainValveHistoryView, WarmwaterPumpHistoryView
from .views import control, ww_control, rules_check, rules_list, rule_delete, rule_show, rule_edit
#from django.contrib.auth.decorators import login_required, permission_required
from .RulesController import RuleListView, RuleDetailView

urlpatterns = [
#    path('', views.index, name='index'),

    path('', MotorListView.as_view(), name='index'),
#    path('<int:pk>', MotorDetailView.as_view(), name='detail'),
    path('<int:pk>', views.show),
    path('mainvalve', MainValveHistoryView.as_view(), name='mainvalve'),
    path('mainvalve/graphmv', views.graphmv),
    path('mainvalve/control', control,),
    path('ww', WarmwaterPumpHistoryView.as_view(), name='ww'),
    path('ww/control', ww_control,),

    path('rules/check', rules_check),
#    path('rules/list', rules_list),
    path('rules/list', RuleListView.as_view()),
    path('rules/<int:pk>/delete', rule_delete, name='ruleDelete'),
    path('rules/<int:pk>/edit', rule_edit, name='ruleEdit'),
    path('rules/<int:pk>', RuleDetailView.as_view(), name='ruleShow'),
#    path('rules/<int:pk>', rule_show, name='ruleShow'),
#    path('rules/(?P<pk>\d+)/delete/', rule_delete, name='ruleDelete'),
    path('rules/delete', rule_delete),
    path('view/graph', views.graph_results),
    path('view/<str:method>', views.action),
]
