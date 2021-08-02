from django.urls import path
from . import views
from .views import CheckinView

urlpatterns = [
    path('', views.index, name='index'),
    path('check_in/', CheckinView.as_view())
]
