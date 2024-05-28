from django.urls import path
from alerts import views

urlpatterns = [
    path("place_alert/<str:id>",views.place_alert,name='place_alert'),
]
