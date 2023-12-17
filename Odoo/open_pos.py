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

# Define los datos para el nuevo punto de venta
pos_data = {
    'name': 'Nombre de tu Punto de Venta',
    'company_id': 1,  # Reemplaza con el ID de tu empresa
    'sequence_id': 1,  # Reemplaza con el ID de tu secuencia de punto de venta
    'journal_id': 1,  # Reemplaza con el ID de tu diario de ventas
    'iface_cashdrawer': True,  # Activa el cajón de efectivo (si es compatible)
    'iface_invoicing': True,  # Activa la facturación (si es compatible)
}

# Crea el punto de venta
pos_id = models.execute_kw(db, uid, password, 'pos.config', 'create', [pos_data])

if pos_id:
    print(f'El punto de venta con ID {pos_id} ha sido creado exitosamente.')
else:
    print('Hubo un error al crear el punto de venta.')
