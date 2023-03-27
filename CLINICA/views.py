from django.http import HttpResponse
import json
from django.shortcuts import render, redirect

def presentacion(request):
    return render(request,'presentacion/presentacion.html')
def salir_presentacion(request):
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

#costo historico
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