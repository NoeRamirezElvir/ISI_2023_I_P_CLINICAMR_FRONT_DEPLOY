from decimal import Decimal
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
        numeroFactura = request.POST.get('numeroFactura')
        fechaActual = request.POST['fechaActual']
        idCorrelativo = int(request.POST['idCorrelativo'])
        idPaciente = int(request.POST['idPaciente'])
        idEmpleado = int(request.POST['idEmpleado'])
        idConsulta = int(request.POST['idConsulta'])
        idMetodo = int(request.POST['idMetodo'])
        estado = request.POST['estado']

        montoEfectivo = request.POST.get('montoEfectivo')
        numeroTarjeta = request.POST.get('numeroTarjeta')

        montoTarjeta = request.POST.get('montoTarjeta')
        subtotal = request.POST.get('subtotal')
        imp = request.POST.get('imp')
        total = request.POST.get('total')
        cambio = request.POST.get('cambio')

        #print(numeroFactura,fechaActual,idCorrelativo,idPaciente,idEmpleado,idConsulta,idMetodo,montoEfectivo,numeroTarjeta, montoTarjeta,subtotal,imp,total,cambio)


        medicamentos = request.POST['medicamentosSeleccionados']
        tratamientos = request.POST['tratamientosSeleccionados']
        examenes = request.POST['examenesSeleccionados']
        medicamentos_seleccionados = json.loads(medicamentos)
        tratamientos_seleccionados = json.loads(tratamientos)
        examenes_seleccionados = json.loads(examenes)

        medicamentos_lista = []
        for item in medicamentos_seleccionados:
            medicamento = {}
            medicamento['id'] = int(item.split(" - ")[0])
            medicamento['nombre'] = str(item.split(" - ")[1])
            medicamento['precio'] = float(item.split(" - ")[2])
            medicamento['impuesto'] = float(item.split(" - ")[3])
            medicamento['cantidad'] = int(item.split(" - ")[4])
            medicamentos_lista.append(medicamento)

        tratamientos_lista = []
        for item in tratamientos_seleccionados:
            tratamiento = {}
            tratamiento['id'] = int(item.split(" - ")[0])
            tratamiento['nombre'] = str(item.split(" - ")[1])
            tratamiento['precio'] = float(item.split(" - ")[2])
            tratamiento['impuesto'] = float(item.split(" - ")[3])
            tratamientos_lista.append(tratamiento)
        
        examenes_lista = []
        for item in examenes_seleccionados:
            examen = {}
            examen['id'] = int(item.split(" - ")[0])
            examen['nombre'] = str(item.split(" - ")[1])
            examen['precio'] = float(item.split(" - ")[2])
            examen['impuesto'] = float(item.split(" - ")[3])
            examenes_lista.append(examen)

        # Crear el diccionario final
        resultado = {}
        resultado['correlativo'] = idCorrelativo
        resultado['idPaciente'] = idPaciente
        resultado['fechaActual'] = fechaActual
        resultado['idEmpleado'] = idEmpleado
        resultado['idMetodo'] = idMetodo
        resultado['idConsulta'] = idConsulta
        resultado['montoEfectivo'] = montoEfectivo
        resultado['numeroTarjeta'] = numeroTarjeta
        resultado['estado'] = estado
        resultado['medicamentos'] = medicamentos_lista
        resultado['tratamientos'] = tratamientos_lista
        resultado['examenes'] = examenes_lista
        #print(resultado)
        resultado_json = json.dumps(resultado)

        registro_temp = {
            'fechaActual':fechaActual,
            'idCorrelativo':idCorrelativo,
            'idPaciente':idPaciente,
            'idEmpleado':idEmpleado,
            'idConsulta':idConsulta,
            'idMetodo':idMetodo,
            'estado':estado,
            'montoEfectivo':montoEfectivo,
            'numeroTarjeta':numeroTarjeta,
            'montoTarjeta':montoTarjeta,
            'subtotal':subtotal,
            'imp':imp,
            'total':total,
            'cambio':cambio,
            'medicamentos_lista':medicamentos_lista,
            'tratamientos_lista':tratamientos_lista,
            'examenes_lista':examenes_lista
        }
        context = {}
        response = requests.post(url+'recaudo/', resultado_json)
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            registro_temp['numeroFactura'] = data['numeroFactura']
            context = {'pacientes_list':pacientes_list,
                        'empleados_list':empleados_list,
                        'consultas_list':consultas_list,
                        'medicamentos_list':medicamentos_list,
                        'tratamientos_list':tratamientos_list,
                        'examenes_list':examenes_list,
                        'sar_list':sar_list,
                        'metodo_list':metodo_list,
                        'registro_temp':registro_temp,
                        'mensaje': mensaje
                        }
            
            datos_pdf = {
                
            }
            return render(request, 'recaudo/recaudo.html', context)
        else:
            data = response.json()
            mensaje = data['message']
            context = {'pacientes_list':pacientes_list,
                        'empleados_list':empleados_list,
                        'consultas_list':consultas_list,
                        'medicamentos_list':medicamentos_list,
                        'tratamientos_list':tratamientos_list,
                        'examenes_list':examenes_list,
                        'sar_list':sar_list,
                        'metodo_list':metodo_list,
                        'registro_temp':registro_temp,
                        'mensaje': mensaje
                        }
        return render(request, 'recaudo/recaudo.html', context)
    else:
        return render(request, 'recaudo/recaudo.html', context)


def abrir_actualizar_recaudo(request):
    return render(request, 'recaudo/actualizar_recaudo.html')

def actualizar_recaudo(request,id):
    return render(request, 'recaudo/actualizar_recaudo.html')

def buscar_recaudo(request):
    valor = request.GET.get('buscador', None)
    url2 = url + 'recaudo/busqueda/'
    if valor is not None and (len(valor)>0):
        if valor.isdigit():
            id = int(valor)
            response = requests.get(url2 + f'id/{id}')
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                recaudo = {}
                recaudo = data['recaudo']
                context = {'recaudo': recaudo, 'mensaje':mensaje}
                return render(request, 'recaudo/buscar_recaudo.html', context)  
            else:
                recaudo = []
                mensaje = 'No se encontraron registros'
                return render(request, 'recaudo/buscar_recaudo.html', {'recaudo': recaudo, 'mensaje': mensaje})     
        else:
            response = requests.get(url2+'numeroFactura/'+valor)
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                recaudo = {}
                recaudo = data['recaudo']
                context = {'recaudo': recaudo, 'mensaje':mensaje}
                return render(request, 'recaudo/buscar_recaudo.html', context)
            else:
                recaudo = []
                mensaje = 'No se encontraron registros'
                return render(request, 'recaudo/buscar_recaudo.html', {'recaudo': recaudo, 'mensaje': mensaje})
    else:
        response = requests.get(url+'recaudo/')
        if response.status_code == 200:
            data = response.json()
            recaudo = data['recaudo']
            mensaje = data['message']   
            return render(request, 'recaudo/buscar_recaudo.html', {'recaudo': recaudo, 'mensaje': mensaje})
        else:
            recaudo = []
            mensaje = 'No se encontraron registros'
        return render(request, 'recaudo/buscar_recaudo.html', {'recaudo': recaudo, 'mensaje': mensaje})



def eliminar_recaudo(request,id):
    return render(request, 'recaudo/buscar_recaudo.html')


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