import xmlrpc.client

url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'cbernalestrella@gmail.com'
password = '12345678'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Nombre del modelo
modelo_sesion = 'pos.session'

def cerrar_sesion_punto_venta(id_sesion):
    try:
        # Llamada al método 'action_pos_session_closing_control' en el modelo 'pos.session'
        resultado_cierre = models.execute_kw(db, uid, password, modelo_sesion,
                                             'action_pos_session_closing_control', [id_sesion])

        # Imprimir el resultado (ajusta según tus necesidades)
        print(f"Sesión cerrada correctamente. Resultado: {resultado_cierre}")

    except xmlrpc.client.Fault as error:
        print(f"Error al cerrar la sesión: {error.faultCode} - {error.faultString}")

    except Exception as e:
        print(f"Error general: {e}")

# ID de la sesión que deseas cerrar
id_sesion_a_cerrar = 26

# Llamar a la función para cerrar la sesión
cerrar_sesion_punto_venta(id_sesion_a_cerrar)
