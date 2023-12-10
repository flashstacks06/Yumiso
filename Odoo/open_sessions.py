import xmlrpc.client

url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def obtener_sesiones_abiertas():
    modelo_sesion = 'pos.session'
    
    try:
        # Consultar sesiones abiertas con información sobre el punto de venta
        sesiones_abiertas = models.execute_kw(db, uid, password, modelo_sesion, 'search_read',
                                              [[['state', '=', 'opened']]], {'fields': ['id', 'name', 'config_id']})

        # Imprimir la lista de sesiones abiertas con información sobre el punto de venta
        print("Sesiones abiertas:")
        for sesion in sesiones_abiertas:
            print("ID: {}, Nombre: {}, Punto de venta: {}".format(sesion['id'], sesion['name'], sesion['config_id'][1]))

        return sesiones_abiertas

    except xmlrpc.client.Fault as error:
        print("Error al obtener sesiones abiertas:", error.faultCode, "-", error.faultString)

    except Exception as e:
        print("Error general:", e)

# Llamar a la función para obtener sesiones abiertas
sesiones_abiertas = obtener_sesiones_abiertas()

# Si hay sesiones abiertas, puedes seleccionar una para cerrar (reemplaza 0 con el índice de la sesión que deseas cerrar)
if sesiones_abiertas:
    indice_sesion_a_cerrar = 0
    id_sesion_a_cerrar = sesiones_abiertas[indice_sesion_a_cerrar]['id']
    print("ID de la sesión seleccionada para cerrar:", id_sesion_a_cerrar)
else:
    print("No hay sesiones abiertas.")
