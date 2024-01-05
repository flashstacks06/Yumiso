import xmlrpc.client
from datetime import datetime

# Datos del servidor Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Establecer conexión con Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

def obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta):
    domain = [('name', '=', nombre_punto_de_venta)]
    pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [domain])
    if pos_config_ids:
        return pos_config_ids[0]
    else:
        raise Exception(f'No se encontró un punto de venta con el nombre: {nombre_punto_de_venta}')

def buscar_cliente_por_correo(correo_cliente):
    domain = [('email', '=', correo_cliente)]
    cliente = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], {'fields': ['id']})
    if cliente:
        return cliente[0]['id']
    else:
        raise Exception(f'No se encontró un cliente con el correo: {correo_cliente}')

def obtener_id_sesion_abierta_o_abrir(id_punto_de_venta, user_id):
    domain = [('config_id', '=', id_punto_de_venta), ('state', '=', 'opened')]
    session_ids = models.execute_kw(db, uid, password, 'pos.session', 'search', [domain])
    if session_ids:
        return session_ids[0]
    else:
        # Si no se encuentra la sesión abierta, simplemente tomamos el primer ID de sesión existente
        domain = [('config_id', '=', id_punto_de_venta)]
        session_ids = models.execute_kw(db, uid, password, 'pos.session', 'search', [domain])
        if session_ids:
            return session_ids[0]
        else:
            # Si aún no hay sesión, intentamos abrir una nueva
            return abrir_sesion_pos(id_punto_de_venta, user_id)

def abrir_sesion_pos(id_punto_de_venta, user_id):
    session_data = {
        'config_id': id_punto_de_venta,
        'user_id': user_id,
    }
    session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [session_data])
    return session_id

def crear_orden_pos(nombre_punto_de_venta, cliente_id, productos_a_agregar):
    id_punto_de_venta = obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta)
    session_id = obtener_id_sesion_abierta_o_abrir(id_punto_de_venta, uid)

    current_week_number = datetime.now().isocalendar()[1]
    order_name = f"{nombre_punto_de_venta}/{current_week_number}"

    pos_order_data = {
        'partner_id': cliente_id,
        'session_id': session_id,
        'name': order_name,
        'lines': [],
        'amount_tax': 0.0,
        'amount_total': 0.0,
        'amount_paid': 0.0,
        'amount_return': 0.0,
    }

    for producto_id, cantidad in productos_a_agregar.items():
        product_info = models.execute_kw(db, uid, password, 'product.product', 'read', [producto_id], {'fields': ['id', 'display_name', 'lst_price', 'taxes_id']})
        if product_info:
            product = product_info[0]
            price_unit = product['lst_price']
            price_subtotal = price_unit * cantidad
            line_data = {
                'product_id': product['id'],
                'qty': cantidad,
                'price_unit': price_unit,
                'price_subtotal': price_subtotal,
                'price_subtotal_incl': price_subtotal,
                'tax_ids': [(6, 0, product['taxes_id'])],
            }
            pos_order_data['lines'].append((0, 0, line_data))
            pos_order_data['amount_total'] += price_subtotal

    order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [pos_order_data])
    return order_id

# Ejemplo de uso
try:
    nombre_punto_de_venta = "Maquina 71"
    cliente_id = buscar_cliente_por_correo("arcade@yumiso.com")
    productos_a_agregar = {14: 2}  # Reemplazar con los IDs de producto reales y cantidades
    orden_pos_id = crear_orden_pos(nombre_punto_de_venta, cliente_id, productos_a_agregar)
    print(f'Orden de punto de venta creada con ID: {orden_pos_id}')
except Exception as e:
    print(f"Error: {e}")
