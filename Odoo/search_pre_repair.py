import xmlrpc.client
import sys
import base64
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Funciones de Desencriptación y Quitar Relleno
def decrypt_aes(encrypted_data, base64_key, base64_iv):
    key = base64.urlsafe_b64decode(base64_key)
    iv = base64.urlsafe_b64decode(base64_iv)

    # Asegurarse de que la cadena encriptada tenga el relleno correcto
    padded_encrypted_data = encrypted_data + '=' * (-len(encrypted_data) % 4)
    encrypted_data_bytes = base64.urlsafe_b64decode(padded_encrypted_data)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(plaintext) + unpadder.finalize()
    return unpadded_data.strip()  # Elimina .decode('utf-8')

# Función para buscar al cliente
def buscar_cliente(correo_cliente_enc, key, iv):
    correo_cliente = decrypt_aes(correo_cliente_enc, key, iv).strip()  # Elimina .decode('utf-8')
    cliente = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['email', '=', correo_cliente]]],
        {'fields': ['id', 'email'], 'limit': 1})
    if cliente:
        return {'id': cliente[0]['id'], 'login': cliente[0]['email']}
    else:
        return None

# Función para confirmar la orden de reparación
def confirmar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_validate', [orden_id])

# Función para iniciar la orden de reparación
def iniciar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_repair_start', [orden_id])

def finalizar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_repair_end', [orden_id])


# Clave y IV predefinidos para desencriptación
key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='

# Argumentos de la línea de comandos
numero_maquina = sys.argv[2]  # Número de la máquina
ids_productos_str = sys.argv[3]  # String de IDs de productos (formato de lista)
print(ids_productos_str)
correo_cliente_enc = sys.argv[1]  # Correo electrónico del cliente encriptado

ids_productos = [int(x) for x in ids_productos_str.strip('[]').split(',') if int(x) != 0]
print(ids_productos)

# URL y credenciales para el servidor XML-RPC
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Autenticación y conexión
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Convertir los IDs de productos en una lista de enteros
#ids_productos = [int(x) for x in ids_productos_str.strip('[]').split(',') if x.isdigit()]
#print(ids_productos)
# Desencriptar el correo electrónico del cliente
correo_cliente = decrypt_aes(correo_cliente_enc, key, iv)

# Buscar el producto por número de máquina
producto_id = models.execute_kw(db, uid, password, 'product.product', 'search', [[['name', 'ilike', f'Maquina {numero_maquina}']]])
producto_id = producto_id[0] if producto_id else None

# Unidad de Medida y ubicaciones por defecto (ajustar según tu sistema)
uom_id = 1
location_id = 12
location_dest_id = 15

# Buscar órdenes de reparación en estado 'draft' para la máquina especificada
search_domain = [('product_id', '=', producto_id), ('state', '=', 'draft')]
draft_repair_ids = models.execute_kw(db, uid, password, 'repair.order', 'search', [search_domain])


# Actualizar las órdenes de reparación
for repair_id in draft_repair_ids:
    # Eliminar las líneas de operación existentes
    models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {'operations': [(5,)]}])

    # Añadir nuevas líneas de operación con los productos especificados
    for pid in ids_productos:
        # Obtener el precio de venta del producto
        producto_info = models.execute_kw(db, uid, password, 'product.product', 'read', [pid], {'fields': ['list_price']})
        precio_producto = producto_info[0]['list_price'] if producto_info else 0

        models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {
            'operations': [(0, 0, {
                'product_id': pid,
                'product_uom_qty': 1,
                'product_uom': uom_id,
                'name': f'Product ID {pid}',
                'price_unit': precio_producto,
                'location_id': location_id,
                'location_dest_id': location_dest_id
            })]
        }])

    # Actualizar el cliente de la orden
    cliente = buscar_cliente(correo_cliente_enc, key, iv)
    if cliente:
        cliente_id = cliente['id']
        models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {'partner_id': cliente_id}])

    # Confirmar la orden de reparación
    confirmar_orden_reparacion(repair_id)

    # Iniciar la orden de reparación
    iniciar_orden_reparacion(repair_id)

    # Finalizar la orden de reparación
    finalizar_orden_reparacion(repair_id)


print(f"Las órdenes de reparación en estado 'draft' para 'Maquina {numero_maquina}' han sido actualizadas.")
