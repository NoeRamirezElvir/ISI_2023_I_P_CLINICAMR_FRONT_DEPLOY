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
from CLINICA.views_api.views_impuesto import *
from CLINICA.views_api.views_Pacientes import *
from CLINICA.views_api.views_muestras  import *
from CLINICA.views_api.views_login import *
from CLINICA.views_api.views_TipoMuestra import *
from CLINICA.views_api.views_subtipo import *
from CLINICA.views_api.views_tipo import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', presentacion),

###################
    path('CLINICA/templates/presentacion/usuariosignup.html',registrar_login, name="registrar_login"),
    path('CLINICA/templates/presentacion/usuariosignup.html',usuariosignup, name="usuariosignup"),
    path('CLINICA/templates/presentacion/usuariologin.html',iniciar_sesion, name="iniciar_sesion"),
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
    #
    path('CLINICA/templates/home.html',home),
    path('CLINICA/templates/presentacion/iniciomenu.html',iniciomenu),
    path('CLINICA/templates/usuario/usuario.html',usuario),
    path('CLINICA/templates/usuario/inicio.html',inicio),
    path('CLINICA/templates/empleado/empleado.html',empleado),
    #
    path('CLINICA/templates/usuario/listar.html',buscar_usuarios,name = 'buscar_usuarios'),
    path('CLINICA/templates/usuario/listar.html',listar_usuarios,name = 'lista_usuarios'),
    path('CLINICA/templates/usuario/<int:id>',eliminar_usuario,name = 'eliminar_usuario'),
    path('CLINICA/templates/usuario/registro.html',crear_usuario,name="crear_usuario"),
    path('CLINICA/templates/usuario/actualizar.html',abrir_actualizar_usuarios,name="abrir_actualizar_usuarios"),
    path('CLINICA/templates/cargo.html',crear_cargo, name="crear_cargo"),
    path('CLINICA/templates/usuario/actualizar.html/<int:id>',actualizar_usuario,name="actualizar_usuario"),
    path('CLINICA/templates/empleado/buscarEmpleado.html',listar_empleados, name="listar_empleados"),

    path('CLINICA/templates/buscarCargo.html',listar_cargos, name="listar_cargos"),
    path('CLINICA/templates/buscarDocumento.html',listar_documentos, name= 'lista_documentos'),

    #impuestos
    path('CLINICA/templates/Impuestos/ImpuestoActualizar.html',abrir_actualizar_Impuestos,name="abrir_actualizar_Impuestos"),
    path('CLINICA/templates/Impuestos/ImpuestoActualizar.html/<int:id>',actualizar_Impuestos,name="actualizar_Impuestos"),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html/<int:id>',eliminar_Impuestos,name = 'eliminar_Impuestos'),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html',buscar_Impuestos,name = 'buscar_Impuestos'),
    path('CLINICA/templates/Impuestos/Impuesto.html',crear_Impuestos, name="crear_Impuestos"),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html',listar_Impuestos, name="listar_Impuestos"),

    #Especialidades
    path('CLINICA/templates/especialidadActualizar.html',abrir_actualizar_especialidades,name="abrir_actualizar_especialidades"),
    path('CLINICA/templates/especialidadActualizar.html/<int:id>',actualizar_especialidades,name="actualizar_especialidades"),
    path('CLINICA/templates/BuscarEspecialidad.html/<int:id>',eliminar_especialidades,name = 'eliminar_especialidades'),
    path('CLINICA/templates/BuscarEspecialidad.html',buscar_especialidades,name = 'buscar_especialidades'),
    path('CLINICA/templates/especialidad.html',crear_especialidades, name="crear_especialidades"),
    path('CLINICA/templates/BuscarEspecialidad.html',listar_especialidades, name="listar_especialidades"),


    #SubTipo
    path('CLINICA/templates/SubTipo/subtipoActualizar.html',abrir_actualizar_subtipo,name="abrir_actualizar_subtipo"),
    path('CLINICA/templates/SubTipo/subtipoActualizar.html/<int:id>',actualizar_subtipo,name="actualizar_subtipo"),
    path('CLINICA/templates/SubTipo/buscarsubtipo.html/<int:id>',eliminar_subtipo,name = 'eliminar_subtipo'),
    path('CLINICA/templates/SubTipo/buscarsubtipo.html',buscar_subtipo,name = 'buscar_subtipo'),
    path('CLINICA/templates/SubTipo/subtipo.html',crear_subtipo, name="crear_subtipo"),
    path('CLINICA/templates/SubTipo/buscarsubtipo.html',listar_subtipo, name="listar_subtipo"),

    #Tipo
    path('CLINICA/templates/Tipos/tipoactualizar.html',abrir_actualizar_tipo,name="abrir_actualizar_tipo"),
    path('CLINICA/templates/Tipos/tipoactualizar.html/<int:id>',actualizar_tipo,name="actualizar_tipo"),
    path('CLINICA/templates/Tipos/buscartipo.html/<int:id>',eliminar_tipo,name = 'eliminar_tipo'),
    path('CLINICA/templates/Tipos/buscartipo.html',buscar_tipo,name = 'buscar_tipo'),
    path('CLINICA/templates/Tipos/tipo.html',crear_tipo, name="crear_tipo"),
    path('CLINICA/templates/Tipos/buscartipo.html',listar_tipo, name="listar_tipo"),

    #Pacientes
    path('CLINICA/templates/Pacientes/PacienteActualizar.html',abrir_actualizar_pacientes,name="abrir_actualizar_pacientes"),
    path('CLINICA/templates/Pacientes/PacienteActualizar.html/<int:id>',actualizar_pacientes,name="actualizar_pacientes"),
    path('CLINICA/templates/Pacientes/buscarPaciente.html/<int:id>',eliminar_pacientes,name = 'eliminar_pacientes'),
    path('CLINICA/templates/Pacientes/buscarPaciente.html',buscar_pacientes,name = 'buscar_pacientes'),
    path('CLINICA/templates/Pacientes/Paciente.html',crear_paciente, name="crear_paciente"),
    path('CLINICA/templates/Pacientes/buscarPaceinte.html',listar_pacientes, name="listar_pacientes"),


    # Tipo Muestra
    path('CLINICA/templates/TipoMuestra/TMuestraActualizar.html',abrir_actualizar_TipoMuestra,name="abrir_actualizar_TipoMuestra"),
    path('CLINICA/templates/TipoMuestra/TMuestraActualizar.html/<int:id>',actualizar_TipoMuestra,name="actualizar_TipoMuestra"),
    path('CLINICA/templates/TipoMuestra/BuscarTMuestra.html/<int:id>',eliminar_TipoMuestra,name = 'eliminar_TipoMuestra'),
    path('CLINICA/templates/TipoMuestra/BuscarTMuestra.html',buscar_TipoMuestra,name = 'buscar_TipoMuestra'),
    path('CLINICA/templates/TipoMuestra/TMuestra.html',crear_TipoMuestra, name="crear_TipoMuestra"),
    path('CLINICA/templates/TipoMuestra/BuscarTMuestra.html',listar_TipoMuestra, name="listar_TipoMuestra"),


    #Muestras
    path('CLINICA/templates/Muestras/MuestraActualizar.html',abrir_actualizar_muestras,name="abrir_actualizar_muestras"),
    path('CLINICA/templates/Muestras/MuestraActualizar.html/<int:id>',actualizar_muestras,name="actualizar_muestras"),
    path('CLINICA/templates/Muestras/BuscarMuestra.html/<int:id>',eliminar_muestras,name = 'eliminar_muestras'),
    path('CLINICA/templates/Muestras/BuscarMuestra.html',buscar_muestras,name = 'buscar_muestras'),
    path('CLINICA/templates/Muestras/Muestra.html',crear_muestras, name="crear_muestras"),
    path('CLINICA/templates/Muestras/BuscarMuestra.html',listar_muestras, name="listar_muestras"),




    

    path('CLINICA/templates/documento.html',documento),
]
