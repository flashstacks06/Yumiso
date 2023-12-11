import xmlrpc.client

url = 'http://137.184.86.135:8069/'
db = 'yumiso'
admin_username = 'info@inventoteca.com'
admin_password = 'Gr4nj3r04dm1n'
# Datos desencriptados del usuario y la contraseña
decrypted_user = 'cbernalestrella@gmail.com'
decrypted_password = '12345678'

common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

try:
    common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
    user_id = common_proxy.authenticate(db, admin_username, admin_password, {})

    if user_id:
        login, password_to_check = decrypted_user, decrypted_password
        user_proxy = xmlrpc.client.ServerProxy(object_endpoint)

        user_info = user_proxy.execute_kw(
            db, user_id, admin_password,
            'res.users', 'authenticate', [db, login, password_to_check, {}]
        )

        if isinstance(user_info, int):
            user_name = login
        else:
            user_name = user_info[0].get('name', login)

        print(f'Inicio de sesión exitoso para el usuario {user_name}')
    else:
        print('Error al autenticar al usuario admin.')

except xmlrpc.client.Fault as e:
    print(f'Inicio de sesión fallido para el usuario {admin_username}: {e.faultString}')
