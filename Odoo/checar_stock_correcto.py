import xmlrpc.client
import json
import sys

# Configuración
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Analizar el JSON de entrada
input_json = {"Correo": "k5k+nUIENbpUJU9XqQLdwX19PzOwajtZ8ud4c466q6E=","qrid": "71","bag": "3","data": "{\"Stock\":[\"14:45\",\"15:58\",\"16:45\",\"21:55\",\"22:44\"],\"Refill\":[\"14:44\",\"15:44\",\"16:88\",\"21:445\",\"22:449\"]}"}

data_dict = json.loads(input_json["data"])

maquina = input_json["qrid"]  # Obtener el número de máquina desde qrid
n_maquina = f"Maquina {maquina}"

# Iniciar sesión en la fuente XML-RPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Obtener los modelos en la fuente XML-RPC
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Obtener la información de los productos de la fuente XML-RPC
products_from_xmlrpc = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['available_in_pos', '=', True],
      ['name', 'not in', ['Juegos', 'Premios']]]], {'fields': ['name', 'id']})

# Información de los almacenes de la fuente XML-RPC
warehouses_from_xmlrpc = models.execute_kw(db, uid, password,
    'stock.warehouse', 'search_read',
    [[['name', '=', n_maquina]]], {'fields': ['id', 'name', 'lot_stock_id']})

# Mapeo de ubicaciones de stock a almacenes de la fuente XML-RPC
location_to_warehouse_from_xmlrpc = {wh['lot_stock_id'][0]: (wh['id'], wh['name']) for wh in warehouses_from_xmlrpc}

# Crear un diccionario para almacenar la información de los productos de la fuente XML-RPC
product_info_from_xmlrpc = {}

# Obtener la cantidad de productos por ubicación de la fuente XML-RPC
for product in products_from_xmlrpc:
    product_name = product['name']
    product_id = product['id']  # Obtener el ID del producto

    qty_by_location = models.execute_kw(db, uid, password,
        'stock.quant', 'search_read',
        [[['product_id', '=', product_id], ['location_id', 'in', list(location_to_warehouse_from_xmlrpc.keys())]]],
        {'fields': ['location_id', 'quantity']})
    
    product_quantities = {}
    for location_id, (warehouse_id, warehouse_name) in location_to_warehouse_from_xmlrpc.items():
        quantity = next((qty['quantity'] for qty in qty_by_location if qty['location_id'][0] == location_id), 0)
        product_quantities[location_id] = int(quantity)  # Convertir a entero
    
    product_info_from_xmlrpc[product_id] = product_quantities

# Obtener la lista de elementos para "Stock" del JSON
stock_elements_from_json = []
for item in data_dict["Stock"]:
    parts = item.split(":")
    if len(parts) == 2:
        stock_elements_from_json.append({parts[0]: int(parts[1])})  # Convertir a entero

# Comparar las cantidades de stock entre los dos conjuntos de datos
differences = []
for item in stock_elements_from_json:
    for key, value in item.items():
        product_id = int(key)
        if product_id in product_info_from_xmlrpc:
            xmlrpc_quantities = product_info_from_xmlrpc[product_id]
            xmlrpc_total_quantity = sum(xmlrpc_quantities.values())
            diff = value - xmlrpc_total_quantity
            differences.append({key: diff})

# Imprimir la lista de diferencias
print(differences)


