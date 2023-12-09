import xmlrpc.client

# Configura la conexión con el servidor Odoo
url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'  # Reemplaza con la contraseña real

common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

# Conecta al servidor Odoo para obtener el ID de usuario
common_proxy = xmlrpc.client.ServerProxy(common_endpoint)
user_id = common_proxy.authenticate(db, username, password, {})

if user_id:
    print(f'Se autenticó correctamente. Usuario ID: {user_id}')

    # Ahora, lee los roles disponibles
    user_proxy = xmlrpc.client.ServerProxy(object_endpoint)

    # Lee todos los registros de 'res.groups' y muestra los nombres
    roles = user_proxy.execute_kw(
        db, user_id, password,
        'res.groups', 'search_read', [[]],
        {'fields': ['id', 'name']}
    )

    if roles:
        print('Roles disponibles:')
        for role_info in roles:
            print(f'- ID: {role_info["id"]}, Nombre: {role_info["name"]}')
    else:
        print('No se encontraron roles.')

else:
    print('Error al autenticar al usuario.')
