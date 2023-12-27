import xmlrpc.client
import json

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

# Obtener la información de los productos
products = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['available_in_pos', '=', True], 
      ['name', 'not in', ['Juegos', 'Premios']]]], {'fields': ['name']})

# Información de los almacenes
warehouses = models.execute_kw(db, uid, password,
    'stock.warehouse', 'search_read',
    [[['name', '!=', 'San Francisco']]], {'fields': ['id', 'name', 'lot_stock_id']})
print(warehouses)
# Mapeo de ubicaciones de stock a almacenes
location_to_warehouse = {wh['lot_stock_id'][0]: (wh['id'], wh['name']) for wh in warehouses}

# Crear un diccionario para almacenar la información del producto
product_info = {}

# Obtener la cantidad de productos por ubicación
for product in products:
    product_name = product['name']
    product_info[product_name] = {
        'name': product_name,
        'locations': []
    }

    qty_by_location = models.execute_kw(db, uid, password,
        'stock.quant', 'search_read',
        [[['product_id', '=', product['id']], ['location_id', 'in', list(location_to_warehouse.keys())]]],
        {'fields': ['location_id', 'quantity']})
    
    for location_id, (warehouse_id, warehouse_name) in location_to_warehouse.items():
        quantity = next((qty['quantity'] for qty in qty_by_location if qty['location_id'][0] == location_id), 0)
        product_info[product_name]['locations'].append({
            'warehouse': warehouse_name,
            'quantity': quantity
        })

# Convertir el diccionario en JSON
result_json = json.dumps(list(product_info.values()), indent=4)

# Imprimir el JSON resultante
print(result_json)
