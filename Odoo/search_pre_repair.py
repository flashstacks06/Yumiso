import xmlrpc.client
import sys

# Argumentos de la línea de comandos
numero_maquina = sys.argv[1]  # Número de la máquina
ids_productos_str = sys.argv[2]  # String de IDs de productos (formato de lista)
nuevo_correo_cliente = sys.argv[3]  # Nuevo correo electrónico del cliente

# Configuración del servidor XML-RPC
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión y autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Buscar órdenes de reparación en estado 'draft' para la máquina especificada
search_domain = [('product_id.name', '=', f'Maquina {numero_maquina}'), ('state', '=', 'draft')]
draft_repair_ids = models.execute_kw(db, uid, password, 'repair.order', 'search', [search_domain])

# Convertir los IDs de productos en una lista de enteros
ids_productos = [int(x) for x in ids_productos_str.strip('[]').split(',') if x.isdigit()]

# Buscar el cliente basado en el nuevo correo electrónico
clientes = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['email', '=', nuevo_correo_cliente]]], {'fields': ['id']})
cliente_id = clientes[0]['id'] if clientes else None

if not cliente_id:
    print(f"No se pudo encontrar un cliente con el correo electrónico: {nuevo_correo_cliente}")
    sys.exit(1)

# Unidad de Medida por defecto y ubicaciones (ajustar según tu sistema)
uom_id = 1
location_id = 12
location_dest_id = 15

# Actualizar las órdenes de reparación
for repair_id in draft_repair_ids:
    # Actualizar el cliente de la orden
    models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {'partner_id': cliente_id}])

    # Eliminar las líneas de operación existentes
    models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {'operations': [(5,)]}])

    # Añadir nuevas líneas de operación
    for pid in ids_productos:
        # Obtener el precio de venta del producto
        producto_info = models.execute_kw(db, uid, password, 'product.product', 'read', [pid], {'fields': ['list_price']})
        precio_producto = producto_info[0]['list_price'] if producto_info else 0

        models.execute_kw(db, uid, password, 'repair.order', 'write', [[repair_id], {
            'operations': [(0, 0, {
                'product_id': pid,
                'product_uom_qty': 1,
                'product_uom': uom_id,
                'name': f'Producto {pid}',
                'price_unit': precio_producto,
                'location_id': location_id,
                'location_dest_id': location_dest_id
            })]
        }])

print(f"Las órdenes de reparación en estado 'draft' para 'Maquina {numero_maquina}' han sido actualizadas con los nuevos productos y cliente.")
