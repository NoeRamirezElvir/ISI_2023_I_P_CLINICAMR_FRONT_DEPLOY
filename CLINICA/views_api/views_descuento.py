from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
def listar_Descuentos(request):
    response = requests.get(url+'Descuentos/')
    if response.status_code == 200:
        data = response.json()
        Descuentos = data['Descuentos']
    else:
        Descuentos = []
    context = {'Descuentos': Descuentos}
    return render(request, 'Descuentos/BuscarDescuento.html', context)

def crear_Descuentos(request):
    
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            valor = float(request.POST['valor'])
            registro_temp = {'nombre': nombre, 'valor': valor}
            response = requests.post(url+'Descuentos/', json={'nombre': nombre, 'valor': valor})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_Descuentos')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_Descuentos')
                    logger.debug(f"Se ha registrado un Descuentos: Nombre={nombre}")
                return render(request, 'Descuentos/Descuento.html', {'mensaje': mensaje, 'Descuentos': registro_temp,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_Descuentos')
                logger.warning("No se pudo crear  Descuentos: " + mensaje)
                return render(request, 'Descuentos/Descuento.html', {'mensaje': mensaje, 'Descuentos': registro_temp,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_Descuentos','logs_Descuentos')
            logger.debug('Entrando a la funcion crear Descuentos')
            return render(request, 'Descuentos/Descuento.html',{'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    
    except Exception as e:
        logger = definir_log_info('excepcion_Descuentos','logs_Descuentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Descuentos/Descuento.html',{'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def abrir_actualizar_Descuentos(request):
    
    try:   
        if request.method == 'POST':
            resp = requests.get(url+'Descuentos/busqueda/id/'+str(request.POST['id_Descuentos']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                Descuentos = data['Descuentos']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('error_abrir_actualizar','logs_Descuentos')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar','logs_Descuentos')
                    logger.debug("Se obtuvo el Descuentos correspondiente a la actualizacion: " + mensaje)
            else:
                Descuentos = []
                logger = definir_log_info('error_abrir_actualizar','logs_Descuentos')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
            context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'Descuentos/DescuentoActualizar.html', context)
    
    except Exception as e:
        logger = definir_log_info('excepcion_Descuentos','logs_Descuentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
        return render(request, 'Descuentos/DescuentoActualizar.html', context)


def actualizar_Descuentos(request, id):
    
    try:
        if id == '':
            raise Exception("ID: esta vacio")
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            valor = float(request.POST['valor'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'Descuentos/id/{idTemporal}', json={'nombre': nombre, 'valor': valor})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el Descuentos relacionado con el id
            res = requests.get(url+f'Descuentos/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            Descuentos = data['Descuentos']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar','logs_Descuentos')
                logger.debug("Actualizacion correcta del Descuentos: " + mensaje)
                return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Descuentos':Descuentos ,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            else:
                logger = definir_log_info('error_actualizar','logs_Descuentos')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Descuentos':Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'Descuentos/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                Descuentos = data['Descuentos']
                mensaje = data['message']
                logger = definir_log_info('actualizar','logs_Descuentos')
                logger.debug("Obteniendo informacion del Descuentos: " + mensaje)
                return render(request, 'Descuentos/DescuentoActualizar.html', {'Nombre': nombre,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar','logs_Descuentos')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Nombre':nombre,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})

    except Exception as e:
        logger = definir_log_info('excepcion_Descuentos','logs_Descuentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Nombre':nombre,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})



def eliminar_Descuentos(request, id):   
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'Descuentos/id/{idTemporal}')
            res = response.json()
            rsp_Descuentos = requests.get(url + 'Descuentos/') 
            context ={}
            if rsp_Descuentos.status_code == 200:
                data = rsp_Descuentos.json()
                Descuentos = data['Descuentos']
                logger = definir_log_info('eliminar_Descuentos','logs_Descuentos')
                logger.info("Descuentos eliminado correctamente")
                context = {'Descuentos': Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
            else:
                Descuentos = []
                logger = definir_log_info('error_eliminar_Descuentos','logs_Descuentos')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                mensaje = res['message']
                context = {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
            return render(request, 'Descuentos/BuscarDescuento.html', context) 
    except:
        rsp_Descuentos = requests.get(url + 'Descuentos/') 
        context ={}
        if  rsp_Descuentos.status_code == 200:
            data = rsp_Descuentos.json()
            Descuentos = data['Descuentos']
            context = {'Descuentos': Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario(),'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
        else:
            Descuentos = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
        logger = definir_log_info('excepcion_Descuentos','logs_Descuentos')
        logger.exception("Ocurrio una excepcion:" + str(mensaje))
        context = {'Descuentos': Descuentos, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
        return render(request, 'Descuentos/BuscarDescuento.html', context)
    

def buscar_Descuentos(request):
        
    try:    
        valor = request.GET.get('buscador', None)
        url2 = url + 'Descuentos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Descuentos = {}
                    Descuentos = data['Descuentos']
                    logger = definir_log_info('buscar_Descuentos','logs_Descuentos')
                    logger.debug("Se obtuvo el Descuentos especifico(filtrado por ID): " + mensaje)
                    context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
                    return render(request, 'Descuentos/BuscarDescuento.html', context)   
                else:
                    Descuentos = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('error_buscar_Descuentos','logs_Descuentos')
                    logger.debug("No se obtuvo el Descuentos especifico(filtrado por ID): " + mensaje)
                    return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Descuentos = {}
                    Descuentos = data['Descuentos']
                    logger = definir_log_info('buscar_Descuentos','logs_Descuentos')
                    logger.debug("Se obtuvo el Descuentos especifico(filtrado por nombre): " + mensaje)
                    context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
                    return render(request, 'Descuentos/BuscarDescuento.html', context)
                else:
                    Descuentos = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('error_buscar_Descuentos','logs_Descuentos')
                    logger.debug("No se obtuvo el Descuentos especifico(filtrado por ID): " + mensaje)
                    return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            response = requests.get(url+'Descuentos/')
            if response.status_code == 200:
                data = response.json()
                Descuentos = data['Descuentos']
                mensaje = data['message']   
                logger = definir_log_info('buscar_Descuentos','logs_Descuentos')
                logger.debug("Se obtuvieron todos los Descuentoss: " + mensaje )
                return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            else:
                Descuentos = []
                mensaje = 'No se encontraron registros'
                logger = definir_log_info('error_buscar_Descuentos','logs_Descuentos')
                logger.debug("No se obtuvo el Descuentos especifico(filtrado por ID): " + mensaje)    
            return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    
    
    except Exception as e:
        logger = definir_log_info('excepcion_Descuentos','logs_Descuentos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'Descuentoss/')
        if response.status_code == 200:
            data = response.json()
            Descuentos = data['Descuentos']
            mensaje = data['message']  
            logger = definir_log_info('buscar_Descuentos','logs_Descuentos')
            logger.debug("Se obtuvieron todos los Descuentoss: " + mensaje ) 
            return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            Descuentos = []
            mensaje = 'No se encontraron Descuentos'
            logger = definir_log_info('error_buscar_Descuentos','logs_Descuentos')
            logger.debug("No se pudo obtener informacion de Descuentoss: " + mensaje)
        return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    