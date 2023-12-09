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
        user_id_to_check = user_info[0]['id']

        # Lee los roles asignados al usuario
        roles = user_proxy.execute_kw(
            db, user_id, password,
            'res.users', 'read', [user_id_to_check],
            {'fields': ['name', 'groups_id']}
        )

        if roles and roles[0]['groups_id']:
            print(f'Roles del usuario con ID {user_id_to_check}:')
            for role_id in roles[0]['groups_id']:
                # Lee la información de cada rol
                role_info = user_proxy.execute_kw(
                    db, user_id, password,
                    'res.groups', 'read', [role_id],
                    {'fields': ['name']}
                )
                print(f'- {role_info[0]["name"]}')
        else:
            print('El usuario no tiene roles asignados.')

    else:
        print(f'No se encontró el usuario con nombre o ID {user_name_or_id}')

else:
    print('Error al autenticar al usuario.')
