import xmlrpc.client
from datetime import datetime
import sys
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Verificar si se proporcionan los argumentos necesarios
if len(sys.argv) != 4:
    print("Uso: python create_order_per_pos.py <nombre_punto_venta> <correo_cliente> <productos_y_cantidades>")
    sys.exit(1)

key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='

numero_punto_de_venta = sys.argv[1]
nombre_punto_de_venta = f"Maquina {numero_punto_de_venta}"
correo_cliente_enc = sys.argv[2]
productos_cantidades_str = sys.argv[3]

# Conexión a Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

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

# Funciones de Desencriptación y Quitar Relleno
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

def buscar_cliente_por_correo(correo_cliente):
    domain = [('email', '=', correo_cliente)]
    cliente = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], {'fields': ['id']})

    if cliente:
        return cliente[0]['id']
    else:
        raise Exception(f'No se encontró un cliente con el correo: {correo_cliente}')

def iniciar_sesion_pos(id_punto_de_venta):
    session_data = {
        'config_id': id_punto_de_venta,
        'user_id': uid,
    }

    session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [session_data])
    return session_id

def crear_orden_pos_y_pagar(productos_a_agregar, session_id, cliente_id):
    current_week_number = datetime.now().isocalendar()[1]
    order_name = f"{nombre_punto_de_venta}/{current_week_number}"

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

    pos_order_data['amount_total'] = sum(line[2]['qty'] * line[2]['price_unit'] for line in pos_order_data['lines'])

    order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [pos_order_data])

    payment_method_ids = models.execute_kw(db, uid, password, 'pos.payment.method', 'search', [[['is_cash_count', '=', True]]])

    if payment_method_ids:
        payment_method_id = payment_method_ids[0]

        payment_data = {
            'pos_order_id': order_id,
            'amount': pos_order_data['amount_total'],
            'payment_method_id': payment_method_id,
        }

        payment_id = models.execute_kw(db, uid, password, 'pos.payment', 'create', [payment_data])

        if payment_id:
            updated = models.execute_kw(db, uid, password, 'pos.order', 'write', [[order_id], {'state': 'paid'}])
            print(f"Orden de punto de venta creada y pagada con ID: {order_id}")
        else:
            print("No se pudo registrar el pago.")
    else:
        print("No se encontró método de pago en efectivo.")

    return order_id

def cerrar_sesion_punto_venta(nombre_punto_venta):
    pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'search', [[('name', '=', nombre_punto_de_venta)]])
    if not pos_config_id:
        print(f"No se encontró la configuración para el punto de venta: {nombre_punto_de_venta}")
        return False

    pos_session_id = models.execute_kw(db, uid, password, 'pos.session', 'search', [[('config_id', '=', pos_config_id[0]), ('state', '=', 'opening_control')]])
    if not pos_session_id:
        print(f"No hay una sesión abierta para el punto de venta: {nombre_punto_de_venta}")
        return False

    try:
        models.execute_kw(db, uid, password, 'pos.session', 'action_pos_session_closing_control', [pos_session_id[0]])
        print(f"La sesión del punto de venta {nombre_punto_de_venta} ha sido cerrada.")
        return True
    except Exception as e:
        print(f"No se pudo cerrar la sesión del punto de venta {nombre_punto_de_venta}: {str(e)}")
        return False

try:
    id_punto_de_venta = obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta)
    print(f'El ID del punto de venta "{nombre_punto_de_venta}" es: {id_punto_de_venta}')

    decrypted_data = ""
    try:
        decrypted_data = unpad(decrypt_aes(correo_cliente_enc, key, iv)).decode('utf-8').strip()
    except Exception as e:
        print(f'Error al desencriptar el correo del cliente: {str(e)}')
    
    if decrypted_data:
        print(f'El correo del cliente desencriptado es: {decrypted_data}')

        cliente_id = buscar_cliente_por_correo(decrypted_data)
        print(f'El ID del cliente con correo "{decrypted_data}" es: {cliente_id}')

        sesion_pos_id = iniciar_sesion_pos(id_punto_de_venta)
        print(f'Sesión de punto de venta iniciada con ID: {sesion_pos_id}')

        productos_a_agregar = {}

        try:
            productos_cantidades_str = productos_cantidades_str.strip('[]')  # Eliminar corchetes
            productos_cantidades = productos_cantidades_str.split(',')  # Dividir en elementos

            for pc in productos_cantidades:
                producto_id, cantidad = pc.split(':')
                productos_a_agregar[int(producto_id)] = int(cantidad)

        except Exception as e:
            print(f'Error al procesar los productos y cantidades: {str(e)}')

        if productos_a_agregar:
            orden_pos_id = crear_orden_pos_y_pagar(productos_a_agregar, sesion_pos_id, cliente_id)

            # Cerrar la sesión del punto de venta
            if orden_pos_id and sesion_pos_id:
                cerrar_sesion_punto_venta(nombre_punto_de_venta)
        else:
            print('La lista de productos está vacía.')

except Exception as e:
    print(f'Ocurrió un error: {e}')
