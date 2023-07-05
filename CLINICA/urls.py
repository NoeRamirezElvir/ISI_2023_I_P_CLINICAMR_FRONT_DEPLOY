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
from views_api import views_sintomas
from views_api import views_precio_historico_medicamento
from views_api import views_costo_historico_medicamento
from views_api import views_medicamento
from views_api import views_enfermedad 
from views_api import views_enfermedad_detalle
from views_api import views_empleados
from views_api import views_laboratorios
from views_api import views_metodo_de_pago
from views_api import views_proveedor
from views_api import views_parametros_generales
from views_api import views_tratamientos
from views_api import views_resultado
from views_api import views_diagnostico
from views_api import views_precio_historico_tratamiento
from views_api import views_precio_historico_examen
from views_api import views_diagnostico_detalle
from views_api import views_recaudo_detalle_examen
from views_api import views_recaudo_detalle_medicamento
from views_api import views_recaudo_detalle_tratamiento
from views_api import views_consulta_detalle
from views_api import views_precio_historico_consulta
from views_api import views_examen
from views_api import views_consulta
from views_api import views_expediente
from views_api import views_autorizacion_paciente
from views_api import views_traslado_paciente
from views_api import views_correlativo_SAR
from views_api import views_recaudo
from views_api import views_descuento

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

     path('',views_empleados.abrir_actualizar_empleados, name='abrir_actualizar_empleados'),
    path('',views_empleados.actualizar_empleados , name='actualizar_empleados'),
    path('',views_empleados.eliminar_empleados, name='eliminar_empleados'),
    path('',views_empleados.listar_empleados, name='listar_empleados'),
    path('',views_empleados.buscar_empleados, name='buscar_empleados'),
    path('',views_empleados.crear_empleados, name='crear_empleados'),


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
    path('',views_impuesto_historico.eliminar_impuesto_historico , name='eliminar_impuesto_historico'),
    path('',views_impuesto_historico.buscar_impuesto_historico, name='buscar_impuesto_historico'),

    #Sintomas
    path('',views_sintomas.abrir_actualizar_sintomas , name='abrir_actualizar_sintomas'),
    path('',views_sintomas.actualizar_sintomas , name='actualizar_sintomas'),
    path('',views_sintomas.eliminar_sintomas , name='eliminar_sintomas'),
    path('',views_sintomas.listar_sintomas, name='listar_sintomas'),
    path('',views_sintomas.buscar_sintomas, name='buscar_sintomas'),
    path('',views_sintomas.crear_sintomas, name='crear_sintomas'),

    #Precio historico
    path('',views_precio_historico_medicamento.eliminar_precio_historico_medicamento , name='eliminar_precio_historico_medicamento'),
    path('',views_precio_historico_medicamento.buscar_precio_historico_medicamento, name='buscar_precio_historico_medicamento'),

    #Costo historico
    path('',views_costo_historico_medicamento.eliminar_costo_historico_medicamento , name='eliminar_costo_historico_medicamento'),
    path('',views_costo_historico_medicamento.buscar_costo_historico_medicamento, name='buscar_costo_historico_medicamento'),

    #Medicamentos
    path('',views_medicamento.abrir_actualizar_medicamentos , name='abrir_actualizar_medicamentos'),
    path('',views_medicamento.actualizar_medicamentos , name='actualizar_medicamentos'),
    path('',views_medicamento.eliminar_medicamentos , name='eliminar_medicamentos'),
    path('',views_medicamento.listar_medicamentos, name='listar_medicamentos'),
    path('',views_medicamento.buscar_medicamentos, name='buscar_medicamentos'),
    path('',views_medicamento.crear_medicamentos, name='crear_medicamentos'),

    #Enfermedad
    path('',views_enfermedad.abrir_actualizar_enfermedad , name='abrir_actualizar_enfermedad'),
    path('',views_enfermedad.actualizar_enfermedad , name='actualizar_enfermedad'),
    path('',views_enfermedad.eliminar_enfermedad , name='eliminar_enfermedad'),
    path('',views_enfermedad.listar_enfermedad, name='listar_enfermedad'),
    path('',views_enfermedad.buscar_enfermedad, name='buscar_enfermedad'),
    path('',views_enfermedad.crear_enfermedad, name='crear_enfermedad'),

    #Enfermedad detalle
    path('',views_enfermedad_detalle.eliminar_enfermedad_detalle , name='eliminar_enfermedad_detalle'),
    path('',views_enfermedad_detalle.buscar_enfermedad_detalle, name='buscar_enfermedad_detalle'),


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
  
    path('',views.especialidad, name='especialidad'),
    path('',views.documento, name='documento'),

    #Laboratorios
    path('',views_laboratorios.abrir_actualizar_laboratorios , name='abrir_actualizar_laboratorios'),
    path('',views_laboratorios.actualizar_laboratorios , name='actualizar_laboratorios'),
    path('',views_laboratorios.eliminar_laboratorios , name='eliminar_laboratorios'),
    path('',views_laboratorios.listar_laboratorios, name='buscar_laboratorios'),
    path('',views_laboratorios.buscar_laboratorios, name='buscar_laboratorios'),
    path('',views_laboratorios.crear_laboratorios, name='crear_laboratorios'),

    #Metodo de pago
    path('',views_metodo_de_pago.abrir_actualizar_metodos_De_pago , name='abrir_actualizar_metodos_De_pago'),
    path('',views_metodo_de_pago.actualizar_metodos_De_pago , name='actualizar_metodos_De_pago'),
    path('',views_metodo_de_pago.eliminar_metodos_De_pago , name='eliminar_metodos_De_pago'),
    path('',views_metodo_de_pago.listar_metodos_De_pago, name='buscar_metodos_De_pago'),
    path('',views_metodo_de_pago.buscar_metodos_De_pago, name='buscar_metodos_De_pago'),
    path('',views_metodo_de_pago.crear_metodos_De_pago, name='crear_metodos_De_pago'),
   
    #Proveedor
    path('',views_proveedor.abrir_actualizar_proveedor , name='abrir_actualizar_proveedor'),
    path('',views_proveedor.actualizar_proveedor , name='actualizar_proveedor'),
    path('',views_proveedor.eliminar_proveedor , name='eliminar_proveedor'),
    path('',views_proveedor.listar_proveedor, name='buscar_proveedor'),
    path('',views_proveedor.buscar_proveedor, name='buscar_proveedor'),
    path('',views_proveedor.crear_proveedor, name='crear_proveedor'),
   
    #parametros_generales
    path('',views_parametros_generales.abrir_actualizar_parametros_generales , name='abrir_actualizar_parametros_generales'),
    path('',views_parametros_generales.actualizar_parametros_generales , name='actualizar_parametros_generales'),
    path('',views_parametros_generales.eliminar_parametros_generales , name='eliminar_parametros_generales'),
    path('',views_parametros_generales.listar_parametros_generales, name='buscar_parametros_generales'),
    path('',views_parametros_generales.buscar_parametros_generales, name='buscar_parametros_generales'),
    path('',views_parametros_generales.crear_parametros_generales, name='crear_parametros_generales'),
   
   #tratamientos
    path('',views_tratamientos.abrir_actualizar_tratamientos , name='abrir_actualizar_tratamientos'),
    path('',views_tratamientos.actualizar_tratamientos , name='actualizar_tratamientos'),
    path('',views_tratamientos.eliminar_tratamientos , name='eliminar_tratamientos'),
    path('',views_tratamientos.listar_tratamientos, name='buscar_tratamientos'),
    path('',views_tratamientos.buscar_tratamientos, name='buscar_tratamientos'),
    path('',views_tratamientos.crear_tratamientos, name='crear_tratamientos'),
   
    #diagnosticos
    path('',views_diagnostico.abrir_actualizar_diagnosticos , name='abrir_actualizar_diagnosticos'),
    path('',views_diagnostico.actualizar_diagnosticos , name='actualizar_diagnosticos'),
    path('',views_diagnostico.eliminar_diagnosticos , name='eliminar_diagnosticos'),
    path('',views_diagnostico.listar_diagnosticos, name='buscar_diagnosticos'),
    path('',views_diagnostico.buscar_diagnosticos, name='buscar_diagnosticos'),
    path('',views_diagnostico.crear_diagnosticos, name='crear_diagnosticos'),

    #Examen
    path('',views_examen.actualizar_examenes , name='actualizar_examenes'),
    path('',views_examen.actualizar_examenes , name='actualizar_examenes'),
    path('',views_examen.eliminar_examenes , name='eliminar_examenes'),
    path('',views_examen.listar_examenes, name='listar_examenes'),
    path('',views_examen.buscar_examenes, name='buscar_examenes'),
    path('',views_examen.crear_examenes, name='crear_examenes'),


    #Diagnostico detalle
    path('',views_diagnostico_detalle.eliminar_diagnostico_detalle , name='eliminar_diagnostico_detalle'),
    path('',views_diagnostico_detalle.buscar_diagnostico_detalle, name='buscar_diagnostico_detalle'),


    #Precio historico
    path('',views_precio_historico_tratamiento.eliminar_precio_historico_tratamiento , name='eliminar_precio_historico_tratamiento'),
    path('',views_precio_historico_tratamiento.buscar_precio_historico_tratamiento, name='buscar_precio_historico_tratamiento'),

    #Precio historico
    path('',views_precio_historico_examen.eliminar_precio_historico_examen , name='eliminar_precio_historico_examen'),
    path('',views_precio_historico_examen.buscar_precio_historico_examen, name='buscar_precio_historico_examen'),

    #Recaudo detalle examen
    path('',views_recaudo_detalle_examen.eliminar_recaudo_detalle_examen , name='eliminar_recaudo_detalle_examen'),
    path('',views_recaudo_detalle_examen.buscar_recaudo_detalle_examen, name='buscar_recaudo_detalle_examen'),

    #Recaudo detalle tratamiento
    path('',views_recaudo_detalle_tratamiento.eliminar_recaudo_detalle_tratamiento , name='eliminar_recaudo_detalle_tratamiento'),
    path('',views_recaudo_detalle_tratamiento.buscar_recaudo_detalle_tratamiento, name='buscar_recaudo_detalle_tratamiento'),

    #Recaudo detalle medicamento
    path('',views_recaudo_detalle_medicamento.eliminar_recaudo_detalle_medicamento , name='eliminar_recaudo_detalle_medicamento'),
    path('',views_recaudo_detalle_medicamento.buscar_recaudo_detalle_medicamento, name='buscar_recaudo_detalle_medicamento'),

    #Consulta
    path('',views_consulta.abrir_actualizar_consulta , name='abrir_actualizar_consulta'),
    path('',views_consulta.actualizar_consulta , name='actualizar_consulta'),
    path('',views_consulta.eliminar_consulta , name='eliminar_consulta'),
    path('',views_consulta.listar_consulta, name='listar_consulta'),
    path('',views_consulta.buscar_consulta, name='buscar_consulta'),
    path('',views_consulta.crear_consulta, name='crear_consulta'),

    #Expediente
    path('',views_expediente.abrir_actualizar_expediente , name='abrir_actualizar_expediente'),
    path('',views_expediente.abrir_detalle_expediente , name='ver_detalle_expediente'),
    path('',views_expediente.actualizar_expediente , name='actualizar_expediente'),
    path('',views_expediente.eliminar_expediente , name='eliminar_expediente'),
    path('',views_expediente.listar_expediente, name='listar_expediente'),
    path('',views_expediente.buscar_expediente, name='buscar_expediente'),
    path('',views_expediente.crear_expediente, name='crear_expediente'),

    #detalle consulta
    path('',views_consulta_detalle.eliminar_detalle_consulta , name='eliminar_detalle_consulta'),
    path('',views_consulta_detalle.buscar_detalle_consulta, name='buscar_detalle_consulta'),

    #Precio historico consulta
    path('',views_precio_historico_consulta.eliminar_precio_historico_consulta , name='eliminar_precio_historico_consulta'),
    path('',views_precio_historico_consulta.buscar_precio_historico_consulta, name='buscar_precio_historico_consulta'),


    #Expediente
    path('',views_autorizacion_paciente.abrir_actualizar_autorizacion , name='abrir_actualizar_autorizacion'),
    path('',views_autorizacion_paciente.actualizar_autorizacion , name='actualizar_autorizacion'),
    path('',views_autorizacion_paciente.eliminar_autorizacion , name='eliminar_autorizacion'),
    path('',views_autorizacion_paciente.listar_autorizacion , name='listar_autorizacion'),
    path('',views_autorizacion_paciente.buscar_autorizacion , name='buscar_autorizacion'),
    path('',views_autorizacion_paciente.crear_autorizacion , name='crear_autorizacion'),

    #Traslado Paciente
    path('',views_traslado_paciente.abrir_actualizar_traslados , name='abrir_actualizar_traslados'),
    path('',views_traslado_paciente.actualizar_traslados , name='actualizar_traslados'),
    path('',views_traslado_paciente.eliminar_traslados , name='eliminar_traslados'),
    path('',views_traslado_paciente.listar_traslados , name='listar_traslados'),
    path('',views_traslado_paciente.buscar_traslados , name='buscar_traslados'),
    path('',views_traslado_paciente.crear_traslados , name='crear_traslados'),

    #Resultados
    path('',views_resultado.abrir_actualizar_resultados , name='abrir_actualizar_resultados'),
    path('',views_resultado.actualizar_resultados , name='actualizar_resultados'),
    path('',views_resultado.eliminar_resultados , name='eliminar_resultados'),
    path('',views_resultado.listar_resultados , name='listar_resultados'),
    path('',views_resultado.buscar_resultados , name='buscar_resultados'),
    path('',views_resultado.crear_resultados , name='crear_resultados'),


    #Correlativo
    path('',views_correlativo_SAR.abrir_actualizar_correlativo , name='abrir_actualizar_correlativo'),
    path('',views_correlativo_SAR.actualizar_correlativo , name='actualizar_correlativo'),
    path('',views_correlativo_SAR.eliminar_correlativo , name='eliminar_correlativo'),
    path('',views_correlativo_SAR.listar_correlativo , name='listar_correlativo'),
    path('',views_correlativo_SAR.buscar_correlativo , name='buscar_correlativo'),
    path('',views_correlativo_SAR.crear_correlativo , name='crear_correlativo'),

    #Recaudo
    #path('',views_recaudo.crear_recaudo , name='crear_recaudo'),

    path('',views_recaudo.abrir_actualizar_recaudo , name='abrir_actualizar_recaudo'),
    path('',views_recaudo.actualizar_recaudo , name='actualizar_recaudo'),
    path('',views_recaudo.eliminar_recaudo , name='eliminar_recaudo'),
    path('',views_recaudo.buscar_recaudo , name='buscar_recaudo'),
    path('',views_recaudo.crear_recaudo , name='crear_recaudo'),
    path('reimprimir',views_recaudo.reimprimir_recaudo , name='reimprimir_recaudo'),

    #Descuentos
    path('',views_descuento.abrir_actualizar_Descuentos , name='abrir_actualizar_Descuentos'),
    path('',views_descuento.actualizar_Descuentos , name='actualizar_Descuentos'),
    path('',views_descuento.eliminar_Descuentos , name='eliminar_Descuentos'),
    path('',views_descuento.listar_Descuentos, name='buscar_Descuentos'),
    path('',views_descuento.buscar_Descuentos, name='buscar_Descuentos'),
    path('',views_descuento.crear_Descuentos, name='crear_Descuentos'),



]
#path('',views.cargo, name='cargo'),