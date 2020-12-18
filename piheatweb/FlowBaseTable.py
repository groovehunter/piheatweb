import django_tables2 as tables
from django.utils.html import format_html


css_attrs = {   "td": {"class": "p-2 border" },
                "th": {"class": "bg-blue-100 border text-left px-6 py-3"}
}

class FlowMixin(tables.Table):
#    class Meta:
    pass

class FlowBaseTable(tables.Table):
    edit    = tables.CheckBoxColumn(accessor='pk') #attrs={'input', 'ads'})
    #title   = tables.Column(linkify=True)
#    emtpy_text = 'n/a'
    def render_id(self, value):
        #return value
        return format_html('<a href="/video/topic/%s">%s</a>' %(value,value))

    def before_render(self, request):
        if not request.user.has_perm('edit'):
            self.columns.hide('edit')
