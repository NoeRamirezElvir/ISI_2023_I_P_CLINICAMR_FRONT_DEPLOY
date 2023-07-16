from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def listar_medicamentos(request):
    response = requests.get(url+'medicamentos/')
    if response.status_code == 200:
        data = response.json()
        medicamentos = data['medicamentos']
    else:
        medicamentos = []
    context = {'medicamentos': medicamentos}
    return render(request, 'medicamentos/buscar_medicamentos.html', context)

def crear_medicamentos(request):
    tipos = list_tipos()
    proveedores = list_proveedores()
    impuestos = list_impuestos()
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            idTipo = request.POST['idTipo']
            activo = request.POST['payment_method']
            stockActual = request.POST['stockActual']
            stockMinimo = request.POST['stockMinimo']
            stockMaximo = request.POST['stockMaximo']
            idImpuesto = request.POST['idImpuesto']
            idProveedor = request.POST['idProveedor']
            costoCompra = request.POST['costoCompra']
            precioVenta = request.POST['precioVenta']
            registro_temp = {'nombre': nombre,
                            'idTipo': int(idTipo),
                            'activo': int(activo),
                            'stockActual': stockActual,
                            'stockMinimo': stockMinimo,
                            'stockMaximo': stockMaximo,
                            'idImpuesto': int(idImpuesto),
                            'idProveedor': int(idProveedor),
                            'costoCompra': costoCompra,
                            'precioVenta': precioVenta
                            }
            response = requests.post(url+'medicamentos/', json={'nombre': nombre,
                                                                'idTipo': idTipo,
                                                                'activo': activo,
                                                                'stockActual': stockActual,
                                                                'stockMinimo': stockMinimo,
                                                                'stockMaximo': stockMaximo,
                                                                'idImpuesto': idImpuesto,
                                                                'idProveedor': idProveedor,
                                                                'costoCompra': costoCompra,
                                                                'precioVenta': precioVenta})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_medicamentos','logs_medicamentos')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_medicamentos','logs_medicamentos')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'medicamentos/medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                        'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                        'mensaje': mensaje, 
                                                                        'registro_temp': registro_temp,
                                                                        'tipos':tipos,
                                                                        'proveedores':proveedores,
                                                                        'impuestos':impuestos})
            else:
                data = response.json()
                mensaje = data['message']
                logger = definir_log_info('crear_medicamentos','logs_medicamentos')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'medicamentos/medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                        'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                        'mensaje': mensaje, 
                                                                        'registro_temp': registro_temp,
                                                                        'tipos':tipos,
                                                                        'proveedores':proveedores,
                                                                        'impuestos':impuestos})
        else:
            logger = definir_log_info('crear_medicamentos','logs_medicamentos')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'medicamentos/medicamentos.html',{'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                    'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                    'tipos':tipos,
                                                                    'proveedores':proveedores,
                                                                    'impuestos':impuestos})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_medicamentos','logs_medicamentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'medicamentos/medicamentos.html',{'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                'tipos':tipos,
                                                                'proveedores':proveedores,
                                                                'impuestos':impuestos})
   

def abrir_actualizar_medicamentos(request):
    tipos = list_tipos()
    proveedores = list_proveedores()
    impuestos = list_impuestos()
    try:
        if request.method == 'POST':
            resp = requests.get(url+'medicamentos/busqueda/id/'+str(request.POST['id_medicamentos']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                medicamentos = data['medicamentos']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_medicamentos','logs_medicamentos')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_medicamentos','logs_medicamentos')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                medicamentos = []
                logger = definir_log_info('abrir_actualizar_medicamentos','logs_medicamentos')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos,'tipos':tipos, 'proveedores':proveedores, 'impuestos':impuestos, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'medicamentos/actualizar_medicamentos.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_medicamentos','logs_medicamentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        medicamentos = []
        context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos,'tipos':tipos, 'proveedores':proveedores, 'impuestos':impuestos, 'mensaje':mensaje}
        mensaje = data['message']
        return render(request, 'medicamentos/actualizar_medicamentos.html', context)
   

