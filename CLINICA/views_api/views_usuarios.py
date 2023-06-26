from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import render
from passlib.context import CryptContext
import requests
from django.shortcuts import redirect
from ..views_api.datos_reporte import DatosReportes



url = 'https://clinicamr.onrender.com/api/'
#LOS METODOS FUNCIONAN PARA ABRIR LAS PANTALLAS, ENVIAR O RECIBIR LOS DATOS
#METODO GET. TRAE TODOS LOS USUARIOS PARA LA LISTA DE VISUALIZAR
def listar_usuarios(request):
    rsp_usuario = requests.get(url+'usuarios/') 
    if rsp_usuario.status_code == 200:
        data = rsp_usuario.json()
        usuarios = data['usuariosr']
    else:
        usuarios = []
    context = {'usuariosr': usuarios}
    return render(request, 'usuario/listar.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_usuario(request):
    rsp_empleado = requests.get(url+'empleados/')
    if rsp_empleado.status_code == 200:
            data = rsp_empleado.json()
            empleado = data['empleados']
    else:
            empleado = []
    if request.method == 'POST':
        idEmpleado = int(request.POST['idEmpleadl'])
        nombreUsuario = request.POST['user']
        password = request.POST['password']
        passwordc = request.POST['passwordc']
        activo = int(request.POST['activado'])
        bloqueado = int(request.POST['bloqueo'])
        registro_temp = {'idEmpleado':idEmpleado, 'nombreUsuario': nombreUsuario, 'password': password, 'activo': activo, 'bloqueado': bloqueado, 'passwordc':passwordc}
        response = requests.post(url+'usuarios/', json={'idEmpleado':idEmpleado, 'nombreUsuario': nombreUsuario, 'password': password, 'activo': activo, 'bloqueado': bloqueado, 'passwordc':passwordc})
        userdata={}
        if response.status_code == 200:
            userdata = response.json()
            mensaje = userdata['message']
            return render(request, 'usuario/registro.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'empleado': empleado, 'registro_temp': registro_temp})
        else:
            mensaje = userdata['usuariosr']
            return render(request, 'usuario/registro.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'empleado': empleado, 'registro_temp': registro_temp})
    else:
        return render(request, 'usuario/registro.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(), 'empleado': empleado})


#METODO PARA ABRIR LA PANTALLA DE ACTUALIZAR, TOMANDO EL ID DE LA PANTALLA VISUALIZAR Y ASI LLENAR LOS CAMPOS CON ESTA INFORMACION
def abrir_actualizar_usuarios(request):
    rsp_empleado = requests.get(url+'empleados/')
    if rsp_empleado.status_code == 200:
            data = rsp_empleado.json()
            empleado = data['empleados']
    else:
            empleado = []
    if request.method == 'POST':
         rsp_usuario = requests.get(url+'usuarios/busqueda/id/'+str(request.POST['id_usuario']))
         mensaje = data['message']
         if rsp_usuario.status_code == 200:
            data = rsp_usuario.json()
            usuarios = data['usuariosr']
            mensaje = data['message']
         else:
            usuarios = []
         context = {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'empleado':empleado, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'usuario/actualizar.html', context,)

#METODO PARA ACTUALIZAR Y ABRIR LA PANTALLA DE VISUALIZAR
def actualizar_usuario(request, id):
    if request.method == 'POST':
        #Metodo para llenar el SELECT de los Empleados
        rsp_empleado = requests.get(url+'empleados/')
        if rsp_empleado.status_code == 200:
                data = rsp_empleado.json()
                empleado = data['empleados']
        else:
                empleado = []
                # FIN Metodo para llenar el SELECT de los Empleados
        #Obtener los datos para hacer la actualizacion
        idTemporal = id
        idEmpleado = int(request.POST['idEmpleadl'])
        nombreUsuario = request.POST['user']
        password = request.POST['password']
        passwordc = request.POST['passwordc']
        activo = int(request.POST['activado'])
        bloqueado = int(request.POST['bloqueo'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'usuarios/id/{idTemporal}', json={'idEmpleado':idEmpleado, 'nombreUsuario': nombreUsuario, 'password': password, 'activo': activo, 'bloqueado': bloqueado, 'passwordc':passwordc})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el usuario relacionado con el id
        res = requests.get(url+f'usuarios/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        usuario = data['usuariosr']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'usuario/actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'usuariosr':usuario, 'empleado': empleado })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'usuario/actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'usuariosr':usuario,'empleado': empleado, 'contra':password})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'usuarios/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            usuario = data['usuariosr']
            mensaje = data['message']
            return render(request, 'usuario/actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuario})
        else:
            mensaje = data['message']
            return render(request, 'usuario/actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'usuariosr':usuario})
        

def eliminar_usuario(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'usuarios/id/{idTemporal}')
            res = response.json()
            rsp_usuario = requests.get(url + 'usuarios/') 
            if rsp_usuario.status_code == 200:
                data = rsp_usuario.json()
                usuarios = data['usuariosr']
            else:
                usuarios = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje': mensaje}
            return render(request, 'usuario/listar.html', context)     
    except:
        rsp_usuario = requests.get(url + 'usuarios/') 
        if rsp_usuario.status_code == 200:
            data = rsp_usuario.json()
            usuarios = data['usuariosr']
        else:
            usuarios = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'error': mensaje}
        return render(request, 'usuario/listar.html', context)     
    
def buscar_usuarios(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'usuarios/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    usuarios = {}
                    usuarios = data['usuariosr']
                    context = {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje':mensaje}
                    return render(request, 'usuario/listar.html', context) 
                else:
                    usuarios = []
                    mensaje = 'No se encontraron usuarios'
                    return render(request, 'usuario/listar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje': mensaje})
          
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    usuarios = {}
                    usuarios = data['usuariosr']
                    context = {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje':mensaje}
                    return render(request, 'usuario/listar.html', context)
                else:
                    usuarios = []
                    mensaje = 'No se encontraron usuarios'
                    return render(request, 'usuario/listar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje': mensaje})
    

        else:
            response = requests.get(url+'usuarios/')
            if response.status_code == 200:
                data = response.json()
                usuarios = data['usuariosr']
                mensaje = data['message']   
                return render(request, 'usuario/listar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje': mensaje})
            else:
                usuarios = []
                mensaje = 'No se encontraron usuarios'
            return render(request, 'usuario/listar.html', {'reportes_lista':DatosReportes.cargar_lista_usuarios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'usuariosr': usuarios, 'mensaje': mensaje})
    


        









def validar_password(password,encriptado):
    contexto = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__rounds=10
    )
    verify = contexto.verify(password, encriptado)
    return verify