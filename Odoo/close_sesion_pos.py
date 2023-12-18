from xmlrpc import client as xmlrpclib
from xmlrpc.client import ServerProxy

# Configura la conexión XML-RPC con tu instancia de Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'  # Reemplaza con la contraseña real

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Define el nombre del punto de venta
point_of_sale_name = "Test"  # Reemplaza con el nombre de tu punto de venta

# Busca el ID del punto de venta en base al nombre
pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [[('name', '=', point_of_sale_name)]])
if not pos_config_ids:
    raise Exception(f"No se encontró el punto de venta con el nombre '{point_of_sale_name}'")

pos_config_id = pos_config_ids[0]

# Crea una nueva sesión de punto de venta
session_name = "Mi Sesión"
session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [{
    'name': session_name,
    'config_id': pos_config_id,  # Asocia la sesión con el punto de venta
}])

# Verifica el ID de la sesión creada
print(f"Sesión creada con ID: {session_id}")

# Abre la sesión
try:
    models.execute_kw(db, uid, password, 'pos.session', 'open', [session_id])
    print("Sesión abierta exitosamente.")
except Exception as e:
    print(f"Error al abrir la sesión: {e}")

# Crea una orden de punto de venta
customer_name = "route@yumiso.com"
order_vals = {
    'session_id': session_id,
    'partner_id': False,  # Puedes asociar un cliente si es necesario
    'name': customer_name,
}
try:
    order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [order_vals])
    print(f"Orden creada con ID: {order_id}")
except Exception as e:
    print(f"Error al crear la orden: {e}")
    order_id = None  # Definimos la variable order_id como None en caso de error

# Agrega los productos a la orden con sus precios reales
product_ids = [21, 25, 23]  # IDs de los productos que se agregarán a la orden
if order_id:
    for product_id in product_ids:
        product = models.execute_kw(db, uid, password, 'product.product', 'read', [product_id], {'fields': ['name', 'lst_price']})
        order_line_vals = {
            'order_id': order_id,
            'product_id': product_id,
            'name': product[0]['name'],
            'price_unit': product[0]['lst_price'],  # Precio del producto
            'qty': 1,  # Cantidad
        }
        try:
            models.execute_kw(db, uid, password, 'pos.order.line', 'create', [order_line_vals])
            print(f"Producto agregado a la orden: {product[0]['name']}")
        except Exception as e:
            print(f"Error al agregar el producto a la orden: {e}")

# Realiza un pago (puedes agregar más métodos de pago según sea necesario)
payment_method_id = 1  # ID del método de pago
payment_vals = {
    'amount': 30.0,  # Monto a pagar
    'payment_date': xmlrpclib.DateTime(fields.datetime.now()),
    'payment_name': 'Efectivo',  # Nombre del método de pago
    'journal_id': payment_method_id,
    'order_id': order_id,
}
if order_id:
    try:
        models.execute_kw(db, uid, password, 'pos.payment', 'create', [payment_vals])
        print("Pago realizado exitosamente.")
    except Exception as e:
        print(f"Error al realizar el pago: {e}")

# Cierra la sesión sin importar si la orden se cierra con menos dinero
try:
    models.execute_kw(db, uid, password, 'pos.session', 'close', [session_id])
    print("Sesión cerrada exitosamente.")
except Exception as e:
    print(f"Error al cerrar la sesión: {e}")

# Puedes agregar manejo de excepciones y otras validaciones según tus necesidades
