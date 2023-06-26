import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes



url = 'https://clinicamr.onrender.com/api/'
def eliminar_impuesto_historico(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'impuestoHistorico/id/{idTemporal}')
            res = response.json()
            rsp_pacientes = requests.get(url + 'impuestoHistorico/') 
            if rsp_pacientes.status_code == 200:
                data = rsp_pacientes.json()
                historicos = data['historicos']
            else:
                historicos = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)     
    except:
        rsp_pacientes = requests.get(url + 'impuestoHistorico/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'error': mensaje}
        return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)     
   
def buscar_impuesto_historico(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'impuestoHistorico/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón citas'
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
              
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón citas'
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            response = requests.get(url+'impuestoHistorico/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón citas'
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
