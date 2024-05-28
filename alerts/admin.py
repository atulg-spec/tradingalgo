from django.contrib import admin
from alerts.models import *
from django.utils.html import format_html


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name','status_color', 'datetime', 'place_alert_button']

    def status_color(self, obj):
        if obj.status == 'completed':
            return format_html(f'<span style="color: green;">{obj.status}</span>', obj.status)
        elif obj.status == 'failed':
            return format_html(f'<span style="color: red;">{obj.status}</span>', obj.status)
        else:
            return format_html(f'<span style="color: blue;">{obj.status}</span>', obj.status)

    def place_alert_button(self, obj):
        return format_html(f'''
                           <a href='/place_alert/{obj.id}'><button type='button' class='btn btn-success'">Place Alert</button></a>
                           ''')

    place_alert_button.short_description = 'Place Alert'
    status_color.short_description = 'Status'

admin.site.register(orders, OrderAdmin)

@admin.register(IndexTokens)
class IndexTokens(admin.ModelAdmin):
    list_display = ('BANKNIFTY','CRUDEOIL','SENSEX','NIFTY')
