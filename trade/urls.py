from django.urls import path
from trade import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --SINGUP AND LOGIN--
    path("",views.index,name='home'),
    path("login",views.handlelogin,name='login'),
    path("logout",views.handlelogout,name='logout'),
    # --USER DASHBOARD AND PROFILE--
    path("dashboard",views.dashboard,name='dashboard'),
    path("notify",views.notify,name='notify'),
    path("apiinfo",views.apiinfo,name='apiinfo'),
    path("profile",views.profile,name='profile'),
    path("resetorder/",views.resetorder,name='resetorder'),
    # --ANGEL API--
    path("createangelapi",views.createangelapi,name='createangelapi'),
    path("saveangelapi",views.saveangelapi,name='saveangelapi'),
    path("modifyangelapi/<str:apiid>",views.modifyangel,name='modifyangel'),
    path("deleteangelapi/<str:apiid>",views.deleteangelapi,name='deleteangelapi'),
    # --DHAN API--
    path("createdhanapi",views.createdhanapi,name='createdhanapi'),
    path("modifydhanapi/<str:apiid>",views.modifydhanapi,name='modifydhanapi'),
    path("deletedhanapi/<str:apiid>",views.deletedhanapi,name='deletedhanapi'),
    # --5 PAISA API--
    path("modifypaisaapi/<str:apiid>",views.modifypaisaapi,name='modifypaisaapi'),
    path("createpaisaapi",views.createpaisaapi,name='createpaisaapi'),
    path("deletepaisaapi/<str:apiid>",views.deletepaisaapi,name='deletepaisaapi'),
    # --FYERS API--
    path("createfyersapi",views.createfyersapi,name='createfyersapi'),
    path("modifyfyersapi/<str:apiid>",views.modifyfyersapi,name='modifyfyers'),
    path("fyerslogin",views.fyerslogin,name='fyerslogin'),
    path("deletefyersapi/<str:apiid>",views.deletefyersapi,name='deletefyersapi'),
    # --ALICE BLUE API--
    path("createaliceapi",views.createaliceapi,name='createaliceapi'),
    path("modifyaliceapi/<str:apiid>",views.modifyaliceapi,name='modifyaliceapi'),
    path("deletealiceapi/<str:apiid>",views.deletealiceapi,name='deletealiceapi'),
    # --TRADING STATUS--
    path("status",views.status,name='status'),
    path("tradestatus",views.tradestatus,name='tradestatus'),
    # --HISTORY--
    path("history",views.history,name='history'),
    path("save_history",views.save_history,name='save_history'),
    # --CONTACT US--
    path("help",views.help,name='help'),
    # --WEBHOOK--
    # path("webhook/<str:url>",views.webhook,name='webhook'),
    path("alert/<str:url>",views.alert,name='alert'),
    # STRATEGY
    path("strat",views.strat,name='strat'),
    path("modifystratergy/<str:id>",views.modifystratergy,name='modifystratergy'),
    path("deletestratergy/<str:id>",views.deletestratergy,name='deletestratergy'),
    path("ststatus",views.ststatus,name='ststatus'),
    path("targetorder",views.targetorder,name='targetorder'),
    path("limit_order",views.limit_order,name='limit_order'),
    # PAGES
    path("symbols",views.symbol_search,name='symbol_search'),
    path("about",views.about,name='about'),
    path("terms",views.terms,name='terms'),
    path("pricing",views.pricing,name='pricing'),
    path("privacypolicy",views.privacypolicy,name='privacypolicy'),
    path("refundpolicy",views.refundpolicy,name='refundpolicy'),  
    path("syntax",views.syntax,name='syntax'),  
    # PLAN
    path("plan",views.plan,name="plan"),
    path("payment_success/<str:order_id>",views.payment_success,name="payment_success"),
    path("upstox_cred",views.upstox_cred,name='upstox_cred'),
    # TEST URLS
    path("test",views.test,name="test"),
    path("automatedstratergy",views.automatedstratergy,name="automatedstratergy"),
    path("activate_stratergy",views.activate_stratergy,name="activate_stratergy"),
]
