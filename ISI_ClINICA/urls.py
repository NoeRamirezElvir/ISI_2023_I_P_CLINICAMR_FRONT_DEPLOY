"""ISI_ClINICA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from CLINICA.views import *
from CLINICA.views_api.views_usuarios import *
from CLINICA.views_api.views_documento import *
from CLINICA.views_api.views_cargos import *
from CLINICA.views_api.views_especialidades import *
from CLINICA.views_api.views_empleados import *
from CLINICA.views_api.views_cargos import *
from CLINICA.views_api.views_documento import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', presentacion),

###################
    path('CLINICA/templates/presentacion/usuariosignup.html',usuariosignup, name="usuariosignup"),
    path('CLINICA/templates/presentacion/usuariologin.html',usuariologin, name="buscar_login"),
    path('CLINICA/templates/cargoactualizar.html',abrir_actualizar_cargos,name="abrir_actualizar_cargos"),
    path('CLINICA/templates/cargoactualizar.html/<int:id>',actualizar_cargo,name="actualizar_cargo"),
    path('CLINICA/templates/buscarCargo.html/<int:id>',eliminar_cargo,name = 'eliminar_cargo'),
    path('CLINICA/templates/buscarCargo.html',buscar_cargos,name = 'buscar_cargos'),
    ##
    path('CLINICA/templates/documentoactualizar.html',abrir_actualizar_documentos,name="abrir_actualizar_documentos"),
    path('CLINICA/templates/documentoactualizar.html/<int:id>',actualizar_documento,name="actualizar_documento"),
    path('CLINICA/templates/buscarDocumento.html/<int:id>',eliminar_documento,name = 'eliminar_documento'),
    path('CLINICA/templates/buscarDocumento.html',buscar_documentos,name = 'buscar_documentos'),
    path('CLINICA/templates/documento.html',crear_documento, name="crear_documento"),

    path('CLINICA/templates/home.html',home),
    path('CLINICA/templates/presentacion/iniciomenu.html',iniciomenu),
    path('CLINICA/templates/usuario/usuario.html',usuario),
    path('CLINICA/templates/usuario/inicio.html',inicio),
    path('CLINICA/templates/empleado/empleado.html',empleado),

    path('CLINICA/templates/usuario/listar.html',buscar_usuarios,name = 'buscar_usuarios'),
    path('CLINICA/templates/usuario/listar.html',listar_usuarios,name = 'lista_usuarios'),
    path('CLINICA/templates/usuario/<int:id>',eliminar_usuario,name = 'eliminar_usuario'),
    path('CLINICA/templates/usuario/registro.html',crear_usuario,name="crear_usuario"),
    path('CLINICA/templates/usuario/actualizar.html',abrir_actualizar_usuarios,name="abrir_actualizar_usuarios"),
    path('CLINICA/templates/cargo.html',crear_cargo, name="crear_cargo"),
    path('CLINICA/templates/usuario/actualizar.html/<int:id>',actualizar_usuario,name="actualizar_usuario"),
    path('CLINICA/templates/empleado/buscarEmpleado.html',listar_empleados, name="listar_empleados"),
    path('CLINICA/templates/BuscarEspecialidad.html',listar_especialidades, name="lista_especialidades"),
    path('CLINICA/templates/buscarCargo.html',listar_cargos, name="listar_cargos"),
    path('CLINICA/templates/buscarDocumento.html',listar_documentos, name= 'lista_documentos'),

    
    path('CLINICA/templates/especialidad.html',especialidad),
    path('CLINICA/templates/documento.html',documento),
]
