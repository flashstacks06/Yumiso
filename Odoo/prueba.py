import xmlrpc.client
import sys

# Verificación de argumentos de la línea de comandos
if len(sys.argv) != 5:
    print("Uso: python script.py <nombre> <correo> <contraseña> <grupo>")
    sys.exit(1)

# Datos de usuario desde argumentos de la línea de comandos
nombre, correo, contraseña, nombre_grupo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

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

    # Buscar el grupo por nombre
    group_ids = odoo_proxy.execute_kw(
        db, admin_user_id, admin_password,
        'res.groups', 'search', [[['name', '=', nombre_grupo]]]
    )

    if group_ids:
        group_id = group_ids[0]

        # Crear el nuevo usuario
        new_user_id = odoo_proxy.execute_kw(
            db, admin_user_id, admin_password,
            'res.users', 'create', [{
                'name': nombre,
                'login': correo,
                'password': contraseña,
                'groups_id': [(4, group_id)]
            }]
        )

        print(f"Usuario creado con éxito. ID: {new_user_id}")
    else:
        print(f"No se encontró el grupo: {nombre_grupo}")
else:
    print('Error al autenticar al administrador.')
