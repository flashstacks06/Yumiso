import xmlrpc.client
import sys

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
    odoo_proxy = xmlrpc.client.ServerProxy(object_endpoint)

    # Obtener todos los grupos
    groups = odoo_proxy.execute_kw(
        db, admin_user_id, admin_password,
        'res.groups', 'search_read', [[]],
        {'fields': ['id', 'name']}
    )

    if groups:
        print("ID y nombre de cada grupo disponible:")
        for group in groups:
            print(f"ID: {group['id']}, Nombre: {group['name']}")
    else:
        print("No se encontraron grupos.")
else:
    print('Error al autenticar al administrador.')
