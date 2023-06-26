import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes




url = 'https://clinicamr.onrender.com/api/'
def eliminar_enfermedad_detalle(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'enfermedadDetalle/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'enfermedadDetalle/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
            else:
                detalles = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje}
            return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)     
    except:
        rsp_detalles = requests.get(url + 'enfermedadDetalle/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'error': mensaje}
        return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)     

def buscar_enfermedad_detalle(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'enfermedadDetalle/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                response = requests.get(url2 + f'nombre/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)   
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
   
        else:
            response = requests.get(url+'enfermedadDetalle/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']   
                return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
            return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
