import xmlrpc.client
import sys
import base64
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Argumentos de la línea de comandos
numero_maquina = sys.argv[1]  # Número de la máquina
correo_cliente = sys.argv[2]  # Correo electrónico del cliente
numero_maquina = sys.argv[2]  # Número de la máquina
correo_cliente_enc = sys.argv[1]  # Correo electrónico del cliente
ids_productos_str = sys.argv[3]  # String de IDs de productos (formato de lista)

# Eliminar los corchetes y espacios, y luego convertir la cadena en una lista de enteros
ids_productos = [int(x) for x in ids_productos_str.strip('[]').split(',') if x.strip()]
ids_productos = [int(x) for x in ids_productos_str.strip('[]').split(',') if int(x) != 0]



# URL y credenciales para el servidor XML-RPC
@@ -33,7 +38,8 @@ def buscar_producto(numero_maquina):
    return productos[0] if productos else None

# Función para buscar el cliente basado en el correo electrónico
def buscar_cliente(correo_cliente):
def buscar_cliente():
    correo_cliente = unpad(decrypt_aes(correo_cliente_enc, key, iv)).decode('utf-8').strip()
    cliente = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['email', '=', correo_cliente]]],
@@ -96,11 +102,33 @@ def iniciar_orden_reparacion(orden_id):
def finalizar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_repair_end', [orden_id])

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

# Clave y IV predefinidos para desencriptación
key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='


# Ejecutar el script
if __name__ == "__main__":
    producto = buscar_producto(numero_maquina)
    print(producto)
    cliente = buscar_cliente(correo_cliente)
    cliente = buscar_cliente()
    print(cliente)

    if producto and cliente:
