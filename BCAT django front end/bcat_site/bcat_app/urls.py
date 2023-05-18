from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    #path('home/', views.home, name='home'),
    path('BCAT/', views.BCAT, name='BCAT'),
    #path('test/', views.test, name='test'),
    #path('api/', views.api, name='api'),
    
]
