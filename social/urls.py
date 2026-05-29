from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crear/', views.crear_post, name='crear_post'),
    path('register/', views.register, name='register'),
path('register/', views.register, name='register'),
]