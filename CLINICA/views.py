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
def abrir_actualizar_impuesto_historico(request):#
    return render(request,'impuesto_historico/impuesto_historico_actualizar.html')
def actualizar_impuesto_historico(request,id):#
    return render(request,'impuesto_historico/impuesto_historico_buscar.html')
def buscar_impuesto_historico(request):#
    return render(request,'impuesto_historico/impuesto_historico_buscar.html')
def crear_impuesto_historico(request):#
    return render(request,'impuesto_historico/impuesto_historico.html')
def eliminar_impuesto_historico(request,id):#
    return render(request,'impuesto_historico/impuesto_historico.html')



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
