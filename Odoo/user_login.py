import xmlrpc.client
import sys

def authenticate_user(url, db, admin_username, admin_password, login, password_to_check):
    common_endpoint = f'{url}/xmlrpc/2/common'
    object_endpoint = f'{url}/xmlrpc/2/object'

    try:
        # Conecta al servidor Odoo para obtener el ID de usuario
        common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
        user_id = common_proxy.authenticate(db, admin_username, admin_password, {})

        if user_id:
            print(f'Se autenticó correctamente. Usuario ID: {user_id}')

            user_proxy = xmlrpc.client.ServerProxy(object_endpoint)

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
    if len(sys.argv) != 3:
        print("Uso: python script.py <nombre_usuario> <contraseña>")
        sys.exit(1)

    url = 'http://137.184.117.41:8069'
    db = 'yumiso'
    admin_username = 'info@inventoteca.com'
    admin_password = 'Gr4nj3r04dm1n'
    login = sys.argv[1]
    password_to_check = sys.argv[2]

    authenticate_user(url, db, admin_username, admin_password, login, password_to_check)
