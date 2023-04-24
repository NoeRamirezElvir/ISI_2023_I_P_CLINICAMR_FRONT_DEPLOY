from decimal import Decimal
from django.http import HttpResponse
import json
from django.shortcuts import redirect, render
from django.urls import reverse
import requests

from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



url = 'http://localhost:8080/api/'

def crear_recaudo(request):  
    rsp = requests.get(url+f'listasRecaudo/')
    data = rsp.json()
    context = data

    if request.method == 'POST':
        fechaActual = request.POST['fechaActual']
        idCorrelativo = int(request.POST['idCorrelativo'])
        idPaciente = int(request.POST['idPaciente'])
        idEmpleado = int(request.POST['idEmpleado'])
        idConsulta = int(request.POST['idConsulta'])
        idMetodo = int(request.POST['idMetodo'])
        idDescuento = int(request.POST['idDescuento'])
        estado = request.POST['estado']

        montoEfectivo = request.POST.get('montoEfectivo') if request.POST.get('montoEfectivo') else '00.00'
        numeroTarjeta = request.POST.get('numeroTarjeta') if request.POST.get('numeroTarjeta') else 'N/A'
        serie = request.POST['serie']
        montoTarjeta = request.POST.get('montoTarjeta') if request.POST.get('montoTarjeta') else '00.00'

        subtotal = request.POST.get('subtotal')
        imp = request.POST.get('imp')
        total = request.POST.get('total')
        cambio = request.POST.get('cambio') if request.POST.get('cambio') else '00.00'
        descuento = request.POST.get('des') if request.POST.get('des') else '00.00'

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
            impuesto = float(item.split(" - ")[3])
            medicamento['impuesto'] = "{:.2f}".format(impuesto)
            medicamento['cantidad'] = int(item.split(" - ")[4])
            medicamentos_lista.append(medicamento)

        tratamientos_lista = []
        for item in tratamientos_seleccionados:
            tratamiento = {}
            tratamiento['id'] = int(item.split(" - ")[0])
            tratamiento['nombre'] = str(item.split(" - ")[1])
            tratamiento['precio'] = float(item.split(" - ")[2])
            impuesto = float(item.split(" - ")[3])
            tratamiento['impuesto'] = "{:.2f}".format(impuesto)
            tratamientos_lista.append(tratamiento)
        
        examenes_lista = []
        for item in examenes_seleccionados:
            examen = {}
            examen['id'] = int(item.split(" - ")[0])
            examen['nombre'] = str(item.split(" - ")[1])
            examen['precio'] = float(item.split(" - ")[2])
            impuesto = float(item.split(" - ")[3])
            examen['impuesto'] = "{:.2f}".format(impuesto)
            examenes_lista.append(examen)

        # Crear el diccionario final
        resultado = {}
        resultado['correlativo'] = idCorrelativo
        resultado['idPaciente'] = idPaciente
        resultado['fechaActual'] = fechaActual
        resultado['idEmpleado'] = idEmpleado
        resultado['idMetodo'] = idMetodo
        resultado['idConsulta'] = idConsulta
        resultado['idDescuento'] = idDescuento
        resultado['montoEfectivo'] = montoEfectivo
        resultado['numeroTarjeta'] = numeroTarjeta
        resultado['estado'] = estado
        resultado['medicamentos'] = medicamentos_lista
        resultado['tratamientos'] = tratamientos_lista
        resultado['examenes'] = examenes_lista
        resultado['total'] = total
        resultado['subtotal'] = subtotal
        resultado['cambio'] = cambio
        resultado['descuento'] = descuento
        resultado['imp'] = imp
        resultado['montoTarjeta'] = montoTarjeta
        
        
        resultado_json = json.dumps(resultado)

        registro_temp = {
            'fechaActual':fechaActual,
            'idCorrelativo':idCorrelativo,
            'idPaciente':idPaciente,
            'idEmpleado':idEmpleado,
            'idConsulta':idConsulta,
            'idMetodo':idMetodo,
            'idDescuento':idDescuento,
            'estado':estado,
            'montoEfectivo':montoEfectivo,
            'numeroTarjeta':numeroTarjeta,
            'montoTarjeta':montoTarjeta,
            'subtotal':subtotal,
            'serie':serie,
            'imp':imp,
            'total':total,
            'cambio':cambio,
            'descuento':descuento,
            'medicamentos_lista':medicamentos_lista,
            'tratamientos_lista':tratamientos_lista,
            'examenes_lista':examenes_lista
        }
        
        response = requests.post(url+'recaudo/', resultado_json)

        if not idConsulta == 0:
            rsp_consulta = requests.get(url+f'consultas/busqueda/id/{idConsulta}')
            data = rsp_consulta.json()
            consulta = data['consultas']
        else:
            consulta = None
        data={}
        data = response.json()
        mensaje = data['message']
        
        if mensaje == "Registro Exitoso.":
            data = response.json()
            mensaje = data['message']
            registro_temp['numeroFactura'] = data['numeroFactura']
            datos_pdf = data['datos_pdf']
            datos_pdf['medicamentos'] = medicamentos_lista
            datos_pdf['tratamientos'] = tratamientos_lista
            datos_pdf['examenes'] = examenes_lista
            datos_pdf['consulta'] = consulta
            datos_pdf['subtotalFactura'] = subtotal
            datos_pdf['totalFactura'] = format(float(total),',.2f')
            datos_pdf['impuestosFactura'] = imp
            datos_pdf['numeroTarjeta'] = numeroTarjeta
            datos_pdf['montoTarjeta'] = format(float(montoTarjeta),',.2f')
            datos_pdf['montoEfectivo'] = format(float(montoEfectivo),',.2f')
            datos_pdf['cambio'] = format(float(cambio),',.2f')
            datos_pdf['descuento'] = format(float(descuento),',.2f')
            datos_pdf['numMasc'] = mascara_tarjeta(numeroTarjeta)
                      

            #print(datos_pdf)
            context['mensaje'] =  mensaje
            context['datos_pdf'] = datos_pdf
            context['registro_temp'] = registro_temp
            
            pdf = render_to_pdf('recaudo/recaudo_pdf.html', context)
            response_pdf = HttpResponse(pdf, content_type='application/pdf')
            response_pdf['Content-Disposition'] = 'attachment; filename="recaudo.pdf"'
            return response_pdf
        else:
            data = response.json()
            mensaje = data['message']
            context['registro_temp'] = registro_temp
            context['mensaje'] =  mensaje
        return render(request, 'recaudo/recaudo.html', context)
    else:
        return render(request, 'recaudo/recaudo.html', context)

