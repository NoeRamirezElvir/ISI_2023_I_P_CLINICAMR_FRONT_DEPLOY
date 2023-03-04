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
    path('',views.empleado, name='empleado'),
    path('',views.cargo, name='cargo'),
    path('',views.especialidad, name='especialidad'),
    path('',views.documento, name='documento'),
    path('',views.buscarEmpleado, name='buscarEmpleado'), 
    path('',views.buscarDocumento, name='buscarDocumento'),
    path('',views.BuscarEspecialidad, name='BuscarEspecialidad'),

]
