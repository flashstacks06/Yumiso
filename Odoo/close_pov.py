import xmlrpc.client
from datetime import datetime

# Datos de conexión a Odoo
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Función para cerrar la sesión de un punto de venta
def cerrar_sesion_punto_venta(nombre_punto_venta):
    # Obtener ID de la configuración del punto de venta
    pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'search', [[('name', '=', nombre_punto_venta)]])
    if not pos_config_id:
        print(f"No se encontró la configuración para el punto de venta: {nombre_punto_venta}")
        return False

    # Obtener ID de la sesión actual basado en la configuración del punto de venta
    pos_session_id = models.execute_kw(db, uid, password, 'pos.session', 'search', [[('config_id', '=', pos_config_id[0]), ('state', '=', 'opening_control')]])
    if not pos_session_id:
        print(f"No hay una sesión abierta para el punto de venta: {nombre_punto_venta}")
        return False

    # Cerrar la sesión del punto de venta
    try:
        models.execute_kw(db, uid, password, 'pos.session', 'action_pos_session_closing_control', [pos_session_id[0]])
        print(f"La sesión del punto de venta {nombre_punto_venta} ha sido cerrada.")
        return True
    except Exception as e:
        print(f"No se pudo cerrar la sesión del punto de venta {nombre_punto_venta}: {str(e)}")
        return False

# Ejemplo de uso
if __name__ == "__main__":
    nombre_punto_venta = input("Ingrese el nombre del punto de venta para cerrar la sesión: ")
    cerrar_sesion_punto_venta(nombre_punto_venta)