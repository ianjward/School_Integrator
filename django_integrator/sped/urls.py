from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_file, name='sped_add_file'),
]