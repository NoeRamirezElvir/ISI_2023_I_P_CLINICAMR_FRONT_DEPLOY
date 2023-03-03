from django.urls import path
from . import views

urlpatterns = [
    path('', views.presentacion,name='presentacion'),
    path('',views.usuariologin, name='usuariologin'),
    path('',views.home, name='home'),
    path('',views.iniciomenu, name='iniciomenu'),
    path('',views.usuario, name='usuario'),
    path('',views.inicio, name='inicio'),
    path('',views.listar, name='listar'),
    path('',views.registro, name='registro'),
]
