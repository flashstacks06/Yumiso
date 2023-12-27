import xmlrpc.client

# Configuración de la conexión
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Nombre para la nueva ubicación padre y almacén
nombre_ubicacion_padre = "Maquina 72"

# Iniciar sesión en Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Obtener los modelos
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Extraer la primera letra y los números para el código del almacén
codigo_almacen = nombre_ubicacion_padre[0] + ''.join(filter(str.isdigit, nombre_ubicacion_padre))
print(codigo_almacen)
# Crear el almacén con la ubicación de stock
warehouse_id = models.execute_kw(db, uid, password, 'stock.warehouse', 'create', [{
    'name': nombre_ubicacion_padre,
    'code': codigo_almacen,  # Código del almacén modificado
}])

picking_type_ids = models.execute_kw(db, uid, password, 'stock.picking.type', 'search', [[
    ['warehouse_id', '=', warehouse_id],
    ['code', '=', 'outgoing'],
    ['default_location_src_id.usage', '=', 'internal'],
    ['default_location_dest_id.usage', '=', 'customer']
]])
picking_type_id = picking_type_ids[0] if picking_type_ids else False
payment_method_ids = models.execute_kw(db, uid, password, 'pos.payment.method', 'search', [[]])

# Crear el punto de venta y asignarle el almacén y el tipo de operación de punto de venta
# Comprueba si picking_type_ids no está vacía antes de intentar obtener el primer elemento
pos_config_id = models.execute_kw(db, uid, password, 'pos.config', 'create', [{
    'name': nombre_ubicacion_padre,
    'warehouse_id': warehouse_id,
    'picking_type_id': picking_type_id if picking_type_id else False,
    'payment_method_ids': [(6, 0, payment_method_ids)],
}])

consumable_data = {
    'name': nombre_ubicacion_padre,  # Nombre específico del producto
    'type': 'consu',  # Tipo de producto consumible
    # Otros campos relevantes, como precio, descripción, categoría, etc.
}

# Llamar al método 'create' para crear el producto consumible
product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [consumable_data])


print(f"Ubicación padre '{nombre_ubicacion_padre}', ubicación 'Stock', almacén y punto de venta creados con éxito.")
print(f"ID del Almacén: {warehouse_id}, ID del Punto de Venta: {pos_config_id}")
