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

# Obtener los productos disponibles en el punto de venta
product_ids = models.execute_kw(db, uid, password,
    'product.product', 'search',
    [[['available_in_pos', '=', True]]])

# Obtener la información de los productos
products = models.execute_kw(db, uid, password,
    'product.product', 'read',
    [product_ids], {'fields': ['name', 'lst_price', 'qty_available']})

# Obtener la información de los almacenes
warehouses = models.execute_kw(db, uid, password,
    'stock.warehouse', 'search_read',
    [[]], {'fields': ['id', 'name', 'lot_stock_id']})

# Crear un diccionario para mapear IDs de ubicaciones de stock a nombres e IDs de almacenes
location_to_warehouse = {wh['lot_stock_id'][0]: (wh['id'], wh['name']) for wh in warehouses}

# Obtener las cantidades de productos por ubicación
for product in products:
    product_id = product['id']
    qty_by_location = models.execute_kw(db, uid, password,
        'stock.quant', 'search_read',
        [[['product_id', '=', product_id], ['location_id', 'in', list(location_to_warehouse.keys())]]],
        {'fields': ['location_id', 'quantity']})

    print("Producto:", product['name'])
    for qty in qty_by_location:
        location_id = qty['location_id'][0]
        warehouse_info = location_to_warehouse.get(location_id, ("ID desconocido", "Ubicación desconocida"))
        warehouse_id, warehouse_name = warehouse_info
        print(f"ID Almacén: {warehouse_id}, Almacén: {warehouse_name}, Cantidad: {qty['quantity']} Unidades disponible")
    print("-" * 30)
