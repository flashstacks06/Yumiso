import xmlrpc.client

# Configura la conexión con el servidor Odoo
url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'  # Contraseña proporcionada por el usuario

common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

# Conecta al servidor Odoo para obtener el ID de usuario
common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
user_id = common_proxy.authenticate(db, username, password, {})

if user_id:
    print(f'Se autenticó correctamente. Usuario ID: {user_id}')

    # Ahora, busca el ID del usuario por nombre o ID
    user_proxy = xmlrpc.client.ServerProxy(object_endpoint)
    user_name_or_id = 'Perenganito Route'  # Reemplaza con el nombre o ID del usuario real

    user_info = user_proxy.execute_kw(
        db, user_id, password,
        'res.users', 'search_read', [[['name', '=', user_name_or_id]]],
        {'fields': ['id']}
    )

    if user_info:
        user_id_to_update = user_info[0]['id']

        # Actualiza el campo 'groups_id' con una lista vacía para eliminar todos los grupos
        user_proxy.execute_kw(
            db, user_id, password,
            'res.users', 'write', [[user_id_to_update], {'groups_id': [(6, 0, [])]}]
        )

        print(f'Se eliminaron todos los grupos del usuario con ID {user_id_to_update}')

    else:
        print(f'No se encontró el usuario con nombre o ID {user_name_or_id}')

else:
    print('Error al autenticar al usuario.')