def actualizar_recaudo(request,id):
    if request.method == 'POST':
        idTemporal = id
        estado = request.POST['mi-input']
        response = requests.put(url+f'recaudo/id/{idTemporal}', json={'estado': estado})
        rsp =  response.json()

        rsp_recaudos = requests.get(url+'recaudo/')
        if rsp_recaudos.status_code == 200:
            data = rsp_recaudos.json()
            recaudo = data['recaudo'] 
        else:
            recaudo = []

        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'recaudo/buscar_recaudo.html', {'mensaje': mensaje, 'recaudo': recaudo})
        else:
            mensaje = rsp['message']                            
            return render(request, 'recaudo/buscar_recaudo.html', {'mensaje': mensaje,'recaudo': recaudo})

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
    try:
        if request.method == 'POST' and 'eliminar' in request.POST:
            idTemporal = id
            response = requests.delete(url + f'recaudo/id/{idTemporal}')
            res = response.json()
            rsp_recaudo = requests.get(url + 'recaudo/') 
            if rsp_recaudo.status_code == 200:
                data = rsp_recaudo.json()
                recaudo = data['recaudo']
            else:
                recaudo = []
            mensaje = res['message']
            context = {'recaudo': recaudo, 'mensaje': mensaje}
            return render(request, 'recaudo/buscar_recaudo.html', context)   
    except:
        rsp_recaudo = requests.get(url + 'recaudo/') 
        if rsp_recaudo.status_code == 200:
            data = rsp_recaudo.json()
            recaudo = data['recaudo']
        else:
            recaudo = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'recaudo': recaudo, 'error': mensaje}
        return render(request, 'recaudo/buscar_recaudo.html', context)   

def reimprimir_recaudo(request,id):
    if request.method == 'POST' and 'reimprimir' in request.POST:
        rsp = requests.get(url + f'reimprimirPdf/id/{id}')
        data = rsp.json()

        datos_pdf = data['datos_pdf']
        context = { 'datos_pdf': datos_pdf}

        pdf = render_to_pdf('recaudo/recaudo_pdf.html', context)
        response_pdf = HttpResponse(pdf, content_type='application/pdf')
        response_pdf['Content-Disposition'] = 'attachment; filename="recaudo.pdf"'
        return response_pdf

def list_sar():
    rsp_correlativo = requests.get(url+'correlativo/busqueda/activo/1')
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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def mascara_tarjeta(str):
    if str is None or len(str) <= 4:
        return str
    else:
        ultimos_4_caracteres = str[-4:]
        asteriscos = "*" * (len(str) - 4)
        return "{}{}".format(asteriscos, ultimos_4_caracteres)
