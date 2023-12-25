import xmlrpc.client

# Configuración
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Iniciar sesión
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Obtener los modelos
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# ID del producto y del almacén
product_id = 14  # Reemplaza por el ID real del producto
location_id = 18  # Reemplaza por el ID real de la ubicación del almacén

# Nueva cantidad a mano
new_quantity = 1000.0

# Buscar stock.quant para el producto y la ubicación especificados
quant_ids = models.execute_kw(db, uid, password,
    'stock.quant', 'search',
    [[['product_id', '=', product_id], ['location_id', '=', location_id]]])

# Si existe un quant, actualízalo; si no, créalo.
if quant_ids:
    models.execute_kw(db, uid, password,
                      'stock.quant', 'write',
                      [quant_ids, {'inventory_quantity': new_quantity}])
else:
    models.execute_kw(db, uid, password,
                      'stock.quant', 'create',
                      [{'product_id': product_id, 'location_id': location_id, 'inventory_quantity': new_quantity}])

print("Cantidad a mano actualizada para el producto en el almacén especificado.")
