import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes

url = 'https://clinicamr.onrender.com/api/'
def eliminar_recaudo_detalle_tratamiento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'recaudoDetalleTratamiento/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'recaudoDetalleTratamiento/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
            else:
                detalles = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje}
            return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', context)     
    except:
        rsp_detalles = requests.get(url + 'recaudoDetalleTratamiento/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'error': mensaje}
        return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', context)     

def buscar_recaudo_detalle_tratamiento(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'recaudoDetalleTratamiento/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

            else:
                response = requests.get(url2 + f'numeroFactura/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', context)      
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

        else:
            response = requests.get(url+'recaudoDetalleTratamiento/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']   
                return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
            return render(request, 'recaudo_detalle_tratamiento/buscar_recaudo_detalle_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
