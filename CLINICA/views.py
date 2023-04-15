from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
import requests

def presentacion(request):
    return render(request,'presentacion/presentacion.html')

url = 'http://localhost:8080/api/'
def salir_presentacion(request):
    rsp_empleado = requests.get(url+'usuarios/busqueda/sesion/1')
    if rsp_empleado.status_code == 200:
        data = rsp_empleado.json()
        usuario = data['usuariosr']
        id = usuario[0]['id']
        response = requests.put(url+f'login/id/{ id }')
    return render(request, 'presentacion/presentacion.html')
def iniciar_sesion(request):
    return render(request,'presentacion/usuariologin.html')
def registrar_login(request):
    return render(request,'presentacion/usuariosignup.html')

def usuariosignup(request):##############
    return render(request,'presentacion/usuariosignup.html')
def abrir_actualizar_cargos(request):#
    return render(request,'cargos/cargoactualizar.html')
def actualizar_cargo(request,id):#
    return render(request,'cargos/cargoactualizar.html')
def buscar_cargos(request):#
    return render(request,'cargos/buscarCargo.html')
#Documentos
def abrir_actualizar_documentos(request):#
    return render(request,'documentos/documentoactualizar.html')
def actualizar_documento(request,id):#
    return render(request,'documentos/documentoactualizar.html')
def buscar_documentos(request):#
    return render(request,'documentos/buscarDocumento.html')
def crear_documento(request):#
    return render(request,'documentos/documento.html')

#Impuesto
def abrir_actualizar_Impuestos(request):#
    return render(request,'Impuestos/ImpuestoActualizar.html')
def actualizar_Impuestos(request,id):#
    return render(request,'Impuestos/ImpuestoActualizar.html')
def buscar_Impuestos(request):#
    return render(request,'Impuestos/BuscarImpuesto.html')
def crear_Impuestos(request):#
    return render(request,'Impuestos/Impuesto.html')
def eliminar_Impuestos(request,id):#
    return render(request,'Impuestos/Impuesto.html')


#SubTipo
def abrir_actualizar_subtipo(request):#
    return render(request,'SubTipo/subtipoActualizar.html')
def actualizar_subtipo(request,id):#
    return render(request,'SubTipo/subtipoActualizar.html')
def buscar_subtipo(request):#
    return render(request,'SubTipo/buscarsubtipo.html')
def crear_subtipo(request):#
    return render(request,'SubTipo/subtipo.html')
def eliminar_subtipo(request,id):#
    return render(request,'SubTipo/subtipo.html')


#Tipos
def abrir_actualizar_tipo(request):#
    return render(request,'Tipos/tipoactualizar.html')
def actualizar_tipo(request,id):#
    return render(request,'Tipos/tipoactualizar.html')
def buscar_tipo(request):#
    return render(request,'Tipos/buscartipo.html')
def crear_tipo(request):#
    return render(request,'Tipos/tipo.html')
def eliminar_tipo(request,id):#
    return render(request,'Tipos/tipo.html')


#Tipo Muestra
def abrir_actualizar_TipoMuestra(request):#
    return render(request,'TipoMuestra/TMuestraActualizar.html')
def actualizar_TipoMuestra(request,id):#
    return render(request,'TipoMuestra/TMuestraActualizar.html')
def buscar_TipoMuestra(request):#
    return render(request,'TipoMuestra/BuscarTMuestra.html')
def crear_TipoMuestra(request):#
    return render(request,'TipoMuestra/TMuestra.html')
def eliminar_TipoMuestra(request,id):#
    return render(request,'TipoMuestra/TMuestra.html')


#Pacientes
def abrir_actualizar_pacientes(request):#
    return render(request,'Pacientes/PacienteActualizar.html')
def actualizar_pacientes(request,id):#
    return render(request,'Pacientes/PacienteActualizar.html')
def buscar_pacientes(request):#
    return render(request,'Pacientes/buscarPaciente.html')
def crear_paciente(request):#
    return render(request,'Pacientes/Paciente.html')
def eliminar_pacientes(request,id):#
    return render(request,'Pacientes/Paciente.html')


#Especialidades
def abrir_actualizar_especialidades(request):#
    return render(request,'especialidad/especialidadActualizar.html')
def actualizar_especialidades(request,id):#
    return render(request,'especialidad/especialidadActualizar.html')
def buscar_especialidades(request):#
    return render(request,'especialidad/BuscarEspecialidad.html')
def crear_especialidades(request):#
    return render(request,'especialidad/especialidad.html')
def eliminar_especialidades(request,id):#
    return render(request,'especialidad/especialidad.html')


#Muestra
def abrir_actualizar_muestras(request):#
    return render(request,'Muestras/MuestraActualizar.html')
