from django.urls import path
from . import views
from views_api import views_cargos
from views_api import views_usuarios


urlpatterns = [
    path('', views.presentacion,name='presentacion'),
    path('',views.usuariologin, name='usuariologin'),
    path('',views.home, name='home'),
    path('',views.iniciomenu, name='iniciomenu'),
    path('',views.usuario, name='usuario'),
    path('',views.inicio, name='inicio'),

    path('',views_usuarios.listar_usuarios, name='listar'),
    path('',views_usuarios.buscar_usuarios, name='buscar_usuarios'),
    path('',views_cargos.crear_cargo, name='crear_cargo'),
    path('',views_usuarios.crear_usuario , name='crear_usuario'),
    path('',views_usuarios.abrir_actualizar_usuarios , name='abrir_actualizar_usuarios'),
    path('',views_usuarios.actualizar_usuario , name='actualizar_usuario'),
    path('',views_usuarios.eliminar_usuario , name='eliminar_usuario'),

    path('',views.buscarDocumento, name='lista_documentos'),
    path('',views.BuscarEspecialidad, name='lista_especialidades'),
    
    path('',views.empleado, name='empleado'),
    
    path('',views.especialidad, name='especialidad'),
    path('',views.documento, name='documento'),
    path('',views.buscarEmpleado, name='buscarEmpleado'), 
    

]
#path('',views.cargo, name='cargo'),