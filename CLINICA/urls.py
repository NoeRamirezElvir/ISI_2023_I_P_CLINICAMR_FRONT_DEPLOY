from django.urls import path
from . import views
from views_api import views_cargos
from views_api import views_usuarios
from views_api import views_login
from views_api import views_documento


urlpatterns = [
    path('', views.presentacion,name='presentacion'),


#####################
    path('',views.usuariosignup, name='usuariosignup'),
    path('',views_login.buscar_login, name='usuariologin'),
    path('',views_cargos.abrir_actualizar_cargos , name='abrir_actualizar_cargos'),
    path('',views_cargos.actualizar_cargo , name='actualizar_cargo'),
    path('',views_cargos.eliminar_cargo , name='eliminar_cargo'),
    path('',views_cargos.listar_cargos, name='buscarCargos'),
    path('',views_cargos.buscar_cargos, name='buscar_cargos'),
    #
    path('',views_documento.abrir_actualizar_documentos , name='abrir_actualizar_documentos'),
    path('',views_documento.actualizar_documento , name='actualizar_documento'),
    path('',views_documento.eliminar_documento , name='eliminar_documento'),
    path('',views_documento.listar_documentos, name='buscarDocumentos'),
    path('',views_documento.buscar_documentos, name='buscar_documentos'),
    path('',views_documento.crear_documento, name='crear_documento'),



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