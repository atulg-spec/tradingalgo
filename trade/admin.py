from typing import Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from .models import *
from django.utils.html import format_html
from django.contrib.admin import AdminSite

@admin.register(plans)
class plans(admin.ModelAdmin):
    list_display = ('plan_type','price','discount','after_discount_price')

class adminbotquantity(admin.ModelAdmin):
    list_display = ('user', 'quantity','crudeoil_quantity','nifty_quantity','bank_nifty_quantity','fin_nifty_quantity','sensex_quantity')
admin.site.register(bot_order_quantity,adminbotquantity)

class clientprofile(admin.ModelAdmin):
    list_display = ('user', 'is_verified','number','adhaar','is_trading')

class angelAdmin(admin.ModelAdmin):
    list_display = ('apiuser', 'datetime', 'apiname', 'is_trading')
    list_filter = ('datetime', 'is_trading')
class dhanAdmin(admin.ModelAdmin):
    list_display = ('apiuser', 'datetime', 'apiname', 'is_trading')
    list_filter = ('datetime', 'is_trading')
class paisaAdmin(admin.ModelAdmin):
    list_display = ('apiuser', 'datetime', 'apiname', 'is_trading')
    list_filter = ('datetime', 'is_trading')
class fyAdmin(admin.ModelAdmin):
    list_display = ('apiuser', 'datetime', 'apiname', 'is_trading')
    list_filter = ('datetime', 'is_trading')
class alAdmin(admin.ModelAdmin):
    list_display = ('apiuser','datetime', 'apiname', 'is_trading')
    list_filter = ('datetime', 'is_trading')
admin.site.register(angelapi, angelAdmin)
admin.site.register(dhanapi, dhanAdmin)
admin.site.register(paisaapi, paisaAdmin)
admin.site.register(fyersapi, fyAdmin)
admin.site.register(aliceapi, alAdmin)
@admin.register(contactform)
class contactform(admin.ModelAdmin):
    icon_name = "call"
    list_display = ('datetime','user', 'numemail','issue')
    def has_add_permission(self, request):
        return False
    
admin.site.register(segment)
class customstrategy(admin.ModelAdmin):
    icon_name="event"
admin.site.register(strategy)
admin.site.register(ordertype)
admin.site.register(producttype)

class CustomTradebookResponsesAdmin(admin.ModelAdmin):
    icon_name="code"
    list_display = ('apiid','buy','sell','p_l','status','datetime','broker','symbol','response','apiuser','quantity')
    list_filter = ('datetime','broker', 'status','apiuser')

    def has_add_permission(self, request):
        return False
admin.site.register(tradebook, CustomTradebookResponsesAdmin)

class customwebhookurl(admin.ModelAdmin):
    icon_name = "build"
    list_display = ('custom_url','use','slot','open_time','close_time')
    def custom_url(self, obj):
        return ("https://smart-algo.in/alert/"+obj.url)
admin.site.register(webhookurl,customwebhookurl)

# PLAN
class planAdmin(admin.ModelAdmin):
    list_display = ('id', 'suscribed_date', 'user','placed_order','totalorder_perday','plan_type','active', 'expiry_date')
    list_filter = ('plan_type','suscribed_date','user','totalorder_perday','active','expiry_date')
admin.site.register(allplan, planAdmin)

class stratadmin(admin.ModelAdmin):
    list_display = ('id','user','broker','strategy','symbol','segment','status', 'datetime')
    list_filter = ('user','symbol','broker','strategy','segment','status','datetime')
admin.site.register(allstratergy, stratadmin)

class adminnews(admin.ModelAdmin):
    list_display = ('date','headline')
admin.site.register(news, adminnews)

@admin.register(Limitorder)
class Limitorder(admin.ModelAdmin):
    list_display = ('symbol','colored_limit_price','colored_current_price','crossed','cross_count','status', 'date')
    def colored_limit_price(self, obj):
        return format_html('<span style="color: blue;">{}</span>', obj.limit_price)

    colored_limit_price.short_description = 'Limit Price'
    def colored_current_price(self, obj):
        if obj.current_price > obj.limit_price:
            color = 'green'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.current_price)

    colored_current_price.short_description = 'Current Price'

# @admin.register(trailing_stoploss)
# class trailing_stoploss(admin.ModelAdmin):
#     list_display = ('symbol','current_price','stoploss','ordered_price','target','status', 'date','message')

@admin.register(trailing_stoploss)
class TrailingStoplossAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'colored_current_price', 'colored_stoploss', 'ordered_price', 'coloured_exit_avg', 'target', 'colored_status', 'date', 'message')

    def colored_current_price(self, obj):
        if obj.current_price > obj.ordered_price:
            color = 'green'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.current_price)

    colored_current_price.short_description = 'Current Price'

    def coloured_exit_avg(self, obj):
        if obj.exit_avg > obj.ordered_price:
            color = 'green'
        elif obj.exit_avg <= obj.ordered_price:
            color = 'red'
        else:
            color = 'blue'
        return format_html('<span style="color: {};">{}</span>', color, obj.exit_avg)

    coloured_exit_avg.short_description = 'Exit Avg'

    def colored_stoploss(self, obj):
        if obj.stoploss > obj.ordered_price:
            color = 'green'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.stoploss)

    colored_stoploss.short_description = 'Stoploss'

    def colored_status(self, obj):
        if obj.status == 'pending':
            color = 'blue'
        else:
            color = 'green'
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())  # Use get_status_display to show the human-readable status

    colored_status.short_description = 'Status'


# NOTIFICATION
@admin.register(Notifications)
class Notifications(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('user','date_time')
    
admin.site.register(Events)

@admin.register(tradeHistory)
class tradeHistory(admin.ModelAdmin):
    list_display = ('user','client_id','symbol','quantity','buy_avg','sell_avg','pnl','date_time','broker')
    list_filter = ('date_time','broker','user','client_id','symbol')

# UN_REGISTER
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

admin.site.unregister(Site)
admin.site.unregister(Group)


from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)


# Admin Customization
admin.site.index_title = "Smart-algo"
admin.site.site_header = "Smartalgo Admin Panel"
admin.site.site_title = "Admin Panel"
