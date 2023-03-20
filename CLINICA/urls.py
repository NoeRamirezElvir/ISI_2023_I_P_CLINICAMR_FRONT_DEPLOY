from django.urls import path
from . import views
from views_api import views_cargos
from views_api import views_usuarios
from views_api import views_login
from views_api import views_documento
from views_api import views_impuesto
from views_api import views_Pacientes
from views_api import views_especialidades
from views_api import views_muestras
from views_api import views_TipoMuestra
from views_api import views_subtipo
from views_api import views_tipo
from views_api import views_citas
from views_api import views_impuesto_historico



urlpatterns = [
    path('', views.presentacion,name='presentacion'),
    path('', views.salir_presentacion,name='salir_presentacion'),
    path('',views.usuariosignup, name='usuariosignup'),
    path('',views_login.iniciar_sesion, name='iniciar_sesion'),
    path('',views_login.registrar_login, name='registrar_login'),


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

    #Impuestos
    path('',views_impuesto.abrir_actualizar_Impuestos , name='abrir_actualizar_Impuestos'),
    path('',views_impuesto.actualizar_Impuestos , name='actualizar_Impuestos'),
    path('',views_impuesto.eliminar_Impuestos , name='eliminar_Impuestos'),
    path('',views_impuesto.listar_Impuestos, name='buscar_Impuestos'),
    path('',views_impuesto.buscar_Impuestos, name='buscar_Impuestos'),
    path('',views_impuesto.crear_Impuestos, name='crear_Impuestos'),

    #SubTipo
    path('',views_subtipo.abrir_actualizar_subtipo , name='abrir_actualizar_subtipo'),
    path('',views_subtipo.actualizar_subtipo , name='actualizar_subtipo'),
    path('',views_subtipo.eliminar_subtipo , name='eliminar_subtipo'),
    path('',views_subtipo.listar_subtipo, name='buscar_subtipo'),
    path('',views_subtipo.buscar_subtipo, name='buscar_subtipo'),
    path('',views_subtipo.crear_subtipo, name='crear_subtipo'),


    #Pacientes
    path('',views_Pacientes.abrir_actualizar_pacientes, name='abrir_actualizar_pacientes'),
    path('',views_Pacientes.actualizar_pacientes , name='actualizar_pacientes'),
    path('',views_Pacientes.eliminar_pacientes , name='eliminar_pacientes'),
    path('',views_Pacientes.listar_pacientes, name='buscar_pacientes'),
    path('',views_Pacientes.buscar_pacientes, name='buscar_pacientes'),
    path('',views_Pacientes.crear_paciente, name='crear_paciente'),


    #Tipo
    path('',views_tipo.abrir_actualizar_tipo , name='abrir_actualizar_tipo'),
    path('',views_tipo.actualizar_tipo , name='actualizar_tipo'),
    path('',views_tipo.eliminar_tipo , name='eliminar_tipo'),
    path('',views_tipo.listar_tipo, name='buscar_tipo'),
    path('',views_tipo.buscar_tipo, name='buscar_tipo'),
    path('',views_tipo.crear_tipo, name='crear_tipo'),


    #Especialidad
    path('',views_especialidades.abrir_actualizar_especialidades, name='abrir_actualizar_especialidades'),
    path('',views_especialidades.actualizar_especialidades , name='actualizar_especialidades'),
    path('',views_especialidades.eliminar_especialidades , name='eliminar_especialidades'),
    path('',views_especialidades.listar_especialidades, name='buscar_especialidades'),
    path('',views_especialidades.buscar_especialidades, name='buscar_especialidades'),
    path('',views_especialidades.crear_especialidades, name='crear_especialidades'),

    #Tipo Muestra
    path('',views_TipoMuestra.abrir_actualizar_TipoMuestra , name='abrir_actualizar_TipoMuestra'),
    path('',views_TipoMuestra.actualizar_TipoMuestra , name='actualizar_TipoMuestra'),
    path('',views_TipoMuestra.eliminar_TipoMuestra , name='eliminar_TipoMuestra'),
    path('',views_TipoMuestra.listar_TipoMuestra, name='buscar_TipoMuestra'),
    path('',views_TipoMuestra.buscar_TipoMuestra, name='buscar_TipoMuestra'),
    path('',views_TipoMuestra.crear_TipoMuestra, name='crear_TipoMuestra'),

    #Muestras
    path('',views_muestras.abrir_actualizar_muestras , name='abrir_actualizar_muestras'),
    path('',views_muestras.actualizar_muestras , name='actualizar_muestras'),
    path('',views_muestras.eliminar_muestras , name='eliminar_muestras'),
    path('',views_muestras.listar_muestras, name='buscar_muestras'),
    path('',views_muestras.buscar_muestras, name='buscar_muestras'),
    path('',views_muestras.crear_muestras, name='crear_muestras'),

    #citas
    path('',views_citas.abrir_actualizar_citas , name='abrir_actualizar_citas'),
    path('',views_citas.actualizar_citas , name='actualizar_citas'),
    path('',views_citas.eliminar_citas , name='eliminar_citas'),
    path('',views_citas.listar_citas, name='listar_citas'),
    path('',views_citas.buscar_citas, name='buscar_citas'),
    path('',views_citas.crear_citas, name='crear_citas'),
    path('',views_citas.abrir_calendario, name='abrir_calendario'),

    #Impuesto historico
    path('',views_impuesto_historico.abrir_actualizar_impuesto_historico , name='abrir_impuesto_historico'),
    path('',views_impuesto_historico.actualizar_impuesto_historico , name='actualizar_impuesto_historico'),
    path('',views_impuesto_historico.eliminar_impuesto_historico , name='eliminar_impuesto_historico'),
    path('',views_impuesto_historico.listar_impuesto_historico, name='listar_impuesto_historico'),
    path('',views_impuesto_historico.buscar_impuesto_historico, name='buscar_impuesto_historico'),
    path('',views_impuesto_historico.crear_impuesto_historico, name='crear_impuesto_historico'),

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