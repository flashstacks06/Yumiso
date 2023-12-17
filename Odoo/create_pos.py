import xmlrpc.client

# Configuración de la conexión XML-RPC
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Crea un cliente XML-RPC
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Datos para crear una nueva configuración de punto de venta
pos_config_data = {
    'name': 'Maquina 12',
    # Agrega otros campos según sea necesario
}

# Crea la configuración de punto de venta
pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'create', [pos_config_data])

if pos_config_id:
    print(f'Se ha creado una nueva configuración de punto de venta con ID {pos_config_id}.')

    # Ahora puedes iniciar una sesión de punto de venta para esta configuración
    session_data = {
        'config_id': pos_config_id,
        'user_id': 1,  # Reemplaza con el ID del usuario asignado a la sesión (opcional)
    }

    # Iniciar la sesión de punto de venta
    session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [session_data])

    if session_id:
        print(f'Se ha iniciado la sesión de punto de venta con ID {session_id}.')
    else:
        print('Hubo un error al iniciar la sesión de punto de venta.')

else:
    print('Hubo un error al crear la configuración de punto de venta.')