def actualizar_muestras(request,id):#
    return render(request,'Muestras/MuestraActualizar.html')
def buscar_muestras(request):#
    return render(request,'Muestras/BuscarMuestra.html')
def crear_muestras(request):#
    return render(request,'Muestras/Muestra.html')
def eliminar_muestras(request,id):#
    return render(request,'Muestras/Muestra.html')

#Citas
def abrir_actualizar_citas(request):#
    return render(request,'citas/cita_actualizar.html')
def actualizar_citas(request,id):#
    return render(request,'citas/cita_actualizar.html')
def buscar_citas(request):#
    return render(request,'citas/cita_buscar.html')
def crear_citas(request):#
    return render(request,'citas/cita.html')
def eliminar_citas(request,id):#
    return render(request,'citas/cita.html')
def abrir_calendario(request):#
    return render(request,'citas/cita_calendario.html')

#impuesto historico
def buscar_impuesto_historico(request):#
    return render(request,'impuesto_historico/impuesto_historico_buscar.html')
def eliminar_impuesto_historico(request,id):#
    return render(request,'impuesto_historico/impuesto_historico.html')

#Sintomas
def abrir_actualizar_sintomas(request):#
    return render(request,'sintomas/actualizar_sintomas.html')
def actualizar_sintomas(request,id):#
    return render(request,'sintomas/buscar_sintomas.html')
def buscar_sintomas(request):#
    return render(request,'sintomas/buscar_sintomas.html')
def crear_sintomas(request):#
    return render(request,'sintomas/sintomas.html')
def eliminar_sintomas(request,id):#
    return render(request,'sintomas/sintomas.html')

#precio historico
def buscar_precio_historico_medicamento(request):#
    return render(request,'precio_historico_medicamento/buscar_precio_historico_medicamento.html')
def eliminar_precio_historico_medicamento(request,id):#
    return render(request,'precio_historico_medicamento/buscar_precio_historico_medicamento.html')

#costo historico
def buscar_costo_historico_medicamento(request):#
    return render(request,'costo_historico_medicamento/buscar_costo_historico_medicamento.html')
def eliminar_costo_historico_medicamento(request,id):#
    return render(request,'costo_historico_medicamento/buscar_costo_historico_medicamento.html')

#Medicamento
def abrir_actualizar_medicamentos(request):#
    return render(request,'medicamentos/actualizar_medicamentos.html')
def actualizar_medicamentos(request,id):#
    return render(request,'medicamentos/buscar_medicamentos.html')
def buscar_medicamentos(request):#
    return render(request,'medicamentos/buscar_medicamentos.html')
def crear_medicamentos(request):#
    return render(request,'medicamentos/medicamentos.html')
def eliminar_medicamentos(request,id):#
    return render(request,'medicamentos/medicamentos.html')

#Enfermedad
def abrir_actualizar_enfermedad(request):#
    return render(request,'enfermedad/actualizar_enfermedad.html')
def actualizar_enfermedad(request,id):#
    return render(request,'enfermedad/buscar_enfermedad.html')
def buscar_enfermedad(request):#
    return render(request,'enfermedad/buscar_menfermedad.html')
def crear_enfermedad(request):#
    return render(request,'enfermedad/enfermedad.html')
def eliminar_enfermedad(request,id):#
    return render(request,'enfermedad/enfermedad.html')

#Enfermedad Detalle
def buscar_enfermedad_detalle(request):#
    return render(request,'enfermedad_detalle/buscar_enfermedad_detalle.html')
def eliminar_enfermedad_detalle(request,id):#
    return render(request,'enfermedad_detalle/buscar_enfermedad_detalle.html')


def home(request):
    return render(request,'base_principal.html')
def iniciomenu(request):
    return render(request,'presentacion/iniciomenu.html')
#Usuarios
def usuario(request):
    return render(request,'usuario/usuario.html')

def crear_usuario(request):#
    return render(request,'usuario/registro.html')
def abrir_actualizar_usuario(request):#
    return render(request,'usuario/actualizar.html')
def actualizar_usuario(request,id):#
    return render(request,'usuario/actualizar.html')
def eliminar_usuario(request,id):#
    return render(request,'usuario/listar.html')
def buscar_usuarios(request):#
    return render(request,'usuario/listar.html')

def inicio(request):
    return render(request,'inicio.html',)
def empleado(request):
    return render(request,'empleado/empleado.html')

def crear_cargo(request):#
    return render(request,'cargos/cargo.html')

def especialidad(request):
    return render(request,'especialidad.html')
def documento(request):
    return render(request,'documento.html')
def buscarEmpleado(request):
    return render(request,'empleado/buscarEmpleado.html')

#Empleados
def abrir_actualizar_empleados(request):#
    return render(request,'empleado/EmpleadoActualizar.html')
