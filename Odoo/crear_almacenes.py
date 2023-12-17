import xmlrpc.client

# Configuración de la conexión
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Iniciar sesión en Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Acceder al modelo correspondiente
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Crear 10 almacenes
for i in range(1, 11):
    # Nombre largo y corto del almacén
    long_name = f"Maquina {i}"
    short_name = f"M{i}"

    # Crear el almacén
    models.execute_kw(db, uid, password, 'stock.warehouse', 'create', [{
        'name': long_name,
        'code': short_name,
    }])
