import xmlrpc.client
import base64
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Verificación de argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Uso: python script.py <mensaje_encriptado>")
    sys.exit(1)

# Datos Encriptados desde argumentos de la línea de comandos
encrypted_message = sys.argv[1]

# Clave y IV predefinidos
key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='

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

# Desencriptar Usuario y Contraseña
encrypted_user, encrypted_password = encrypted_message.split(':')
decrypted_user = unpad(decrypt_aes(encrypted_user, key, iv)).decode('utf-8').strip()
decrypted_password = unpad(decrypt_aes(encrypted_password, key, iv)).decode('utf-8').strip()

# Autenticación XML-RPC
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
admin_username = 'info@inventoteca.com'
admin_password = 'Gr4nj3r04dm1n'

# Endpoints XML-RPC
common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

try:
    common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
    user_id = common_proxy.authenticate(db, admin_username, admin_password, {})

    if user_id:
        user_proxy = xmlrpc.client.ServerProxy(object_endpoint)
        user_info = user_proxy.execute_kw(
            db, user_id, admin_password,
            'res.users', 'authenticate', [db, decrypted_user, decrypted_password, {}]
        )

        if isinstance(user_info, int):
            print(f'Inicio de sesión exitoso para el usuario {decrypted_user}')
        else:
            print('Error al autenticar al usuario.')
    else:
        print('Error al autenticar al usuario admin.')

except xmlrpc.client.Fault as e:
    print(f'Error XML-RPC: {e.faultString}')
except Exception as e:
    print(f'Error General: {e}')
