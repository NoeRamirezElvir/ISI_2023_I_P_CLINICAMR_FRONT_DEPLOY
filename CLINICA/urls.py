from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('',views.usuariologin, name='usuariologin'),
    path('',views.home, name='home'),
    path('',views.iniciomenu, name='iniciomenu'),
    path('',views.usuario, name='usuario'),
    path('',views.usuarioinicio, name='usuarioinicio'),
    path('',views.usuariolistar, name='usuariolistar'),
    path('',views.usuarioregistro, name='usuarioregistro'),
]
