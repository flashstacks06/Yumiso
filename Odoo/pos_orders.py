import xmlrpc.client
import json

def get_draft_pos_orders_with_additional_info(url, db, username, password):
    # Información para la autenticación
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    if uid is None:
        raise Exception("Autenticación fallida.")

    # Conexión al modelo pos.order
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Buscar órdenes en estado 'draft'
    order_ids = models.execute_kw(db, uid, password,
                                  'pos.order', 'search',
                                  [[['state', '=', 'draft']]])

    # Leer datos de las órdenes encontradas, incluyendo el punto de venta, el monto pagado y el cliente
    orders = models.execute_kw(db, uid, password,
                               'pos.order', 'read',
                               [order_ids, ['id', 'name', 'date_order', 'amount_total', 'amount_paid', 'pos_reference', 'config_id', 'partner_id']])

    # Obtener los nombres de los puntos de venta
    pos_config_ids = list({order['config_id'][0] for order in orders if order['config_id']})
    pos_configs = models.execute_kw(db, uid, password,
                                    'pos.config', 'read',
                                    [pos_config_ids, ['id', 'name']])

    pos_name_map = {pos['id']: pos['name'] for pos in pos_configs}

    # Obtener los nombres de los clientes
    partner_ids = list({order['partner_id'][0] for order in orders if order['partner_id']})
    partners = models.execute_kw(db, uid, password,
                                    'res.partner', 'read',
                                    [partner_ids, ['id', 'name']])

    partner_name_map = {partner['id']: partner['name'] for partner in partners}

    # Agregar el nombre del punto de venta, el monto pagado y el nombre del cliente a cada orden
    for order in orders:
        pos_id = order['config_id'][0]
        order['pos_name'] = pos_name_map.get(pos_id, 'Desconocido')
        partner_id = order['partner_id'][0]
        order['partner_name'] = partner_name_map.get(partner_id, 'Desconocido')

    return orders

# Ejemplo de uso
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

try:
    draft_orders = get_draft_pos_orders_with_additional_info(url, db, username, password)
    # Convierte la lista de órdenes en una cadena JSON formateada
    json_output = json.dumps(draft_orders, indent=2)
    print(json_output)
except Exception as e:
    print(f"Error: {e}")
