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
modelo_pago = 'pos.make.payment'

def obtener_ordenes_pendientes_pago():
    try:
        # Obtener todas las órdenes pendientes de pago
        ordenes_pendientes = models.execute_kw(db, uid, password, modelo_orden, 'search_read',
                                               [[['state', '=', 'draft']]])

        return ordenes_pendientes

    except xmlrpc.client.Fault as error:
        print(f"Error al obtener las órdenes pendientes de pago: {error.faultCode} - {error.faultString}")
        return None

def realizar_pago(id_orden, monto_pago):
    try:
        # Reemplazar 'nombre_del_campo' con el campo correcto para asociar el pago con la orden
        pago_id = models.execute_kw(db, uid, password, modelo_pago, 'create', [{'amount': monto_pago, 'nombre_del_campo': id_orden}])

        # Imprimir información sobre el pago
        print(f"Pago realizado correctamente. ID de la orden: {id_orden}, Monto Pagado: {monto_pago}, ID del Pago: {pago_id}")

    except xmlrpc.client.Fault as error:
        print(f"Error al realizar el pago: {error.faultCode} - {error.faultString}")

    except Exception as e:
        print(f"Error general al realizar el pago: {e}")

# Obtener todas las órdenes pendientes de pago
ordenes_pendientes = obtener_ordenes_pendientes_pago()

if ordenes_pendientes:
    for orden in ordenes_pendientes:
        id_orden_a_pagar = orden['id']
        monto_total_orden = orden['amount_total']

        # Puedes ajustar el monto de pago según tus necesidades
        monto_pago = monto_total_orden

        # Llamar a la función para realizar el pago
        realizar_pago(id_orden_a_pagar, monto_pago)
else:
    print("No hay órdenes pendientes de pago.")
