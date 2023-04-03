import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def eliminar_recaudo_detalle_examen(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'recaudoDetalleExamen/id/{idTemporal}')
        res = response.json()
        rsp_detalles = requests.get(url + 'recaudoDetalleExamen/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = res['message']
        context = {'detalles': detalles, 'mensaje': mensaje}
        return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)     
    
def buscar_recaudo_detalle_examen(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'recaudoDetalleExamen/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)
            else:
                response = requests.get(url2 + f'nombre/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)      
        else:
            response = requests.get(url+'recaudoDetalleExamen/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']   
                return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
            return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'detalles': detalles, 'mensaje': mensaje})
