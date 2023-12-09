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
modelo_orden = 'pos.order'

def obtener_ordenes_pendientes_pago():
    try:
        # Buscar órdenes en estado de borrador (pendientes de pago)
        ordenes_pendientes = models.execute_kw(db, uid, password, modelo_orden, 'search',
                                               [[['state', '=', 'draft']]])

        # Imprimir los IDs de las órdenes pendientes
        print("IDs de órdenes pendientes de pago:")
        for orden_id in ordenes_pendientes:
            print(orden_id)

        return ordenes_pendientes

    except xmlrpc.client.Fault as error:
        print(f"Error al obtener órdenes pendientes de pago: {error.faultCode} - {error.faultString}")

    except Exception as e:
        print(f"Error general al obtener órdenes pendientes de pago: {e}")

# Llamar a la función para obtener órdenes pendientes de pago
ordenes_pendientes_ids = obtener_ordenes_pendientes_pago()