def actualizar_medicamentos(request, id):
    tipos = list_tipos()
    proveedores = list_proveedores()
    impuestos = list_impuestos()
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            idTipo = request.POST['idTipo']
            activo = request.POST['payment_method']
            stockActual = request.POST['stockActual']
            stockMinimo = request.POST['stockMinimo']
            stockMaximo = request.POST['stockMaximo']
            idImpuesto = request.POST['idImpuesto']
            idProveedor = request.POST['idProveedor']
            costoCompra = request.POST['costoCompra']
            precioVenta = request.POST['precioVenta']
            response = requests.put(url+f'medicamentos/id/{idTemporal}', json={'nombre': nombre,
                                                                                'idTipo': idTipo,
                                                                                'activo': activo,
                                                                                'stockActual': stockActual,
                                                                                'stockMinimo': stockMinimo,
                                                                                'stockMaximo': stockMaximo,
                                                                                'idImpuesto': idImpuesto,
                                                                                'idProveedor': idProveedor,
                                                                                'costoCompra': costoCompra,
                                                                                'precioVenta': precioVenta,
                                                                                })
            rsp =  response.json()
            res = requests.get(url+f'medicamentos/busqueda/id/{idTemporal}')
            data = res.json()
            medicamentos = data['medicamentos']
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_medicamentos','logs_medicamentos')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'medicamentos/actualizar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                                    'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                                    'mensaje': mensaje,
                                                                                    'medicamentos':medicamentos,
                                                                                    'tipos':tipos,
                                                                                    'proveedores':proveedores,
                                                                                    'impuestos':impuestos})
            else:
                mensaje = rsp['message']       
                logger = definir_log_info('actualizar_medicamentos','logs_medicamentos')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                    
                return render(request, 'medicamentos/actualizar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                                    'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                                    'mensaje': mensaje,
                                                                                    'medicamentos':medicamentos,
                                                                                    'tipos':tipos,
                                                                                    'proveedores':proveedores,
                                                                                    'impuestos':impuestos})
        else:
            response = requests.get(url+f'medicamentos/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                medicamentos = data['medicamentos']
                mensaje = data['message']
                logger = definir_log_info('actualizar_medicamentos','logs_medicamentos')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'medicamentos/actualizar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                                    'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                                    'mensaje': mensaje,
                                                                                    'medicamentos':medicamentos,
                                                                                    'tipos':tipos,
                                                                                    'proveedores':proveedores,
                                                                                    'impuestos':impuestos})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_medicamentos','logs_medicamentos')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'medicamentos/actualizar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                                    'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                                    'mensaje': mensaje,
                                                                                    'medicamentos':medicamentos,
                                                                                    'tipos':tipos,
                                                                                    'proveedores':proveedores,
                                                                                    'impuestos':impuestos})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_medicamentos','logs_medicamentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        mensaje = data['message']
        return render(request, 'medicamentos/actualizar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),
                                                                            'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                            'mensaje': mensaje,
                                                                            'medicamentos':[],
                                                                            'tipos':tipos,
                                                                            'proveedores':proveedores,
                                                                            'impuestos':impuestos})
   

def eliminar_medicamentos(request, id):  
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'medicamentos/id/{idTemporal}')
            res = response.json()
            rsp_medicamentos = requests.get(url + 'medicamentos/')
            context = {} 
            if rsp_medicamentos.status_code == 200:
                data = rsp_medicamentos.json()
                medicamentos = data['medicamentos']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_medicamentos','logs_medicamentos')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_medicamentos','logs_medicamentos')
                    logger.info("No se ha podido eliminar el registro")
                context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos}
            else:
                medicamentos = []
                mensaje = res['message']
                logger = definir_log_info('eliminar_medicamentos','logs_medicamentos')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje}
            return render(request, 'medicamentos/buscar_medicamentos.html', context) 
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_medicamentos','logs_medicamentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_medicamentos = requests.get(url + 'medicamentos/') 
        context = {}
        if  rsp_medicamentos.status_code == 200:
            data = rsp_medicamentos.json()
            medicamentos = data['medicamentos']
            context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos}
        else:
            medicamentos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'error': mensaje}
        return render(request, 'medicamentos/buscar_medicamentos.html', context)
    
def buscar_medicamentos(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'medicamentos/busqueda/'

        if valor is not None and (len(valor)>0): 
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    medicamentos = {}
                    medicamentos = data['medicamentos']
                    if medicamentos != []:   
                        logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje':mensaje}
                    return render(request, 'medicamentos/buscar_medicamentos.html', context)    
                else:
                    medicamentos = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    medicamentos = {}
                    medicamentos = data['medicamentos']
                    if medicamentos != []:   
                        logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje':mensaje}
                    return render(request, 'medicamentos/buscar_medicamentos.html', context)
                else:
                    medicamentos = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'medicamentos/')
            if response.status_code == 200:
                data = response.json()
                medicamentos = data['medicamentos']
                mensaje = data['message']   
                if medicamentos != []:   
                    logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
            else:
                medicamentos = []
                mensaje = 'No se encontraron registros'
                logger = definir_log_info('buscar_medicamentos','logs_medicamentos')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_medicamentos','logs_medicamentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'medicamentos/')
        if response.status_code == 200:
            data = response.json()
            medicamentos = data['medicamentos']
            mensaje = data['message']   
            return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
        else:
            medicamentos = []
            mensaje = 'No se encontraron registros'
        return render(request, 'medicamentos/buscar_medicamentos.html', {'reportes_lista':DatosReportes.cargar_lista_medicamentos(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'medicamentos': medicamentos, 'mensaje': mensaje})
    

def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/medicamento')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list

def list_proveedores():
    rsp_proveedores = requests.get(url+'proveedores/')
    if rsp_proveedores.status_code == 200:
        data = rsp_proveedores.json()
        proveedores_list = data['proveedores']
        return proveedores_list
    else:
        proveedores_list = []
        return proveedores_list

def list_impuestos():
    rsp_impuestos = requests.get(url+'Impuestos/')
    if rsp_impuestos.status_code == 200:
        data = rsp_impuestos.json()
        impuestos_list = data['Impuestos']
        return impuestos_list
    else:
        impuestos_list = []
        return impuestos_list