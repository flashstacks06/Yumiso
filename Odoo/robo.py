import xmlrpc.client
import json
import sys
from datetime import datetime
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Configuración
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'


input_json_str = sys.argv[1]
input_json = json.loads(input_json_str)

# Iniciar sesión en la fuente XML-RPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Variables del JSON de entrada
data_dict = input_json["data"]
maquina = input_json["qrid"]
n_maquina = f"Maquina {maquina}"

# Analizar el stock
products_from_xmlrpc = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['available_in_pos', '=', True],
      ['name', 'not in', ['Juegos', 'Premios']]]], {'fields': ['name', 'id']})

warehouses_from_xmlrpc = models.execute_kw(db, uid, password,
    'stock.warehouse', 'search_read',
    [[['name', '=', n_maquina]]], {'fields': ['id', 'name', 'lot_stock_id']})

location_to_warehouse_from_xmlrpc = {wh['lot_stock_id'][0]: (wh['id'], wh['name']) for wh in warehouses_from_xmlrpc}

product_info_from_xmlrpc = {}
for product in products_from_xmlrpc:
    product_id = product['id']
    qty_by_location = models.execute_kw(db, uid, password,
        'stock.quant', 'search_read',
        [[['product_id', '=', product_id], ['location_id', 'in', list(location_to_warehouse_from_xmlrpc.keys())]]],
        {'fields': ['location_id', 'quantity']})
    product_quantities = {location_id: int(next((qty['quantity'] for qty in qty_by_location if qty['location_id'][0] == location_id), 0)) for location_id in location_to_warehouse_from_xmlrpc}
    product_info_from_xmlrpc[product_id] = product_quantities

stock_elements_from_json = [{parts[0]: int(parts[1])} for item in data_dict["Stock"] for parts in [item.split(":")] if len(parts) == 2]
differences = [{key: value - sum(product_info_from_xmlrpc[int(key)].values())} for item in stock_elements_from_json for key, value in item.items()]
print(product_info_from_xmlrpc)
print(differences)


total_stock_json = sum(int(item.split(":")[1]) for item in data_dict["Stock"])
print(total_stock_json)
# Sumar todas las cantidades en la bodega para todos los productos
total_warehouse_stock = sum(sum(quantities.values()) for quantities in product_info_from_xmlrpc.values())
print(total_warehouse_stock)
# Calcular la diferencia entre el stock total del JSON y el stock total en la bodega


def obtener_cantidad_premios(numero_maquina):
    maquina = f"Maquina {numero_maquina}"

    # Buscar el punto de venta con el número de máquina
    punto_venta_id = models.execute_kw(db, uid, password,
        'pos.config', 'search',
        [[['name', '=', maquina]]],
        {'limit': 1})

    # Asegúrate de que encontraste un punto de venta
    if punto_venta_id:
        # Buscar la orden más nueva que tenga solo los dos productos "Juego" y "Premios"
        order_ids = models.execute_kw(db, uid, password,
            'pos.order', 'search',
            [[['session_id.config_id', '=', punto_venta_id[0]],
              ['lines.product_id.name', 'in', ['Juegos', 'Premios']],
              ['state', '=', 'done']]],  # Asegúrate de que la orden está finalizada
            {'limit': 1, 'order': 'date_order desc'})  # Orden más reciente

        # Asegúrate de que encontraste una orden
        if order_ids:
            # Leer los datos de la orden
            order_data = models.execute_kw(db, uid, password,
                'pos.order', 'read',
                [order_ids],
                {'fields': ['lines']})

            # Ahora busca la cantidad del producto "Premios"
            for line in order_data[0]['lines']:
                line_data = models.execute_kw(db, uid, password,
                    'pos.order.line', 'read',
                    [line],
                    {'fields': ['product_id', 'qty']})

                if line_data[0]['product_id'][1] == 'Premios':
                    cantidad_premios = line_data[0]['qty']
                    print(cantidad_premios)
                    return cantidad_premios  # Devuelve la cantidad encontrada

# Funciones de desencriptación y quitar relleno
def decrypt_aes(encrypted_data, base64_key, base64_iv):
    key = base64.urlsafe_b64decode(base64_key)
    iv = base64.urlsafe_b64decode(base64_iv)
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
    return plaintext

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data

# Función para iniciar una sesión POS
def iniciar_sesion_pos():
    pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'search', [[('name', '=', n_maquina)]])
    if not pos_config_id:
        raise Exception(f"No se encontró la configuración para el punto de venta: {n_maquina}")

    session_data = {'config_id': pos_config_id[0], 'user_id': uid}
    session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [session_data])
    return session_id

# Función para crear ordenes usando las diferencias
def crear_orden_con_diferencias(differences, session_id):
    productos_a_agregar = {int(key): abs(val) for d in differences for key, val in d.items()}
    decrypted_data = unpad(decrypt_aes(input_json["Correo"], 'O1GqAK5igRS-BTYgSVLBvg==', 'v0kiTpvIvAN1IoFQNyB1IQ==')).decode('utf-8').strip()
    cliente = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[('email', '=', decrypted_data)]], {'fields': ['id']})
    cliente_id = cliente[0]['id'] if cliente else None
    if not cliente_id:
        raise Exception(f'No se encontró un cliente con el correo: {decrypted_data}')

    current_week_number = datetime.now().isocalendar()[1]
    order_name = f"Robo Maquina{maquina}/{current_week_number}"

    pos_order_data = {
        'partner_id': cliente_id,
        'session_id': session_id,
        'name': order_name,
        'amount_tax': 0.0,
        'amount_total': 0.0,
        'amount_paid': 0.0,
        'amount_return': 0.0,
        'lines': [],
    }

    for producto_id, cantidad in productos_a_agregar.items():
        product_info = models.execute_kw(db, uid, password, 'product.template', 'read', [producto_id], {'fields': ['id', 'name', 'list_price']})
        if product_info:
            subtotal = product_info[0]['list_price'] * cantidad
            pos_order_data['lines'].append((0, 0, {
                'product_id': product_info[0]['id'],
                'qty': cantidad,
                'price_unit': product_info[0]['list_price'],
                'price_subtotal': subtotal,
                'price_subtotal_incl': subtotal,
                'full_product_name': product_info[0]['name'],
            }))

    pos_order_data['amount_total'] = sum(line[2]['price_subtotal'] for line in pos_order_data['lines'])

    order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [pos_order_data])
    print(f"Orden creada con ID: {order_id}")
# Iniciar sesión POS antes de crear la orden

cantidad_premios = obtener_cantidad_premios(maquina)

diferencia_stock = total_warehouse_stock - cantidad_premios - total_stock_json
print(diferencia_stock)


if diferencia_stock != 0:
    # Crear orden con las diferencias
    # Aquí debes reemplazar 'session_id' con la sesión de POS que necesites utilizar.
    session_id = iniciar_sesion_pos()  # Asumiendo que esta función ya está definida y funciona correctamente
    crear_orden_con_diferencias(diferencia_stock, session_id)  # Asumiendo que esta función ya está definida y adapta el parámetro 'diferencia_stock' correctamente
