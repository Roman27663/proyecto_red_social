from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crear/', views.crear_post, name='crear_post'),
    path('register/', views.register, name='register'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comentar/<int:post_id>/', views.crear_comentario, name='crear_comentario'),
]