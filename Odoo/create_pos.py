import xmlrpc.client

url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'cbernalestrella@gmail.com'
password = '12345678'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Conexión al objeto models
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Crear un nuevo punto de venta
point_of_sale = {
    'name': 'Maquina 21',
    # Otros campos necesarios aquí
}

pos_id = models.execute_kw(db, uid, password,
    'pos.config', 'create', [point_of_sale])

print(f"Punto de venta creado con ID: {pos_id}")