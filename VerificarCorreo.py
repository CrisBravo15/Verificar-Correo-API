import funciones as func
import time

if __name__ == "__main__":
    args = func.obtener_argumentos()
    correo = args.correo
    if "@" not in correo:
        func.logging.error(f"{correo} no es un correo válido")
        print(f"{correo} no es un correo válido, favor de ingrear uno correcto")
        exit()
    salida = args.output
    api_key = func.leer_apikey()

    try:
        respuesta = func.consultar_brechas(correo, api_key)
    except Exception as e:
        func.logging.error(f"Error de conexión {e}")
        exit()
    
    if respuesta.status_code == 200:
        brechas = respuesta.json()
        func.logging.info(f"{correo} comprometo en {len(brechas)} brechas")
        detalles = []

        for i, brecha in enumerate(brechas[:3]):
            nombre = brecha["Name"]
            detalle_resp = func.consultar_detalle(nombre, api_key)
            if detalle_resp.status_code == 200:
                detalles.append(detalle_resp.json())
            else:
                log=f"No se pudo obtener detalles de {nombre}. Código: {detalle_resp.status_code}"
                func.logging.error(log)
            if i < 2:
                time.sleep(10)
        
        func.generar_csv(salida,detalles)
        print(f"Consulta completada. Revisa el archivo {salida}.")
    elif respuesta.status_code == 404:
        func.logging.info(f"{correo} no aparece en brechas conocidas.")
        print(f"La cuenta {correo} no aparece en ninguna brecha")
    elif respuesta.status_code == 401:
        func.logging.error("API key inválida")
        print("Error de autenticación")
    else:
        func.logging.error(f"Error inesperado. Código: {respuesta.status_code}")
        print(f"Error inesperado. Código: {respuesta.status_code}")