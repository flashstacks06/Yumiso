import xmlrpc.client

# Configuración de conexión
url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'cbernalestrella@gmail.com'
password = '12345678'
common_endpoint = f'{url}/xmlrpc/2/common'
object_endpoint = f'{url}/xmlrpc/2/object'

# Conexión al servidor Odoo
common = xmlrpc.client.ServerProxy(common_endpoint)
uid = common.authenticate(db, username, password, {})

if uid:
    print("Autenticación exitosa. UID:", uid)

    # ID del producto que deseas consultar
    product_id = 39  # Reemplaza con el ID real del producto

    # Campos que deseas obtener
    fields = ['name', 'image_1920', 'list_price']

    # Obtener la información específica del producto desde Odoo
    product_info = xmlrpc.client.ServerProxy(object_endpoint).execute_kw(
        db, uid, password, 'product.template', 'read', [product_id], {'fields': fields}
    )

    if product_info:
        print("Información del Producto:")
        print(f"Nombre: {product_info[0]['name']}")
        print(f"URL de la Imagen: {product_info[0]['image_1920']}")
        print(f"Precio por Unidad: {product_info[0]['list_price']}")
    else:
        print("Error al obtener la información del producto")
else:
    print("Error en la autenticación")
