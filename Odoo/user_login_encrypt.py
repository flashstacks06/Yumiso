import xmlrpc.client
import sys
from cryptography.fernet import Fernet

def initialize_cipher(key):
    return Fernet(key)

def decrypt_data(cipher, encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

def authenticate_user(url, db, admin_username, admin_password, decrypted_data):
    common_endpoint = f'{url}/xmlrpc/2/common'
    object_endpoint = f'{url}/xmlrpc/2/object'

    try:
        # Conecta al servidor Odoo para obtener el ID de usuario
        common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
        user_id = common_proxy.authenticate(db, admin_username, admin_password, {})

        if user_id:
            #print(f'Se autenticó correctamente. Usuario ID: {user_id}')

            user_proxy = xmlrpc.client.ServerProxy(object_endpoint)

            # Cambiado para incluir tanto el nombre de usuario como la contraseña
            login, password_to_check = decrypted_data.split(':')

            user_info = user_proxy.execute_kw(
                db, user_id, admin_password,
                'res.users', 'authenticate', [db, login, password_to_check, {}]
            )

            if isinstance(user_info, int):
                # El resultado es el ID del usuario, no una lista
                user_name = login
            else:
                # El resultado es una lista que contiene información del usuario
                user_name = user_info[0].get('name', login)

            print(f'Inicio de sesión exitoso para el usuario {user_name}')

        else:
            print('Error al autenticar al usuario admin.')

    except xmlrpc.client.Fault as e:
        print(f'Inicio de sesión fallido para el usuario {login}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    secret_key_str = 'PzvGHUWbE3GNHMgGgU7G4TmxREf99oIbQ7_sGmqo040='  # Reemplaza con tu clave secreta
    encrypted_data_str = sys.argv[1]

    # Convierte las cadenas a bytes
    secret_key = secret_key_str.encode()
    encrypted_data = encrypted_data_str.encode()

    # Inicializa el cifrador con la clave secreta
    cipher = initialize_cipher(secret_key)

    # Descifra los datos
    decrypted_data = decrypt_data(cipher, encrypted_data)

    # Autentica al usuario en Odoo
    url = 'http://137.184.117.41:8069'
    db = 'yumiso'
    admin_username = 'info@inventoteca.com'
    admin_password = 'Gr4nj3r04dm1n'

    print("Datos descifrados:", decrypted_data)

    authenticate_user(url, db, admin_username, admin_password, decrypted_data)
