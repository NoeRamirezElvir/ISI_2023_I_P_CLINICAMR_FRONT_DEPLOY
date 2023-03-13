from django.http import HttpResponse
import json
from django.shortcuts import render
import requests



def presentacion(request):
    return render(request,'presentacion/presentacion.html')
def iniciar_sesion(request):
    return render(request,'presentacion/usuariologin.html')
def registrar_login(request):
    return render(request,'presentacion/usuariosignup.html')

def usuariosignup(request):##############
    return render(request,'presentacion/usuariosignup.html')
def abrir_actualizar_cargos(request):#
    return render(request,'cargoactualizar.html')
def actualizar_cargo(request,id):#
    return render(request,'cargoactualizar.html')
def buscar_cargos(request):#
    return render(request,'buscarCargo.html')
#Documentos
def abrir_actualizar_documentos(request):#
    return render(request,'documentoactualizar.html')
def actualizar_documento(request,id):#
    return render(request,'documentoactualizar.html')
def buscar_documentos(request):#
    return render(request,'buscarDocumento.html')
def crear_documento(request):#
    return render(request,'documento.html')

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


#Pacientes
def abrir_actualizar_pacientes(request):#
    return render(request,'Pacientes/PacienteActualizar.html')
def actualizar_pacientes(request,id):#
    return render(request,'Pacientes/PacienteActualizar.html')
def buscar_pacientes(request):#
    return render(request,'Pacientes/buscarPaciente.html')
def crear_pacientes(request):#
    return render(request,'Pacientes/Paciente.html')
def eliminar_pacientes(request,id):#
    return render(request,'Pacientes/Paciente.html')


#Especialidades
def abrir_actualizar_especialidades(request):#
    return render(request,'especialidadActualizar.html')
def actualizar_especialidades(request,id):#
    return render(request,'especialidadActualizar.html')
def buscar_especialidades(request):#
    return render(request,'BuscarEspecialidad.html')
def crear_especialidades(request):#
    return render(request,'especialidad.html')
def eliminar_especialidades(request,id):#
    return render(request,'especialidad.html')


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
    return render(request,'usuario/inicio.html',)
def empleado(request):
    return render(request,'empleado/empleado.html')

def crear_cargo(request):#
    return render(request,'cargo.html')

def especialidad(request):
    return render(request,'especialidad.html')
def documento(request):
    return render(request,'documento.html')
def buscarEmpleado(request):
    return render(request,'empleado/buscarEmpleado.html')



#Empleados
