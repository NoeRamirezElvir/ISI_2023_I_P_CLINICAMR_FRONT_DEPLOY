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
from CLINICA.views_api.views_citas import *
from CLINICA.views_api.views_impuesto_historico import *
from CLINICA.views_api.views_sintomas import *
from CLINICA.views_api.views_precio_historico_medicamento import *
from CLINICA.views_api.views_costo_historico_medicamento import *
from CLINICA.views_api.views_medicamento import *
from CLINICA.views_api.views_enfermedad import *
from CLINICA.views_api.views_enfermedad_detalle import *
from CLINICA.views_api.views_laboratorios import *
from CLINICA.views_api.views_metodo_de_pago import *
from CLINICA.views_api.views_proveedor import *
from CLINICA.views_api.views_parametros_generales import *
from CLINICA.views_api.views_tratamientos import*
from CLINICA.views_api.views_resultado import *
from CLINICA.views_api.views_diagnostico import *
from CLINICA.views_api.views_precio_historico_tratamiento import *
from CLINICA.views_api.views_precio_historico_examen import *
from CLINICA.views_api.views_diagnostico_detalle import *
from CLINICA.views_api.views_precio_historico_consulta import *
from CLINICA.views_api.views_recaudo_detalle_examen import *
from CLINICA.views_api.views_recaudo_detalle_medicamento import *
from CLINICA.views_api.views_recaudo_detalle_tratamiento import *
from CLINICA.views_api.views_consulta_detalle import *
from CLINICA.views_api.views_examen import *
from CLINICA.views_api.views_consulta import *
from CLINICA.views_api.views_expediente import *
from CLINICA.views_api.views_autorizacion_paciente import *
from CLINICA.views_api.views_traslado_paciente import *
from CLINICA.views_api.views_correlativo_SAR import *
from CLINICA.views_api.views_recaudo import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', presentacion),
    path('CLINICA/templates/presentacion/presentacion.html', salir_presentacion, name='salir_presentacion'),

