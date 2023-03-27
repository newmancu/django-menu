from django.urls import path,include
from menu import views

urlpatterns = [
  path('', views.index, name='index')    
]
