import requests

from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
class DatosReportes():

    def cargar_usuario():
        response = requests.get(url+'usuarios/busqueda/sesion/1')
        if response.status_code == 200:
            data = response.json()
            usuario = data['usuariosr']
            nombre = usuario[0]['nombreUsuario']
        else:
            nombre  = ''
        return nombre
    
    def cargar_lista_autorizacion():
        try:
            response = requests.get(url+'autorizar/')
            if response.status_code == 200:
                data = response.json()
                lista = data['autorizar']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_autorizacion','logs_pdf_autorizacion')
                    logger.debug("No se obtuvieron los registros(autorizacion)")
                else:
                    logger = definir_log_info('pdf_autorizacion','logs_pdf_autorizacion')
                    logger.debug("Se obtuvieron los registros(autorizacion)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_autorizacion','logs_pdf_autorizacion')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista
    
    def cargar_lista_cargos():
        try:
            response = requests.get(url+'cargos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['cargos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('cargos_pdf','logs_pdf_cargo')
                    logger.debug("No se obtuvieron cargos")
                else:
                    logger = definir_log_info('cargos_pdf','logs_pdf_cargo')
                    logger.debug("Se obtuvo la informacion correspondiente a cargos")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('cargos_pdf_excepcion','logs_pdf_cargo')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_citas():
        try:
            response = requests.get(url+'citas/')
            if response.status_code == 200:
                data = response.json()
                lista = data['citas']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_citas','logs_pdf_citas')
                    logger.debug("No se obtuvieron los registros(citas)")
                else:
                    logger = definir_log_info('pdf_citas','logs_pdf_citas')
                    logger.debug("Se obtuvieron los registros(citas)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_citas','logs_pdf_citas')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista
    
    def cargar_lista_pacientes():
        try:
            response = requests.get(url+'pacientes/')
            if response.status_code == 200:
                data = response.json()
                lista = data['pacientes']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_pacientes','logs_pdf_pacientes')
                    logger.debug("No se obtuvieron los registros(pacientes)")
                else:
                    logger = definir_log_info('pdf_pacientes','logs_pdf_pacientes')
                    logger.debug("Se obtuvieron los registros(pacientes)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_pacientes','logs_pdf_pacientes')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista
    
    def cargar_lista_consultas():
        try:
            response = requests.get(url+'consultas/')
            if response.status_code == 200:
                data = response.json()
                lista = data['consultas']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_consultas','logs_pdf_consultas')
                    logger.debug("No se obtuvieron los registros(consultas)")
                else:
                    logger = definir_log_info('pdf_consultas','logs_pdf_consultas')
                    logger.debug("Se obtuvieron los registros(consultas)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_consultas','logs_pdf_consultas')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_sar():
        try:
            response = requests.get(url+'correlativo/')
            if response.status_code == 200:
                data = response.json()
                lista = data['correlativo']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_correlativo_sar','logs_pdf_correlativo_sar')
                    logger.debug("No se obtuvieron los registros(correlativo_sar)")
                else:
                    logger = definir_log_info('pdf_correlativo_sar','logs_pdf_correlativo_sar')
                    logger.debug("Se obtuvieron los registros(correlativo_sar)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_correlativo_sar','logs_pdf_correlativo_sar')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    def cargar_lista_costo_historico_medicamento():
        try:
            response = requests.get(url+'costoHistoricoMedicamento/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_costo_historico_medicamento','logs_pdf_costo_historico_medicamento')
                    logger.debug("No se obtuvieron los registros(costo_historico_medicamento)")
                else:
                    logger = definir_log_info('pdf_costo_historico_medicamento','logs_pdf_costo_historico_medicamento')
                    logger.debug("Se obtuvieron los registros(costo_historico_medicamento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_costo_historico_medicamento','logs_pdf_costo_historico_medicamento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_descuentos():
        try:
            response = requests.get(url+'Descuentos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['Descuentos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_descuentos','logs_pdf_descuentos')
                    logger.debug("No se obtuvieron los registros(descuentos)")
                else:
                    logger = definir_log_info('pdf_descuentos','logs_pdf_descuentos')
                    logger.debug("Se obtuvieron los registros(descuentos)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_descuentos','logs_pdf_descuentos')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_detalle_consulta():
        try:
            response = requests.get(url+'consultaDetalle/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_consulta','logs_pdf_detalle_consulta')
                    logger.debug("No se obtuvieron los registros(detalle_consulta)")
                else:
                    logger = definir_log_info('pdf_detalle_consulta','logs_pdf_detalle_consulta')
                    logger.debug("Se obtuvieron los registros(detalle_consulta)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_consulta','logs_pdf_detalle_consulta')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    def cargar_lista_diagnostico():
        try:
            response = requests.get(url+'diagnostico/')
            if response.status_code == 200:
                data = response.json()
                lista = data['diagnosticos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_diagnostico','logs_pdf_diagnostico')
                    logger.debug("No se obtuvieron los registros(diagnostico)")
                else:
                    logger = definir_log_info('pdf_diagnostico','logs_pdf_diagnostico')
                    logger.debug("Se obtuvieron los registros(diagnostico)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_diagnostico','logs_pdf_diagnostico')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_detalle_diagnostico():
        try:
            response = requests.get(url+'diagnosticoDetalle/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_diagnostico','logs_pdf_detalle_diagnostico')
                    logger.debug("No se obtuvieron los registros(detalle_diagnostico)")
                else:
                    logger = definir_log_info('pdf_detalle_diagnostico','logs_pdf_detalle_diagnostico')
                    logger.debug("Se obtuvieron los registros(detalle_diagnostico)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_diagnostico','logs_pdf_detalle_diagnostico')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_documentos():
        try:
            response = requests.get(url+'documentos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['documentos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_documentos','logs_pdf_documentos')
                    logger.debug("No se obtuvieron los registros(documentos)")
                else:
                    logger = definir_log_info('pdf_documentos','logs_pdf_documentos')
                    logger.debug("Se obtuvieron los registros(documentos)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_documentos','logs_pdf_documentos')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_empleados():
        try:
            response = requests.get(url+'empleados/')
            if response.status_code == 200:
                data = response.json()
                lista = data['empleados']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_empleados','logs_pdf_empleados')
                    logger.debug("No se obtuvieron los registros(empleados)")
                else:
                    logger = definir_log_info('pdf_empleados','logs_pdf_empleados')
                    logger.debug("Se obtuvieron los registros(empleados)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_empleados','logs_pdf_empleados')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

        
    def cargar_lista_enfermedades():
        try:
            response = requests.get(url+'enfermedades/')
            if response.status_code == 200:
                data = response.json()
                lista = data['enfermedades']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_enfermedades','logs_pdf_enfermedades')
                    logger.debug("No se obtuvieron los registros(enfermedades)")
                else:
                    logger = definir_log_info('pdf_enfermedades','logs_pdf_enfermedades')
                    logger.debug("Se obtuvieron los registros(enfermedades)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_enfermedades','logs_pdf_enfermedades')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_detalle_enfermedad():
        try:
            response = requests.get(url+'enfermedadDetalle/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_enfermedad','logs_pdf_detalle_enfermedad')
                    logger.debug("No se obtuvieron los registros(detalle_enfermedad)")
                else:
                    logger = definir_log_info('pdf_detalle_enfermedad','logs_pdf_detalle_enfermedad')
                    logger.debug("Se obtuvieron los registros(detalle_enfermedad)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_enfermedad','logs_pdf_detalle_enfermedad')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_especialidades():
        response = requests.get(url+'especialidad/')
        if response.status_code == 200:
            data = response.json()
            lista = data['especialidad']
        else:
            lista  = []
        return lista
    
    def cargar_lista_examen():
        try:
            response = requests.get(url+'examen/')
            if response.status_code == 200:
                data = response.json()
                lista = data['examenes']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_examen','logs_pdf_examen')
                    logger.debug("No se obtuvieron los registros(examen)")
                else:
                    logger = definir_log_info('pdf_examen','logs_pdf_examen')
                    logger.debug("Se obtuvieron los registros(examen)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_examen','logs_pdf_examen')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_expediente():
        try:
            response = requests.get(url+'expediente/')
            if response.status_code == 200:
                data = response.json()
                lista = data['expedientes']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_expediente','logs_pdf_expediente')
                    logger.debug("No se obtuvieron los registros(expediente)")
                else:
                    logger = definir_log_info('pdf_expediente','logs_pdf_expediente')
                    logger.debug("Se obtuvieron los registros(expediente)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_expediente','logs_pdf_expediente')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_historico_impuesto():
        try:
            response = requests.get(url+'impuestoHistorico/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_hisotrico_impuesto','logs_pdf_hisotrico_impuesto')
                    logger.debug("No se obtuvieron los registros(hisotrico_impuesto)")
                else:
                    logger = definir_log_info('pdf_hisotrico_impuesto','logs_pdf_hisotrico_impuesto')
                    logger.debug("Se obtuvieron los registros(hisotrico_impuesto)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_hisotrico_impuesto','logs_pdf_hisotrico_impuesto')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    def cargar_lista_impuesto():
        try:
            response = requests.get(url+'Impuestos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['Impuestos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_impuesto','logs_pdf_impuesto')
                    logger.debug("No se obtuvieron los registros(impuesto)")
                else:
                    logger = definir_log_info('pdf_impuesto','logs_pdf_impuesto')
                    logger.debug("Se obtuvieron los registros(impuesto)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_impuesto','logs_pdf_impuesto')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_laboratorios():
        try:
            response = requests.get(url+'laboratorios/')
            if response.status_code == 200:
                data = response.json()
                lista = data['laboratorios']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_laboratorios','logs_pdf_laboratorios')
                    logger.debug("No se obtuvieron los registros(laboratorios)")
                else:
                    logger = definir_log_info('pdf_laboratorios','logs_pdf_laboratorios')
                    logger.debug("Se obtuvieron los registros(laboratorios)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_laboratorios','logs_pdf_laboratorios')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_medicamentos():
        try:
            response = requests.get(url+'medicamentos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['medicamentos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_medicamentos','logs_pdf_medicamentos')
                    logger.debug("No se obtuvieron los registros(medicamentos)")
                else:
                    logger = definir_log_info('pdf_medicamentos','logs_pdf_medicamentos')
                    logger.debug("Se obtuvieron los registros(medicamentos)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_medicamentos','logs_pdf_medicamentos')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_metodo_pago():
        try:
            response = requests.get(url+'metodop/')
            if response.status_code == 200:
                data = response.json()
                lista = data['metodop']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_metodo_pago','logs_pdf_metodo_pago')
                    logger.debug("No se obtuvieron los registros(metodo_pago)")
                else:
                    logger = definir_log_info('pdf_metodo_pago','logs_pdf_metodo_pago')
                    logger.debug("Se obtuvieron los registros(metodo_pago)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_metodo_pago','logs_pdf_metodo_pago')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_muestras():
        try:
            response = requests.get(url+'muestras/')
            if response.status_code == 200:
                data = response.json()
                lista = data['muestras']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_muestras','logs_pdf_muestras')
                    logger.debug("No se obtuvieron los registros(muestras)")
                else:
                    logger = definir_log_info('pdf_muestras','logs_pdf_muestras')
                    logger.debug("Se obtuvieron los registros(muestras)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_muestras','logs_pdf_muestras')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_parametros_generales():
        try:
            response = requests.get(url+'parametrosgenerales/')
            if response.status_code == 200:
                data = response.json()
                lista = data['parametrosgenerales']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_parametros_generales','logs_pdf_parametros_generales')
                    logger.debug("No se obtuvieron los registros(parametros_generales)")
                else:
                    logger = definir_log_info('pdf_parametros_generales','logs_pdf_parametros_generales')
                    logger.debug("Se obtuvieron los registros(parametros_generales)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_parametros_generales','logs_pdf_parametros_generales')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_historico_precio_examen():
        try:
            response = requests.get(url+'precioHistoricoExamen/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_precio_historico_examen','logs_pdf_precio_historico_examen')
                    logger.debug("No se obtuvieron los registros(precio_historico_examen)")
                else:
                    logger = definir_log_info('pdf_precio_historico_examen','logs_pdf_precio_historico_examen')
                    logger.debug("Se obtuvieron los registros(precio_historico_examen)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_precio_historico_examen','logs_pdf_precio_historico_examen')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    
    def cargar_lista_historico_precio_tratamiento():
        try:
            response = requests.get(url+'precioHistoricoTratamiento/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_precio_historico_tratamiento','logs_pdf_precio_historico_tratamiento')
                    logger.debug("No se obtuvieron los registros(precio_historico_tratamiento)")
                else:
                    logger = definir_log_info('pdf_precio_historico_tratamiento','logs_pdf_precio_historico_tratamiento')
                    logger.debug("Se obtuvieron los registros(precio_historico_tratamiento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_precio_historico_tratamiento','logs_pdf_precio_historico_tratamiento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_historico_precio_consulta():
        try:
            response = requests.get(url+'precioHistoricoConsulta/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_precio_historico_consulta','logs_pdf_precio_historico_consulta')
                    logger.debug("No se obtuvieron los registros(precio_historico_consulta)")
                else:
                    logger = definir_log_info('pdf_precio_historico_consulta','logs_pdf_precio_historico_consulta')
                    logger.debug("Se obtuvieron los registros(precio_historico_consulta)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_precio_historico_consulta','logs_pdf_precio_historico_consulta')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_precio_historico_medicamento():
        try:
            response = requests.get(url+'precioHistoricoMedicamento/')
            if response.status_code == 200:
                data = response.json()
                lista = data['historicos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_precio_historico_medicamento','logs_pdf_precio_historico_medicamento')
                    logger.debug("No se obtuvieron los registros(precio_historico_medicamento)")
                else:
                    logger = definir_log_info('pdf_precio_historico_medicamento','logs_pdf_precio_historico_medicamento')
                    logger.debug("Se obtuvieron los registros(precio_historico_medicamento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_precio_historico_medicamento','logs_pdf_precio_historico_medicamento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    
    def cargar_lista_detalle_recaudo_examen():
        try:
            response = requests.get(url+'recaudoDetalleExamen/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_recaudo_examen','logs_pdf_detalle_recaudo_examen')
                    logger.debug("No se obtuvieron los registros(detalle_recaudo_examen)")
                else:
                    logger = definir_log_info('pdf_detalle_recaudo_examen','logs_pdf_detalle_recaudo_examen')
                    logger.debug("Se obtuvieron los registros(detalle_recaudo_examen)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_recaudo_examen','logs_pdf_detalle_recaudo_examen')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_detalle_recaudo_medicamento():
        try:
            response = requests.get(url+'recaudoDetalleMedicamento/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_recaudo_medicamento','logs_pdf_detalle_recaudo_medicamento')
                    logger.debug("No se obtuvieron los registros(detalle_recaudo_medicamento)")
                else:
                    logger = definir_log_info('pdf_detalle_recaudo_medicamento','logs_pdf_detalle_recaudo_medicamento')
                    logger.debug("Se obtuvieron los registros(detalle_recaudo_medicamento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_recaudo_medicamento','logs_pdf_detalle_recaudo_medicamento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    
    def cargar_lista_detalle_recaudo_tratamiento():
        try:
            response = requests.get(url+'recaudoDetalleTratamiento/')
            if response.status_code == 200:
                data = response.json()
                lista = data['detalles']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_detalle_recaudo_tratamiento','logs_pdf_detalle_recaudo_tratamiento')
                    logger.debug("No se obtuvieron los registros(detalle_recaudo_tratamiento)")
                else:
                    logger = definir_log_info('pdf_detalle_recaudo_tratamiento','logs_pdf_detalle_recaudo_tratamiento')
                    logger.debug("Se obtuvieron los registros(detalle_recaudo_tratamiento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_detalle_recaudo_tratamiento','logs_pdf_detalle_recaudo_tratamiento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_proveedores():
        try:
            response = requests.get(url+'proveedores/')
            if response.status_code == 200:
                data = response.json()
                lista = data['proveedores']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_proveedores','logs_pdf_proveedores')
                    logger.debug("No se obtuvieron los registros(proveedores)")
                else:
                    logger = definir_log_info('pdf_proveedores','logs_pdf_proveedores')
                    logger.debug("Se obtuvieron los registros(proveedores)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_proveedores','logs_pdf_proveedores')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_recaudo():
        try:
            response = requests.get(url+'recaudo/')
            if response.status_code == 200:
                data = response.json()
                lista = data['recaudo']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_recaudo','logs_pdf_recaudo')
                    logger.debug("No se obtuvieron los registros(recaudo)")
                else:
                    logger = definir_log_info('pdf_recaudo','logs_pdf_recaudo')
                    logger.debug("Se obtuvieron los registros(recaudo)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_recaudo','logs_pdf_recaudo')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_resultado():
        try:
            response = requests.get(url+'resultados/')
            if response.status_code == 200:
                data = response.json()
                lista = data['resultados']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_resultados','logs_pdf_resultados')
                    logger.debug("No se obtuvieron los registros(resultados)")
                else:
                    logger = definir_log_info('pdf_resultados','logs_pdf_resultados')
                    logger.debug("Se obtuvieron los registros(resultados)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_resultados','logs_pdf_resultados')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_sintoma():
        try:
            response = requests.get(url+'sintomas/')
            if response.status_code == 200:
                data = response.json()
                lista = data['sintomas']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_sintomas','logs_pdf_sintomas')
                    logger.debug("No se obtuvieron los registros(sintomas)")
                else:
                    logger = definir_log_info('pdf_sintomas','logs_pdf_sintomas')
                    logger.debug("Se obtuvieron los registros(sintomas)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_sintomas','logs_pdf_sintomas')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_subtipo():
        try:
            response = requests.get(url+'subtipo/')
            if response.status_code == 200:
                data = response.json()
                lista = data['subtipo']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_subtipo','logs_pdf_subtipo')
                    logger.debug("No se obtuvieron los registros(subtipo)")
                else:
                    logger = definir_log_info('pdf_subtipo','logs_pdf_subtipo')
                    logger.debug("Se obtuvieron los registros(subtipo)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_subtipo','logs_pdf_subtipo')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_tipo():
        try:
            response = requests.get(url+'tipo/')
            if response.status_code == 200:
                data = response.json()
                lista = data['tipos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_tipos','logs_pdf_tipos')
                    logger.debug("No se obtuvieron los registros(tipos)")
                else:
                    logger = definir_log_info('pdf_tipos','logs_pdf_tipos')
                    logger.debug("Se obtuvieron los registros(tipos)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_tipos','logs_pdf_tipos')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_tipo_muestra():
        try:
            response = requests.get(url+'tmuestra/')
            if response.status_code == 200:
                data = response.json()
                lista = data['tmuestra']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_tipo_muestra','logs_pdf_tipo_muestra')
                    logger.debug("No se obtuvieron los registros(tipo_muestra)")
                else:
                    logger = definir_log_info('pdf_tipo_muestra','logs_pdf_tipo_muestra')
                    logger.debug("Se obtuvieron los registros(tipo_muestra)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_tipo_muestra','logs_pdf_tipo_muestra')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    
    def cargar_lista_traslados():
        try:
            response = requests.get(url+'traslados/')
            if response.status_code == 200:
                data = response.json()
                lista = data['traslados']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_traslados','logs_pdf_traslados')
                    logger.debug("No se obtuvieron los registros(traslados)")
                else:
                    logger = definir_log_info('pdf_traslados','logs_pdf_traslados')
                    logger.debug("Se obtuvieron los registros(traslados)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_traslados','logs_pdf_traslados')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_tratamiento():
        try:
            response = requests.get(url+'tratamientos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['tratamientos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_tratamiento','logs_pdf_tratamiento')
                    logger.debug("No se obtuvieron los registros(tratamiento)")
                else:
                    logger = definir_log_info('pdf_tratamiento','logs_pdf_tratamiento')
                    logger.debug("Se obtuvieron los registros(tratamiento)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_tratamiento','logs_pdf_tratamiento')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_usuarios():
        try:
            response = requests.get(url+'usuarios/')
            if response.status_code == 200:
                data = response.json()
                lista = data['usuariosr']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_usuarios','logs_pdf_usuarios')
                    logger.debug("No se obtuvieron los registros(usuarios)")
                else:
                    logger = definir_log_info('pdf_usuarios','logs_pdf_usuarios')
                    logger.debug("Se obtuvieron los registros(usuarios)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_usuarios','logs_pdf_usuarios')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista


    def cargar_lista_permisos():
        try:
            response = requests.get(url+'permisos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['permisos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_permisos','logs_pdf_permisos')
                    logger.debug("No se obtuvieron los registros(permisos)")
                else:
                    logger = definir_log_info('pdf_permisos','logs_pdf_permisos')
                    logger.debug("Se obtuvieron los registros(permisos)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_permisos','logs_pdf_permisos')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista



    def cargar_lista_acciones():
        try:
            response = requests.get(url+'acciones/')
            if response.status_code == 200:
                data = response.json()
                lista = data['acciones']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_acciones','logs_pdf_acciones')
                    logger.debug("No se obtuvieron los registros(acciones)")
                else:
                    logger = definir_log_info('pdf_acciones','logs_pdf_acciones')
                    logger.debug("Se obtuvieron los registros(acciones)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_acciones','logs_pdf_acciones')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista
        

    def cargar_lista_pantallas():
        try:
            response = requests.get(url+'pantallas/')
            if response.status_code == 200:
                data = response.json()
                lista = data['pantallas']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('pdf_pantallas','logs_pdf_pantallas')
                    logger.debug("No se obtuvieron los registros(pantallas)")
                else:
                    logger = definir_log_info('pdf_pantallas','logs_pdf_pantallas')
                    logger.debug("Se obtuvieron los registros(pantallas)")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('pdf_acciones','logs_pdf_acciones')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