def actualizar_empleados(request,id):#
    return render(request,'empleado/EmpleadoActualizar.html')
def buscar_empleados(request):#
    return render(request,'empleado/buscarEmpleado.html')
def crear_empleados(request):#
    return render(request,'empleado/empleado.html')
def eliminar_empleados(request,id):#
    return render(request,'empleado/empleado.html')

#Laboratorios
def abrir_actualizar_laboratorios(request):#
    return render(request,'Laboratorios/ActualizarLaboratorios.html')
def actualizar_laboratorios(request,id):#
    return render(request,'Laboratorios/ActualizarLaboratorios.html')
def buscar_laboratorios(request):#
    return render(request,'Laboratorios/BuscarLaboratorios.html')
def crear_laboratorios(request):#
    return render(request,'Laboratorios/Laboratorios.html')
def eliminar_laboratorios(request,id):#
    return render(request,'Laboratorios/Laboratorios.html')

#Metodo de pago
def abrir_actualizar_metodos_De_pago(request):#
    return render(request,'MetodoDePago/ActualizarMetodoDePago.html')
def actualizar_metodos_De_pago(request,id):#
    return render(request,'MetodoDePago/ActualizarMetodoDePago.html')
def buscar_metodos_De_pago(request):#
    return render(request,'MetodoDePago/BuscarMetodoDePago.html')
def crear_metodos_De_pago(request):#
    return render(request,'MetodoDePago/MetodoDePago.html')
def eliminar_metodos_De_pago(request,id):#
    return render(request,'MetodoDePago/MetodoDePago.html')

#proveedores
def abrir_actualizar_proveedor(request):#
    return render(request,'Proveedor/ProveedorActualizar.html')
def actualizar_proveedor(request,id):#
    return render(request,'Proveedor/ProveedorActualizar.html')
def buscar_proveedor(request):#
    return render(request,'Proveedor/BuscarProveedor.html')
def crear_proveedor(request):#
    return render(request,'Proveedor/Proveedor.html')
def eliminar_proveedor(request,id):#
    return render(request,'Proveedor/Proveedor.html')

#parametros_generales
def abrir_actualizar_parametros_generales(request):#
    return render(request,'parametros_generales/Actualizar_parametros_generales.html')
def actualizar_parametros_generales(request,id):#
    return render(request,'parametros_generales/Actualizar_parametros_generales.html')
def buscar_parametros_generales(request):#
    return render(request,'parametros_generales/Buscar_parametros_generales.html')
def crear_parametros_generalesr(request):#
    return render(request,'parametros_generales/parametros_generales.html')
def eliminar_parametros_generales(request,id):#
    return render(request,'parametros_generales/parametros_generales.html')

#Tratamientos
def abrir_actualizar_tratamientos(request):#
    return render(request,'tratamiento/Actualizar_tratamiento.html')
def actualizar_tratamientos(request,id):#
    return render(request,'tratamiento/Actualizar_tratamiento.html')
def buscar_tratamientos(request):#
    return render(request,'tratamiento/Buscar_tratamiento.html')
def crear_tratamientos(request):#
    return render(request,'tratamiento/tratamiento.html')
def eliminar_tratamientos(request,id):#
    return render(request,'tratamiento/Buscar_tratamiento.html')

#resultados
def abrir_actualizar_resultados(request):#
    return render(request,'Resultados/ActualizarResultados.html')
def actualizar_resultados(request,id):#
    return render(request,'Resultados/ActualizarResultados.html')
def buscar_resultados(request):#
    return render(request,'Resultados/BuscarResultados.html')
def crear_resultados(request):#
    return render(request,'Resultados/Resultados.html')
def eliminar_resultados(request,id):#
    return render(request,'Resultados/BuscarResultados.html')

#Diagnostico
def abrir_actualizar_diagnosticos(request):#
    return render(request,'diagnostico/Actualizar_diagnostico.html')
def actualizar_diagnosticos(request,id):#
    return render(request,'diagnostico/Actualizar_diagnostico.html')
def buscar_diagnosticos(request):#
    return render(request,'diagnostico/Buscar_diagnostico.html')
def crear_diagnosticos(request):#
    return render(request,'diagnostico/diagnostico.html')
def eliminar_diagnosticos(request,id):#
    return render(request,'diagnostico/Buscar_diagnostico.html')

#Examen
def abrir_actualizar_examenes(request):#
    return render(request,'examen/actualizar_examen.html')
def actualizar_examenes(request,id):#
    return render(request,'examen/actualizar_examen.html')
def buscar_examenes(request):#
    return render(request,'examen/buscar_examen.html')
def crear_examenes(request):#
    return render(request,'examen/examen.html')
