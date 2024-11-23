from django.urls import path
from . import views  # .represent the current directory

urlpatterns = [
    path('', views.index, name='index')
]
