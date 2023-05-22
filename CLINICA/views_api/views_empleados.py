from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
url = 'https://clinicamr.onrender.com/api/'


def listar_empleados(request):
    response = requests.get(url+'empleados/')
    if response.status_code == 200:
        data = response.json()
        empleados = data['empleados']
    else:
        empleados  = []
    context = {'empleados': empleados}
    return render(request, 'empleado/buscarEmpleado.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_empleados(request):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()
    
    
    
    if request.method == 'POST':
        
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        fechaNacimiento = request.POST['fechaNacimiento']
        idTipoDocumento = int(request.POST['idTipoDocument1'])
        idEspecialidadMedico=int(request.POST['idEspecialidadMedic1'])
        idCargoEmpleado =int(request.POST['idCargoEmplead1'])
        documento= request.POST ['documento']
        telefono = request.POST['telefono']
        email = request.POST['email']
        direccion = request.POST ['direccion']
        activo = int(request.POST['payment_method'])
        
        registro_temp={'nombre': nombre,'apellidos':apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado,'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo}
        response = requests.post(url+'empleados/', json={'nombre': nombre,'apellidos': apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumentos':idTipoDocumento, 'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado, 'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo })
        empleadosdata={}
        if response.status_code == 200:
            empleadosdata = response.json()
            mensaje = empleadosdata['message']
            return render(request, 'empleado/empleado.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'registro_temp':registro_temp})
        else:
            empleadosdata = response.json()
            mensaje = empleadosdata['message']
            return render(request, 'empleado/empleado.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'registro_temp':registro_temp})
    else:
        return render(request, 'empleado/empleado.html', { 'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})

def list_tipodocumento():
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
        data = rsp_TipoDocumento.json()
        TipoDocumento = data['documentos']
        return TipoDocumento

    else:
        TipoDocumento = []
        return TipoDocumento
    

def list_EspecialidadMedico():
    rsp_EspecialidadMedico = requests.get(url +'especialidad/')
    if rsp_EspecialidadMedico.status_code == 200:
        data = rsp_EspecialidadMedico.json()
        EspecialidadMedico = data ['especialidad']
        return EspecialidadMedico
    else:
        EspecialidadMedico=[]
        return EspecialidadMedico
    
def list_cargoEmpleado():
    rsp_CargoEmpleado = requests.get(url +'cargos/')
    if rsp_CargoEmpleado.status_code == 200:
        data = rsp_CargoEmpleado.json()
        CargoEmpleado = data ['cargos']
        return CargoEmpleado
         
    else:
         
         CargoEmpleado=[]
         return CargoEmpleado
     
     

def abrir_actualizar_empleados(request):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()


    if request.method == 'POST':
         resp = requests.get(url+'empleados/busqueda/id/'+str(request.POST['id_empleados']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            empleados = data['empleados']
            mensaje = data['message']
         else:
            empleados = []
         context = {'empleados': empleados,'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'empleado/EmpleadoActualizar.html', context)   
    
def actualizar_empleados(request, id):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()

    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        fechaNacimiento = request.POST['fechaNacimiento']
        idTipoDocumento = int(request.POST['idTipoDocument1'])
        idEspecialidadMedico=int(request.POST['idEspecialidadMedic1'])
        idCargoEmpleado =int(request.POST['idCargoEmplead1'])
        documento= request.POST ['documento']
        telefono = request.POST['telefono']
        email = request.POST['email']
        direccion = request.POST ['direccion']
        activo =int(request.POST['payment_method'])
        
        


        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'empleados/id/{idTemporal}', json={'nombre': nombre,'apellidos': apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumentos':idTipoDocumento,'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado,'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo })
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'empleados/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        empleados = data['empleados']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'empleado/EmpleadoActualizar.html', {'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'empleado/EmpleadoActualizar.html', {'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'empleados/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            empleados = data['empleados']
            mensaje = data['message']
            return render(request, 'empleado/EmpleadoActualizar.html', {'empleados': empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
        else:
            mensaje = data['message']
            return render(request, 'empleado/EmpleadoActualizar.html', {'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})

def eliminar_empleados(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'empleados/id/{idTemporal}')
            res = response.json()
            rsp_empleados = requests.get(url + 'empleados/') 
            if rsp_empleados.status_code == 200:
                data = rsp_empleados.json()
                empleados = data['empleados']
            else:
                empleados = []
            mensaje = res['message']
            context = {'empleados': empleados, 'mensaje': mensaje}
            return render(request, 'empleado/buscarEmpleado.html', context)     
    except:
        rsp_empleados = requests.get(url + 'empleados/') 
        if rsp_empleados.status_code == 200:
            data = rsp_empleados.json()
            empleados = data['empleados']
        else:
            empleados = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'empleados': empleados, 'error': mensaje}
        return render(request, 'empleado/buscarEmpleado.html', context)     
    
def buscar_empleados(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'empleados/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    empleados = {}
                    empleados = data['empleados']
                    context = {'empleados': empleados, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'empleado/buscarEmpleado.html', context)       
                else:
                    empleados = []
                    mensaje = 'No se encontro empleados'
                    return render(request, 'empleado/buscarEmpleado.html', {'empleados': empleados, 'mensaje': mensaje})
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    empleados = {}
                    empleados = data['empleados']
                    context = {'empleados': empleados, 'mensaje':mensaje}
                    return render(request, 'empleado/buscarEmpleado.html', context)
                else:
                    empleados = []
                    mensaje = 'No se encontro empleados'
                    return render(request, 'empleado/buscarEmpleado.html', {'empleados': empleados, 'mensaje': mensaje})
        else:
            response = requests.get(url+'empleados/')
            if response.status_code == 200:
                data = response.json()
                empleados = data['empleados']
                mensaje = data['message']   
                return render(request, 'empleado/buscarEmpleado.html', {'empleados': empleados, 'mensaje': mensaje})
            else:
                empleados = []
                mensaje = 'No se encontro empleados'
            return render(request, 'empleado/buscarEmpleado.html', {'empleados': empleados, 'mensaje': mensaje})
    