def eliminar_examenes(request,id):#
    return render(request,'examen/buscar_examen.html')


#Diagnostico Detalle
def buscar_diagnostico_detalle(request):#
    return render(request,'diagnostico_detalle/buscar_diagnostico_detalle.html')
def eliminar_diagnostico_detalle(request,id):#
    return render(request,'diagnostico_detalle/buscar_diagnostico_detalle.html')


#precio historico tratamiento
def buscar_precio_historico_tratamiento(request):#
    return render(request,'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html')
def eliminar_precio_historico_tratamiento(request,id):#
    return render(request,'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html')

#precio historico examen
def buscar_precio_historico_examen(request):#
    return render(request,'precio_historico_examen/buscar_precio_historico_examen.html')
def eliminar_precio_historico_examen(request,id):#
    return render(request,'precio_historico_examen/buscar_precio_historico_examen.html')

#recaudo detalle examen 
def buscar_recaudo_detalle_examen(request):#
    return render(request,'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html')
def eliminar_recaudo_detalle_examen(request,id):#
    return render(request,'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html')

#recaudo detalle tratamiento 
def buscar_recaudo_detalle_tratamiento(request):#
    return render(request,'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html')
def eliminar_recaudo_detalle_tratamiento(request,id):#
    return render(request,'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html')

#recaudo detalle medicamento 
def buscar_recaudo_detalle_medicamento(request):#
    return render(request,'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html')
def eliminar_recaudo_detalle_medicamento(request,id):#
    return render(request,'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html')

#Consulta
def abrir_actualizar_consulta(request):#
    return render(request,'consulta/actualizar_consulta.html')
def actualizar_consulta(request,id):#
    return render(request,'consulta/buscar_consulta.html')
def buscar_consulta(request):#
    return render(request,'consulta/buscar_consulta.html')
def crear_consulta(request):#
    return render(request,'consulta/consulta.html')
def eliminar_consulta(request,id):#
    return render(request,'consulta/consulta.html')

#Expediente
def ver_detalle_expediente(request):#
    return render(request,'expediente/ver_detalle_expediente.html')
def abrir_actualizar_expediente(request):#
    return render(request,'expediente/actualizar_expediente.html')
def actualizar_expediente(request,id):#
    return render(request,'expediente/buscar_expediente.html')
def buscar_expediente(request):#
    return render(request,'expediente/buscar_mexpediente.html')
def crear_expediente(request):#
    return render(request,'expediente/expediente.html')
def eliminar_expediente(request,id):#
    return render(request,'expediente/expediente.html')

#detalle consulta 
def buscar_detalle_consulta(request):#
    return render(request,'detalle_consulta/buscar_detalle_consulta.html')
def eliminar_detalle_consulta(request,id):#
    return render(request,'detalle_consulta/buscar_detalle_consulta.html')

#precio historico consulta
def buscar_precio_historico_consulta(request):#
    return render(request,'precio_historico_consulta/buscar_precio_historico_consulta.html')
def eliminar_precio_historico_consulta(request,id):#
    return render(request,'precio_historico_consulta/buscar_precio_historico_consulta.html')


#precio historico Autorizacion Paciente
def abrir_actualizar_autorizacion(request):#
    return render(request,'Autorizacion/Autorizaractualizar.html')
def actualizar_autorizacion(request,id):#
    return render(request,'Autorizacion/AutorizarActualizar.html')
def buscar_autorizacion(request):#
    return render(request,'Autorizacion/buscarAutorizar.html')
def crear_autorizacion(request):#
    return render(request,'Autorizacion/Autorizar.html')
def eliminar_autorizacion(request,id):#
    return render(request,'Autorizacion/Autorizar.html')




#Traslado Paciente
def abrir_actualizar_traslados(request):#
    return render(request,'Traslados/actualizar_traslado.html')
def actualizar_traslados(request,id):#
    return render(request,'Traslados/actualizar_traslado.html')
def buscar_traslados(request):#
    return render(request,'Traslados/buscar_traslado.html')
def crear_traslados(request):#
    return render(request,'Traslados/traslado.html')
def eliminar_traslados(request,id):#
    return render(request,'Traslados/traslado.html')


#correlativo
def abrir_actualizar_correlativo(request):#
    return render(request,'correlativo/actualizar_correlativo.html')
def actualizar_correlativo(request,id):#
    return render(request,'correlativo/actualizar_correlativo.html')
def buscar_correlativo(request):#
    return render(request,'correlativo/buscar_correlativo.html')
def crear_correlativo(request):#
    return render(request,'correlativo/correlativo.html')
def eliminar_correlativo(request,id):#
    return render(request,'correlativo/correlativo.html')

#Recaudo
def crear_recaudo(request):#
    return render(request,'recaudo/recaudo.html')