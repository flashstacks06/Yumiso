import xmlrpc.client

# Configuración de la conexión
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Función para obtener el valor de cierre y la diferencia de una sesión de punto de venta
def obtener_info_cierre(nombre_punto_venta, numero_pos):
    try:
        # Buscar el punto de venta por nombre para obtener su ID
        pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'search', [[['name', '=', nombre_punto_venta]]])
        if not pos_config_id:
            print("No se encontró el punto de venta con ese nombre.")
            return

        # Construir el nombre de la sesión completo con el formato adecuado
        pos_session_name = f"POS/{str(numero_pos).zfill(5)}"  # Ejemplo: "POS/00051"

        # Obtener la información de la sesión utilizando el nombre de la sesión
        session_info = models.execute_kw(db, uid, password, 'pos.session', 'search_read', 
                                         [[['config_id', '=', pos_config_id[0]], ['name', '=', pos_session_name]]],
                                        )
        if not session_info:
            print("No se encontró una sesión con ese número de POS para el punto de venta proporcionado.")
            return

        # Imprimir la información del cierre
        for session in session_info:
            print(f"POS Number: {session['name']}")
            print(f"Closing Amount: ${session['cash_register_balance_end_real']}")
            print(f"Closing Difference: ${session['cash_real_difference']}")

    except xmlrpc.client.Fault as error:
        print(f"Error al obtener la información de cierre: {error.faultCode} - {error.faultString}")

    except Exception as e:
        print(f"Error general: {e}")

# Ejecutar el script
if __name__ == '__main__':
    nombre_punto_venta = input("Ingresa el nombre del punto de venta: ")
    numero_pos = input("Ingresa el número de POS: ")
    obtener_info_cierre(nombre_punto_venta, numero_pos)
