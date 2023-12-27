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

# Nombre del almacén
warehouse_name = 'San Francisco'  # Reemplaza con el nombre real del almacén

# ID del producto
product_id = 14  # Reemplaza por el ID real del producto

# Nueva cantidad a mano
new_quantity = 11500.0

# Buscar el ID del almacén por nombre
warehouse_ids = models.execute_kw(db, uid, password,
    'stock.warehouse', 'search',
    [[['name', '=', warehouse_name]]], {'limit': 1})

if not warehouse_ids:
    print(f"El almacén '{warehouse_name}' no fue encontrado.")
else:
    warehouse_id = warehouse_ids[0]
    # Obtener la ubicación del stock principal para el almacén
    warehouse_data = models.execute_kw(db, uid, password,
        'stock.warehouse', 'read',
        [warehouse_ids], {'fields': ['lot_stock_id']})
    location_id = warehouse_data[0]['lot_stock_id'][0] if warehouse_data and 'lot_stock_id' in warehouse_data[0] else False
    
    if not location_id:
        print(f"No se encontró una ubicación interna dentro del almacén '{warehouse_name}'.")
    else:
        # Buscar stock.quant para el producto y la ubicación especificados
        quant_ids = models.execute_kw(db, uid, password,
            'stock.quant', 'search',
            [[['product_id', '=', product_id], ['location_id', '=', location_id]]])

        # Si existe un quant, actualízalo; si no, créalo.
        if quant_ids:
            models.execute_kw(db, uid, password,
                              'stock.quant', 'write',
                              [quant_ids, {'quantity': new_quantity, 'inventory_quantity': new_quantity}])
            print(f"Cantidad a mano actualizada para el producto ID {product_id} en la ubicación del almacén '{warehouse_name}' con ID {location_id}.")
        else:
            models.execute_kw(db, uid, password,
                              'stock.quant', 'create',
                              [{'product_id': product_id, 'location_id': location_id, 'quantity': new_quantity, 'inventory_quantity': new_quantity}])
            models.execute_kw(db, uid, password,
                              'stock.quant', 'write',
                              [quant_ids, {'inventory_quantity': new_quantity}])
            print(f"Cantidad a mano establecida para el producto ID {product_id} en la nueva ubicación del almacén con ID {location_id}.")
