import xmlrpc.client
from datetime import datetime

# Datos de conexión a Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

def obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta):
    pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [[('name', '=', nombre_punto_de_venta)]])
    return pos_config_ids[0] if pos_config_ids else None

def buscar_o_crear_cliente_por_correo(correo_cliente):
    cliente_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[('email', '=', correo_cliente)]])
    if cliente_ids:
        return cliente_ids[0]
    else:
        return models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': correo_cliente, 'email': correo_cliente}])

def crear_orden_pos(id_punto_de_venta, cliente_id, product_ids):
    pos_session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [{'config_id': id_punto_de_venta, 'start_at': datetime.now()}])
    pos_order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [{
        'session_id': pos_session_id,
        'partner_id': cliente_id,
        'lines': [(0, 0, {'product_id': pid, 'qty': 1}) for pid in product_ids],
    }])
    return pos_order_id

def registrar_pago_efectivo_orden(order_id, amount_total):
    payment_method_ids = models.execute_kw(db, uid, password, 'pos.payment.method', 'search', [[('is_cash_count', '=', True)]])
    payment_id = models.execute_kw(db, uid, password, 'pos.payment', 'create', [{'pos_order_id': order_id, 'amount': amount_total, 'payment_method_id': payment_method_ids[0]}])
    models.execute_kw(db, uid, password, 'pos.order', 'write', [[order_id], {'state': 'paid'}])
    models.execute_kw(db, uid, password, 'pos.order', 'write', [[order_id], {'state': 'done'}])
    return payment_id

# Ejecución principal
if __name__ == "__main__":
    nombre_punto_venta = input("Ingrese el nombre del punto de venta: ")
    id_punto_de_venta = obtener_id_punto_de_venta_por_nombre(nombre_punto_venta)
    
    correo_cliente = input('Ingrese el correo del cliente: ')
    cliente_id = buscar_o_crear_cliente_por_correo(correo_cliente)
    
    input_productos = input('Ingrese los IDs de los productos para la orden separados por comas (ejemplo: 1,2,3): ')
    product_ids = list(map(int, input_productos.split(',')))
    
    orden_pos_id = crear_orden_pos(id_punto_de_venta, cliente_id, product_ids)
    print(f'Orden de punto de venta creada con ID: {orden_pos_id}')
    
    total_amount = sum(models.execute_kw(db, uid, password, 'product.product', 'read', [product_ids], {'fields': ['list_price']}))
    registrar_pago_efectivo_orden(orden_pos_id, total_amount)
    print(f'Pago registrado para la orden {orden_pos_id}.')
