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

# Nombre del modelo
modelo_sesion = 'pos.session'
modelo_config = 'pos.config'

def cerrar_sesion_punto_venta(nombre_punto_venta, monto_contado):
    try:
        # Buscar el punto de venta por nombre para obtener su ID
        pos_config_ids = models.execute_kw(db, uid, password, modelo_config, 'search', [[['name', '=', nombre_punto_venta]]])
        if not pos_config_ids:
            print("No se encontró el punto de venta con ese nombre.")
            return

        # Buscar la sesión del punto de venta por el ID de configuración
        session_ids = models.execute_kw(db, uid, password, modelo_sesion, 'search', [[['config_id', 'in', pos_config_ids], ['state', '!=', 'closed']]])
        if not session_ids:
            print("No se encontró una sesión activa para ese punto de venta.")
            return

        # Actualizar la sesión con el monto contado
        cierra = models.execute_kw(db, uid, password, modelo_sesion, 'write', [session_ids[0], {
            'cash_register_total_entry_encoding': monto_contado,
        }])

        print(cierra)
        # Aceptar las diferencias de pago y cerrar la sesión
        models.execute_kw(db, uid, password, modelo_sesion, 'action_pos_session_closing_control', [session_ids[0]])

        print(f"Sesión del punto de venta '{nombre_punto_venta}' cerrada correctamente con un monto contado de: ${monto_contado}")

    except xmlrpc.client.Fault as error:
        print(f"Error al cerrar la sesión: {error.faultCode} - {error.faultString}")

    except Exception as e:
        print(f"Error general: {e}")

# Ejecutar el script
if __name__ == '__main__':
    # Nombre del punto de venta que deseas cerrar
    nombre_punto_venta = input("Ingresa el nombre del punto de venta que quieres cerrar: ")
    monto_contado = int(input("Ingresa el monto contado en la sesión: "))  # Solicitar el monto contado al usuario
    
    # Llamar a la función para cerrar la sesión con el nombre del punto de venta y el monto contado
    cerrar_sesion_punto_venta(nombre_punto_venta, monto_contado)
