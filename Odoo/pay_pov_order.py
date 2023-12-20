import xmlrpc.client
import datetime

# Configuración de la conexión
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Función para registrar el pago en efectivo de una orden
def registrar_pago_efectivo_orden_nueva(nombre_punto_venta):
    # Encuentra el ID de configuración del punto de venta por su nombre
    pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [[['name', '=', nombre_punto_venta]]])
    if not pos_config_ids:
        print(f"No se encontró configuración para el punto de venta: {nombre_punto_venta}")
        return
    
    pos_config_id = pos_config_ids[0]
    # Encuentra órdenes en estado "draft" para este punto de venta
    orders = models.execute_kw(db, uid, password, 'pos.order', 'search_read', 
                               [[['config_id', '=', pos_config_id], ['state', '=', 'draft']]], 
                               {'fields': ['id', 'amount_total']})
    if not orders:
        print("No hay órdenes en estado 'draft' para procesar.")
        return
    for order in orders:
        order_id = order['id']
        total_amount = order['amount_total']  # Total de la orden

    # Encuentra una sesión abierta para este punto de venta
    session_ids = models.execute_kw(db, uid, password, 'pos.session', 'search', [[['config_id', '=', pos_config_id], ['state', '!=', 'closed']]])
    if not session_ids:
        print(f"No hay sesiones abiertas para el punto de venta: {nombre_punto_venta}")
        return
    # Encuentra una orden en estado "nuevo" en la sesión abierta
    order_ids = models.execute_kw(db, uid, password, 'pos.order', 'search', [[['session_id', 'in', session_ids], ['state', '=', 'draft']]])
    if not order_ids:
        print("No hay órdenes en estado 'nuevo' para procesar.")
        return
    
    # Asumimos que vamos a pagar la primera orden "nueva"
    order_id = order_ids[0]
    # Encuentra el método de pago en efectivo
    payment_method_ids = models.execute_kw(db, uid, password, 'pos.payment.method', 'search', [[['is_cash_count', '=', True]]])
    if not payment_method_ids:
        print("No se encontró método de pago en efectivo.")
        return
    
    payment_method_id = 1

    # Registra el pago
    payment_data = {
        'pos_order_id': order_id,
        'amount': total_amount,
        'payment_method_id': payment_method_id,
    }
    payment_id = models.execute_kw(db, uid, password, 'pos.payment', 'create', [payment_data])
    #payment_id = models.execute_kw(db, uid, password, 'pos.payment', 'create', [payment_data])
    if payment_id:
        updated = models.execute_kw(db, uid, password, 'pos.order', 'write', [[order_id], {'state': 'paid'}])
        done = models.execute_kw(db, uid, password, 'pos.order', 'write', [[order_id], {'state': 'done'}])
        print(f"Registrado pago con ID {payment_id} para la orden {order_id}.")

# Ejecución principal
if __name__ == "__main__":
    nombre_punto_venta = input("Ingrese el nombre del punto de venta: ")
    #monto_pago = float(input("Ingrese el monto del pago en efectivo: "))
    registrar_pago_efectivo_orden_nueva(nombre_punto_venta)
