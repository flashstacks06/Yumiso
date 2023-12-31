import xmlrpc.client
import sys
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

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

if len(sys.argv) != 2:
    print("Uso: python script.py <mensaje_encriptado>")
    sys.exit(1)

# Datos Encriptados desde argumentos de la línea de comandos
encrypted_message = sys.argv[1]

# Clave y IV predefinidos para la desencriptación
key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='

# Separar el mensaje encriptado en usuario y contraseña
encrypted_user, encrypted_password = encrypted_message.split(':')

# Desencriptar Usuario
username = unpad(decrypt_aes(encrypted_user, key, iv)).decode('utf-8').strip()

# Desencriptar Contraseña
password = unpad(decrypt_aes(encrypted_password, key, iv)).decode('utf-8').strip()

# Configuración del servidor Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
admin_username = 'info@inventoteca.com'  # Nombre de usuario del administrador
admin_password = 'Gr4nj3r04dm1n'        # Contraseña del administrador

# Endpoints XML-RPC
common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

# Conexión y Autenticación en el servidor Odoo como usuario administrador
common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
admin_user_id = common_proxy.authenticate(db, admin_username, admin_password, {})

if admin_user_id:
    # Conexión para operaciones adicionales con credenciales de administrador
    admin_user_proxy = xmlrpc.client.ServerProxy(object_endpoint)
    
    # Intentar autenticar al usuario con el nombre de usuario y contraseña proporcionados
    try:
        user_id = admin_user_proxy.execute_kw(
            db, admin_user_id, admin_password,
            'res.users', 'authenticate', [db, username, password, {}]
        )

        if isinstance(user_id, int):
            #print(f'Inicio de sesión exitoso para el usuario {username}')
            
            # Leer los roles asignados al usuario utilizando la cuenta del administrador
            roles = admin_user_proxy.execute_kw(
                db, admin_user_id, admin_password,
                'res.users', 'read', [user_id],
                {'fields': ['groups_id']}
            )

            if roles and roles[0]['groups_id']:
                #print('Grupos del usuario:')
                for role_id in roles[0]['groups_id']:
                    role_info = admin_user_proxy.execute_kw(
                        db, admin_user_id, admin_password,
                        'res.groups', 'read', [role_id],
                        {'fields': ['name']}
                    )
                    print(f'{role_info[0]["name"]}')
            else:
                print(f'No tiene grupos asignados.')

    except xmlrpc.client.Fault:
        print('Credenciales incorrectas')
else:
    print('Credenciales incorrectas')
