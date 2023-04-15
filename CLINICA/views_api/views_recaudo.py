from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'

def crear_recaudo(request):
    pacientes_list = list_pacientes()
    empleados_list = list_empleados()
    consultas_list = list_consultas()
    medicamentos_list = list_medicamentos()
    tratamientos_list = list_tratamientos()
    examenes_list = list_examenes()
    sar_list = list_sar()
    metodo_list = list_metodo_pago()
    context = {'pacientes_list':pacientes_list,
                'empleados_list':empleados_list,
                'consultas_list':consultas_list,
                'medicamentos_list':medicamentos_list,
                'tratamientos_list':tratamientos_list,
                'examenes_list':examenes_list,
                'sar_list':sar_list,
                'metodo_list':metodo_list,}
    if request.method == 'POST':
        pass
    else:
        return render(request, 'recaudo/recaudo.html', context)
    


def list_parametros():
    rsp_parametros = requests.get(url+'parametrosgenerales/')
    if rsp_parametros.status_code == 200:
        data = rsp_parametros.json()
        list_parametros = data['parametrosgenerales']
        return list_parametros
    else:
        list_parametros = []
        return list_parametros
     
def list_sar():
    rsp_correlativo = requests.get(url+'correlativo/')
    if rsp_correlativo.status_code == 200:
        data = rsp_correlativo.json()
        list_correlativo = data['correlativo']
        return list_correlativo
    else:
        list_correlativo = []
        return list_correlativo

def list_metodo_pago():
    rsp_metodo = requests.get(url+'metodop/')
    if rsp_metodo.status_code == 200:
        data = rsp_metodo.json()
        list_metodo = data['metodop']
        return list_metodo
    else:
        list_metodo = []
        return list_metodo

def list_consultas():
    rsp_consultas = requests.get(url+'consultas/')
    if rsp_consultas.status_code == 200:
        data = rsp_consultas.json()
        list_consultas = data['consultas']
        return list_consultas
    else:
        list_consultas = []
        return list_consultas
    
def list_medicamentos():
    rsp_medicamentos = requests.get(url+'medicamentos/')
    if rsp_medicamentos.status_code == 200:
        data = rsp_medicamentos.json()
        list_medicamentos = data['medicamentos']
        return list_medicamentos
    else:
        list_medicamentos = []
        return list_medicamentos
    
def list_tratamientos():
    rsp_tratamientos = requests.get(url+'tratamientos/')
    if rsp_tratamientos.status_code == 200:
        data = rsp_tratamientos.json()
        list_tratamientos = data['tratamientos']
        return list_tratamientos
    else:
        list_tratamientos = []
        return list_tratamientos
    
def list_examenes():
    rsp_examenes = requests.get(url+'examen/')
    if rsp_examenes.status_code == 200:
        data = rsp_examenes.json()
        list_examenes = data['examenes']
        return list_examenes
    else:
        list_examenes = []
        return list_examenes
    
def list_pacientes():
    rsp_pacientes = requests.get(url+'pacientes/')
    if rsp_pacientes.status_code == 200:
        data = rsp_pacientes.json()
        list_pacientes = data['pacientes']
        return list_pacientes
    else:
        list_pacientes = []
        return list_pacientes
    
def list_empleados():
    usuario = requests.get(url+'usuarios/busqueda/sesion/1')
    data_user = usuario.json()['usuariosr']
    id=data_user[0]['idEmpleado_id']
    rsp_empleados = requests.get(url+f'empleados/busqueda/id/{id}')
    #rsp_empleados = requests.get(url+'empleados/')
    if rsp_empleados.status_code == 200:
        data = rsp_empleados.json()
        list_empleados = data['empleados']
        return list_empleados
    else:
        list_empleados = []
        return list_empleados