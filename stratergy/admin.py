from django.contrib import admin
from .models import *
from django.shortcuts import redirect
import urllib.parse
from threading import Thread
from django.utils.html import format_html

# Register your models here.

@admin.register(Alert)
class Alert(admin.ModelAdmin):
    list_display = ('symbol_name','stratergy','start_time','ltp','high','low','last_volume','position_status','function')
    fieldsets = (
        (None, {'fields': ('user','stratergy')}),
        ('Syntax Info', {'fields': ('buy_syntax','sell_syntax')}),
        ('Symbol Info', {'fields': ('token','symbol_name','symbol','start_time','end_time', 'high','low' ,'target','function')}),
        ('Automated Info - Leave it blank', {'fields': ('ltp','current_volume','last_volume', 'gap','position_status')}),
    )

@admin.register(Dhan_Settings)
class Dhan_Settings(admin.ModelAdmin):
    list_display = ('client_id','place_alert_button')
    fieldsets = (
        ('Credentials', {'fields': ('client_id','access_token')}),
    )
    def place_alert_button(self, obj):
        if obj.is_active:
            return format_html(f'''
                           <a href='/activate_stratergy'><button type='button' class='btn btn-success'">Active</button></a>
                           ''')
        else:
            return format_html(f'''
                           <a href='/activate_stratergy'><button type='button' class='btn btn-danger'">Inactive</button></a>
                           ''')



@admin.register(StratergyAlert)
class StratergyAlert(admin.ModelAdmin):
    list_display = ('symbol','stratergy','start_time','ltp','high','low','bid_Qty','ask_Qty','position_status','function')
    fieldsets = (
        (None, {'fields': ('user','stratergy')}),
        ('Syntax Info', {'fields': ('buy_syntax','sell_syntax')}),
        ('Symbol Info', {'fields': ('token','segment','start_time','end_time', 'high','low' ,'target','function')}),
    )

@admin.register(Executed_Stratergy)
class Executed_Stratergy(admin.ModelAdmin):
    list_display = ('symbol','remark','datetime')


@admin.register(Stratergy_settings)
class Stratergy_settings(admin.ModelAdmin):
    list_display = ('client_id','url','place_alert_button')
    def response_change(self, request, obj):
        from stratergy.symbols.details import get_market_data
        if get_market_data('NSE_EQ|INE062A01020') is None:
            self.message_user(request, "Stratergy activated successfully.")
            return redirect(f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={obj.api_key}&redirect_uri={urllib.parse.quote(obj.redirect_uri)}')
        else:
            from trade.views import update_data
            thread = Thread(target=update_data)
            thread.start()
            self.message_user(request, "Stratergy activated successfully.")
            return redirect('/admin/stratergy/alert/')
    def place_alert_button(self, obj):
        if obj.is_active:
            return format_html(f'''
                           <a href='/automatedstratergy'><button type='button' class='btn btn-success'">Active</button></a>
                           ''')
        else:
            return format_html(f'''
                           <a href='/automatedstratergy'><button type='button' class='btn btn-danger'">Inactive</button></a>
                           ''')