###################
    path('CLINICA/templates/presentacion/usuariosignup.html',registrar_login, name="registrar_login"),
    path('CLINICA/templates/presentacion/usuariosignup.html',usuariosignup, name="usuariosignup"),
    path('CLINICA/templates/presentacion/usuariologin.html',iniciar_sesion, name="iniciar_sesion"),
    path('CLINICA/templates/cargos/cargoactualizar.html',abrir_actualizar_cargos,name="abrir_actualizar_cargos"),
    path('CLINICA/templates/cargos/cargoactualizar.html/<int:id>',actualizar_cargo,name="actualizar_cargo"),
    path('CLINICA/templates/cargos/buscarCargo.html/<int:id>',eliminar_cargo,name = 'eliminar_cargo'),
    path('CLINICA/templates/cargos/buscarCargo.html',buscar_cargos,name = 'buscar_cargos'),
    
    ##
    path('CLINICA/templates/documentos/documentoactualizar.html',abrir_actualizar_documentos,name="abrir_actualizar_documentos"),
    path('CLINICA/templates/documentos/documentoactualizar.html/<int:id>',actualizar_documento,name="actualizar_documento"),
    path('CLINICA/templates/documentos/buscarDocumento.html/<int:id>',eliminar_documento,name = 'eliminar_documento'),
    path('CLINICA/templates/documentos/buscarDocumento.html',buscar_documentos,name = 'buscar_documentos'),
    path('CLINICA/templates/documentos/documento.html',crear_documento, name="crear_documento"),
    path('CLINICA/templates/documento.html',documento),
    #
    path('CLINICA/templates/home.html',home),
    path('CLINICA/templates/presentacion/iniciomenu.html',iniciomenu),
    path('CLINICA/templates/usuario/usuario.html',usuario),
    path('CLINICA/templates/inicio.html',inicio),
    
    #
    path('CLINICA/templates/usuario/listar.html',buscar_usuarios,name = 'buscar_usuarios'),
    path('CLINICA/templates/usuario/listar.html',listar_usuarios,name = 'lista_usuarios'),
    path('CLINICA/templates/usuario/<int:id>',eliminar_usuario,name = 'eliminar_usuario'),
    path('CLINICA/templates/usuario/registro.html',crear_usuario,name="crear_usuario"),
    path('CLINICA/templates/usuario/actualizar.html',abrir_actualizar_usuarios,name="abrir_actualizar_usuarios"),
    path('CLINICA/templates/cargos/cargo.html',crear_cargo, name="crear_cargo"),
    path('CLINICA/templates/usuario/actualizar.html/<int:id>',actualizar_usuario,name="actualizar_usuario"),
    
    path('CLINICA/templates/cargos/buscarCargo.html',listar_cargos, name="listar_cargos"),
    path('CLINICA/templates/cargos/buscarDocumento.html',listar_documentos, name= 'lista_documentos'),

    #impuestos
    path('CLINICA/templates/Impuestos/ImpuestoActualizar.html',abrir_actualizar_Impuestos,name="abrir_actualizar_Impuestos"),
    path('CLINICA/templates/Impuestos/ImpuestoActualizar.html/<int:id>',actualizar_Impuestos,name="actualizar_Impuestos"),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html/<int:id>',eliminar_Impuestos,name = 'eliminar_Impuestos'),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html',buscar_Impuestos,name = 'buscar_Impuestos'),
    path('CLINICA/templates/Impuestos/Impuesto.html',crear_Impuestos, name="crear_Impuestos"),
    path('CLINICA/templates/Impuestos/BuscarImpuesto.html',listar_Impuestos, name="listar_Impuestos"),

    #Especialidades
    path('CLINICA/templates/especialidad/especialidadActualizar.html',abrir_actualizar_especialidades,name="abrir_actualizar_especialidades"),
    path('CLINICA/templates/especialidad/especialidadActualizar.html/<int:id>',actualizar_especialidades,name="actualizar_especialidades"),
    path('CLINICA/templates/especialidad/BuscarEspecialidad.html/<int:id>',eliminar_especialidades,name = 'eliminar_especialidades'),
    path('CLINICA/templates/especialidad/BuscarEspecialidad.html',buscar_especialidades,name = 'buscar_especialidades'),
    path('CLINICA/templates/especialidad/especialidad.html',crear_especialidades, name="crear_especialidades"),
    path('CLINICA/templates/especialidad/BuscarEspecialidad.html',listar_especialidades, name="listar_especialidades"),


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


    #Empleados
   
    path('CLINICA/templates/empleado/EmpleadoActualizar.html',abrir_actualizar_empleados,name="abrir_actualizar_empleados"),
    path('CLINICA/templates/empleado/EmpleadoActualizar.html/<int:id>',actualizar_empleados,name="actualizar_empleados"),
    path('CLINICA/templates/empleado/buscarEmpleado.html/<int:id>',eliminar_empleados,name = 'eliminar_empleados'),
    path('CLINICA/templates/empleado/buscarEmpleado.html',buscar_empleados,name = 'buscar_empleados'),
    path('CLINICA/templates/empleado/empleado.html',crear_empleados, name="crear_empleados"),
    path('CLINICA/templates/empleado/buscarEmpleado.html',listar_empleados, name="listar_empleados"),

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

    #Citas
    path('CLINICA/templates/citas/cita_actualizar.html',abrir_actualizar_citas,name="abrir_actualizar_citas"),
    path('CLINICA/templates/citas/cita_actualizar.html/<int:id>',actualizar_citas,name="actualizar_citas"),
    path('CLINICA/templates/citas/cita_buscar.html/<int:id>',eliminar_citas,name = 'eliminar_citas'),
    path('CLINICA/templates/citas/cita_buscar.html',buscar_citas,name = 'buscar_citas'),
    path('CLINICA/templates/citas/cita.html',crear_citas, name="crear_citas"),
    path('CLINICA/templates/citas/cita_buscar.html',listar_citas, name="listar_citas"),
    path('CLINICA/templates/citas/cita_calendario.html',abrir_calendario, name="abrir_calendario"),

    #impuesto historico
    path('CLINICA/templates/impuesto_historico/impuesto_historico_buscar.html/<int:id>',eliminar_impuesto_historico,name = 'eliminar_impuesto_historico'),
    path('CLINICA/templates/impuesto_historico/impuesto_historico_buscar.html',buscar_impuesto_historico,name = 'buscar_impuesto_historico'),

    #Sintoma
    path('CLINICA/templates/sintomas/actualizar_sintomas.html',abrir_actualizar_sintomas,name="abrir_actualizar_sintomas"),
    path('CLINICA/templates/sintomas/actualizar_sintomas.html/<int:id>',actualizar_sintomas,name="actualizar_sintomas"),
    path('CLINICA/templates/sintomas/buscar_sintomas.html/<int:id>',eliminar_sintomas,name = 'eliminar_sintomas'),
    path('CLINICA/templates/sintomas/buscar_sintomas.html',buscar_sintomas,name = 'buscar_sintomas'),
    path('CLINICA/templates/sintomas/sintomas.html',crear_sintomas, name="crear_sintomas"),
    path('CLINICA/templates/sintomas/buscar_sintomas.html',listar_sintomas, name="listar_sintomas"),

    #precio historico
    path('CLINICA/templates/precio_historico_medicamento/buscar_precio_historico_medicamento.html/<int:id>',eliminar_precio_historico_medicamento,name = 'eliminar_precio_historico_medicamento'),
    path('CLINICA/templates/precio_historico_medicamento/buscar_precio_historico_medicamento.html',buscar_precio_historico_medicamento,name = 'buscar_precio_historico_medicamento'),

    #costo historico
    path('CLINICA/templates/costo_historico_medicamento/buscar_costo_historico_medicamento.html/<int:id>',eliminar_costo_historico_medicamento,name = 'eliminar_costo_historico_medicamento'),
    path('CLINICA/templates/costo_historico_medicamento/buscar_costo_historico_medicamento.html',buscar_costo_historico_medicamento,name = 'buscar_costo_historico_medicamento'),

    #Medicamentos
    path('CLINICA/templates/medicamentos/actualizar_medicamentos.html',abrir_actualizar_medicamentos,name="abrir_actualizar_medicamentos"),
    path('CLINICA/templates/medicamentos/actualizar_medicamentos.html/<int:id>',actualizar_medicamentos,name="actualizar_medicamentos"),
    path('CLINICA/templates/medicamentos/buscar_medicamentos.html/<int:id>',eliminar_medicamentos,name = 'eliminar_medicamentos'),
    path('CLINICA/templates/medicamentos/buscar_medicamentos.html',buscar_medicamentos,name = 'buscar_medicamentos'),
    path('CLINICA/templates/medicamentos/medicamentos.html',crear_medicamentos, name="crear_medicamentos"),
    path('CLINICA/templates/medicamentos/buscar_medicamentos.html',listar_medicamentos, name="listar_medicamentos"),

    #Enfermedad
    path('CLINICA/templates/enfermedad/actualizar_enfermedad.html',abrir_actualizar_enfermedad,name="abrir_actualizar_enfermedad"),
    path('CLINICA/templates/enfermedad/actualizar_enfermedad.html/<int:id>',actualizar_enfermedad,name="actualizar_enfermedad"),
    path('CLINICA/templates/enfermedad/buscar_enfermedad.html/<int:id>',eliminar_enfermedad,name = 'eliminar_enfermedad'),
    path('CLINICA/templates/enfermedad/buscar_enfermedad.html',buscar_enfermedad,name = 'buscar_enfermedad'),
    path('CLINICA/templates/enfermedad/enfermedad.html',crear_enfermedad, name="crear_enfermedad"),
    path('CLINICA/templates/enfermedad/buscar_enfermedad.html',listar_enfermedad, name="listar_enfermedad"),

    #Laboratorios
    path('CLINICA/templates/Laboratorios/ActualizarLaboratorios.html',abrir_actualizar_laboratorios,name="abrir_actualizar_laboratorios"),
    path('CLINICA/templates/Laboratorios/ActualizarLaboratorios.html/<int:id>',actualizar_laboratorios,name="actualizar_laboratorios"),
    path('CLINICA/templates/Laboratorios/BuscarLaboratorios.html/<int:id>',eliminar_laboratorios,name = 'eliminar_laboratorios'),
    path('CLINICA/templates/Laboratorios/BuscarLaboratorios.html',buscar_laboratorios,name = 'buscar_laboratorios'),
    path('CLINICA/templates/Laboratorios/Laboratorios.html',crear_laboratorios, name="crear_laboratorios"),
    path('CLINICA/templates/Laboratorios/BuscarLaboratorios.html',listar_laboratorios, name="listar_laboratorios"),

    #Detalle enfermedad
    path('CLINICA/templates/enfermedad_detalle/buscar_enfermedad_detalle.html/<int:id>',eliminar_enfermedad_detalle,name = 'eliminar_enfermedad_detalle'),
    path('CLINICA/templates/enfermedad_detalle/buscar_enfermedad_detalle.html',buscar_enfermedad_detalle,name = 'buscar_enfermedad_detalle'),

    #Metodos de pago
    path('CLINICA/templates/MetodoDePago/ActualizarMetodoDePago.html',abrir_actualizar_metodos_De_pago,name="abrir_actualizar_metodos_De_pago"),
    path('CLINICA/templates/MetodoDePago/ActualizarMetodoDePago.html/<int:id>',actualizar_metodos_De_pago,name="actualizar_metodos_De_pago"),
    path('CLINICA/templates/MetodoDePago/BuscarMetodoDePago.html/<int:id>',eliminar_metodos_De_pago,name = 'eliminar_metodos_De_pago'),
    path('CLINICA/templates/MetodoDePago/BuscarMetodoDePago.html',buscar_metodos_De_pago,name = 'buscar_metodos_De_pago'),
    path('CLINICA/templates/MetodoDePago/MetodoDePago.html',crear_metodos_De_pago, name="crear_metodos_De_pago"),
    path('CLINICA/templates/MetodoDePago/BuscarMetodoDePago.html',listar_metodos_De_pago, name="listar_metodos_De_pago"),


    #Proveedores
    path('CLINICA/templates/Proveedor/ProveedorActualizar.html',abrir_actualizar_proveedor,name="abrir_actualizar_proveedor"),
    path('CLINICA/templates/Proveedor/ProveedorActualizar.html/<int:id>',actualizar_proveedor,name="actualizar_proveedor"),
    path('CLINICA/templates/Proveedor/BuscarProveedor.html/<int:id>',eliminar_proveedor,name = 'eliminar_proveedor'),
    path('CLINICA/templates/Proveedor/BuscarProveedor.html',buscar_proveedor,name = 'buscar_proveedor'),
    path('CLINICA/templates/Proveedor/Proveedor.html',crear_proveedor, name="crear_proveedor"),
    path('CLINICA/templates/Proveedor/BuscarProveedor.html',listar_proveedor, name="listar_proveedor"),


    #parametros_generales
    path('CLINICA/templates/parametros_generales/Actualizar_parametros_generales.html',abrir_actualizar_parametros_generales,name="abrir_actualizar_parametros_generales"),
    path('CLINICA/templates/parametros_generales/Actualizar_parametros_generales.html/<int:id>',actualizar_parametros_generales,name="actualizar_parametros_generales"),
    path('CLINICA/templates/parametros_generales/Buscar_parametros_generales.html/<int:id>',eliminar_parametros_generales,name = 'eliminar_parametros_generales'),
    path('CLINICA/templates/parametros_generales/Buscar_parametros_generales.html',buscar_parametros_generales,name = 'buscar_parametros_generales'),
    path('CLINICA/templates/parametros_generales/parametros_generales.html',crear_parametros_generales, name="crear_parametros_generales"),
    path('CLINICA/templates/parametros_generales/Buscar_parametros_generales.html',listar_parametros_generales, name="listar_parametros_generales"),


    #Tratamientos
    path('CLINICA/templates/tratamiento/Actualizar_tratamiento.html',abrir_actualizar_tratamientos,name="abrir_actualizar_tratamientos"),
    path('CLINICA/templates/tratamiento/Actualizar_tratamiento.html/<int:id>',actualizar_tratamientos,name="actualizar_tratamientos"),
    path('CLINICA/templates/tratamiento/Buscar_tratamiento.html/<int:id>',eliminar_tratamientos,name = 'eliminar_tratamientos'),
    path('CLINICA/templates/tratamiento/Buscar_tratamiento.html',buscar_tratamientos,name = 'buscar_tratamientos'),
    path('CLINICA/templates/tratamiento/tratamiento.html',crear_tratamientos, name="crear_tratamientos"),
    path('CLINICA/templates/tratamiento/Buscar_tratamiento.html',listar_tratamientos, name="listar_tratamientos"),

    #Resultados
    path('CLINICA/templates/Resultados/ActualizarResultados.html',abrir_actualizar_resultados,name="abrir_actualizar_resultados"),
    path('CLINICA/templates/Resultados/ActualizarResultados.html/<int:id>',actualizar_resultados,name="actualizar_resultados"),
    path('CLINICA/templates/Resultados/BuscarResultados.html/<int:id>',eliminar_resultados,name = 'eliminar_resultados'),
    path('CLINICA/templates/Resultados/BuscarResultados.html',buscar_resultados,name = 'buscar_resultados'),
    path('CLINICA/templates/Resultados/Resultados.html',crear_resultados, name='crear_resultados'),
    path('CLINICA/templates/Resultados/BuscarResultados.html',listar_resultados, name="listar_resultados"),


    #Diagnostico
    path('CLINICA/templates/diagnostico/Actualizar_diagnostico.html',abrir_actualizar_diagnosticos,name="abrir_actualizar_diagnosticos"),
    path('CLINICA/templates/diagnostico/Actualizar_diagnostico.html/<int:id>',actualizar_diagnosticos,name="actualizar_diagnosticos"),
    path('CLINICA/templates/diagnostico/Buscar_diagnostico.html/<int:id>',eliminar_diagnosticos,name = 'eliminar_diagnosticos'),
    path('CLINICA/templates/diagnostico/Buscar_diagnostico.html',buscar_diagnosticos,name = 'buscar_diagnosticos'),
    path('CLINICA/templates/diagnostico/diagnostico.html',crear_diagnosticos, name="crear_diagnosticos"),
    path('CLINICA/templates/diagnostico/Buscar_diagnostico.html',listar_diagnosticos, name="listar_diagnosticos"),

    #Examen
    path('CLINICA/templates/examen/actualizar_examen.html',abrir_actualizar_examenes,name="abrir_actualizar_examenes"),
    path('CLINICA/templates/examen/actualizar_examen.html/<int:id>',actualizar_examenes,name="actualizar_examenes"),
    path('CLINICA/templates/examen/buscar_examen.html/<int:id>',eliminar_examenes,name = 'eliminar_examenes'),
    path('CLINICA/templates/examen/buscar_examen.html',buscar_examenes,name = 'buscar_examenes'),
    path('CLINICA/templates/examen/examen.html',crear_examenes, name="crear_examenes"),
    path('CLINICA/templates/examen/buscar_examen.html',listar_examenes, name="listar_examenes"),


    #Detalle Diagnostico
    path('CLINICA/templates/diagnostico_detalle/buscar_diagnostico_detalle.html/<int:id>',eliminar_diagnostico_detalle,name = 'eliminar_diagnostico_detalle'),
    path('CLINICA/templates/diagnostico_detalle/buscar_diagnostico_detalle.html',buscar_diagnostico_detalle,name = 'buscar_diagnostico_detalle'),


    #precio historico tratamiento
    path('CLINICA/templates/precio_historico_tratamiento/buscar_precio_historico_tratamiento.html/<int:id>',eliminar_precio_historico_tratamiento,name = 'eliminar_precio_historico_tratamiento'),
    path('CLINICA/templates/precio_historico_tratamiento/buscar_precio_historico_tratamiento.html',buscar_precio_historico_tratamiento,name = 'buscar_precio_historico_tratamiento'),

    #precio historico examen
    path('CLINICA/templates/precio_historico_examen/buscar_precio_historico_examen.html/<int:id>',eliminar_precio_historico_examen,name = 'eliminar_precio_historico_examen'),
    path('CLINICA/templates/precio_historico_examen/buscar_precio_historico_examen.html',buscar_precio_historico_examen,name = 'buscar_precio_historico_examen'),

    #recaudo detalle examen
    path('CLINICA/templates/recaudo_detalle_examen/buscar_recaudo_detalle_examen.html/<int:id>',eliminar_recaudo_detalle_examen,name = 'eliminar_recaudo_detalle_examen'),
    path('CLINICA/templates/recaudo_detalle_examen/buscar_recaudo_detalle_examen.html',buscar_recaudo_detalle_examen,name = 'buscar_recaudo_detalle_examen'),

    #recaudo detalle tratamiento
    path('CLINICA/templates/recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html/<int:id>',eliminar_recaudo_detalle_tratamiento,name = 'eliminar_recaudo_detalle_tratamiento'),
    path('CLINICA/templates/recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html',buscar_recaudo_detalle_tratamiento,name = 'buscar_recaudo_detalle_tratamiento'),

    #recaudo detalle medicamento
    path('CLINICA/templates/recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html/<int:id>',eliminar_recaudo_detalle_medicamento,name = 'eliminar_recaudo_detalle_medicamento'),
    path('CLINICA/templates/recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html',buscar_recaudo_detalle_medicamento,name = 'buscar_recaudo_detalle_medicamento'),

    #Consulta
    path('CLINICA/templates/consulta/actualizar_consulta.html',abrir_actualizar_consulta,name="abrir_actualizar_consulta"),
    path('CLINICA/templates/consulta/actualizar_consulta.html/<int:id>',actualizar_consulta,name="actualizar_consulta"),
    path('CLINICA/templates/consulta/buscar_consulta.html/<int:id>',eliminar_consulta,name = 'eliminar_consulta'),
    path('CLINICA/templates/consulta/buscar_consulta.html',buscar_consulta,name = 'buscar_consulta'),
    path('CLINICA/templates/consulta/consulta.html',crear_consulta, name="crear_consulta"),
    path('CLINICA/templates/consulta/buscar_consulta.html',listar_consulta, name="listar_consulta"),

    #Expediente
    path('CLINICA/templates/expediente/actualizar_expediente.html',abrir_actualizar_expediente,name="abrir_actualizar_expediente"),
    path('CLINICA/templates/expediente/actualizar_expediente.html/<int:id>',actualizar_expediente,name="actualizar_expediente"),
    path('CLINICA/templates/expediente/buscar_expediente.html/<int:id>',eliminar_expediente,name = 'eliminar_expediente'),
    path('CLINICA/templates/expediente/buscar_expediente.html',buscar_expediente,name = 'buscar_expediente'),
    path('CLINICA/templates/expediente/expediente.html',crear_expediente, name="crear_expediente"),
    path('CLINICA/templates/expediente/buscar_expediente.html',listar_expediente, name="listar_expediente"),
    path('CLINICA/templates/expediente/ver_detalle_expediente.html',abrir_detalle_expediente, name="ver_detalle_expediente"),



    #detalle consulta
    path('CLINICA/templates/detalle_consulta/buscar_detalle_consulta.html/<int:id>',eliminar_detalle_consulta,name = 'eliminar_detalle_consulta'),
    path('CLINICA/templates/detalle_consulta/buscar_detalle_consulta.html',buscar_detalle_consulta,name = 'buscar_detalle_consulta'),

    #precio historico consulta
    path('CLINICA/templates/precio_historico_consulta/buscar_precio_historico_consulta.html/<int:id>',eliminar_precio_historico_consulta,name = 'eliminar_precio_historico_consulta'),
    path('CLINICA/templates/precio_historico_consulta/buscar_precio_historico_consulta.html',buscar_precio_historico_consulta,name = 'buscar_precio_historico_consulta'),



    #Autorizacion_Paciente
    path('CLINICA/templates/Autorizacion/Autorizaractualizar.html',abrir_actualizar_autorizacion,name="abrir_actualizar_autorizacion"),
    path('CLINICA/templates/Autorizacion/Autorizaractualizar.html/<int:id>',actualizar_autorizacion,name="actualizar_autorizacion"),
    path('CLINICA/templates/Autorizacion/buscarAutorizar.html/<int:id>',eliminar_autorizacion,name = 'eliminar_autorizacion'),
    path('CLINICA/templates/Autorizacion/buscarAutorizar.html',buscar_autorizacion,name = 'buscar_autorizacion'),
    path('CLINICA/templates/Autorizacion/Autorizar.html',crear_autorizacion, name="crear_autorizacion"),
    path('CLINICA/templates/Autorizacion/buscarAutorizar.html',listar_autorizacion, name="listar_autorizacion"),
    
    #Traslados Pacientes
    path('CLINICA/templates/Traslados/actualizar_traslado.html',abrir_actualizar_traslados,name="abrir_actualizar_traslados"),
    path('CLINICA/templates/Traslados/actualizar_traslado.html/<int:id>',actualizar_traslados,name="actualizar_traslados"),
    path('CLINICA/templates/Traslados/buscar_traslado.html/<int:id>',eliminar_traslados,name = 'eliminar_traslados'),
    path('CLINICA/templates/Traslados/buscar_traslado.html',buscar_traslados,name = 'buscar_traslados'),
    path('CLINICA/templates/Traslados/traslado.html',crear_traslados, name="crear_traslados"),
    path('CLINICA/templates/Traslados/buscar_traslado.html',listar_traslados, name="listar_traslados"),

    #Correlativo
    path('CLINICA/templates/correlativo/actualizar_correlativo.html',abrir_actualizar_correlativo,name="abrir_actualizar_correlativo"),
    path('CLINICA/templates/correlativo/actualizar_correlativo.html/<int:id>',actualizar_correlativo,name="actualizar_correlativo"),
    path('CLINICA/templates/correlativo/buscar_correlativo.html/<int:id>',eliminar_correlativo,name = 'eliminar_correlativo'),
    path('CLINICA/templates/correlativo/buscar_correlativo.html',buscar_correlativo,name = 'buscar_correlativo'),
    path('CLINICA/templates/correlativo/correlativo.html',crear_correlativo, name="crear_correlativo"),
    path('CLINICA/templates/correlativo/buscar_correlativo.html',listar_correlativo, name="listar_correlativo"),

    #Recaudo
    path('CLINICA/templates/recaudo/recaudo_pdf.html',crear_recaudo, name="generar_pdf"),

    path('CLINICA/templates/recaudo/actualizar_recaudo.html',abrir_actualizar_recaudo,name="abrir_actualizar_recaudo"),
    path('CLINICA/templates/recaudo/actualizar_recaudo.html/<int:id>',actualizar_recaudo,name="actualizar_recaudo"),
    path('CLINICA/templates/recaudo/buscar_recaudo.html/<int:id>',eliminar_recaudo,name = 'eliminar_recaudo'),
    path('CLINICA/templates/recaudo/buscar_recaudo.html',buscar_recaudo,name = 'buscar_recaudo'),
    path('CLINICA/templates/recaudo/recaudo.html',crear_recaudo, name="crear_recaudo"),




]
