import xmlrpc.client
import json
import sys

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

maquina = sys.argv[1]
n_maquina = f"Maquina {maquina}"

# Obtener la información de los productos
products = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['available_in_pos', '=', True],
      ['name', 'not in', ['Juegos', 'Premios']]]], {'fields': ['name', 'product_tmpl_id', 'qty_available']})  # Incluir el campo 'qty_available'

# Crear una lista para almacenar la información de los productos
product_info = []

# Obtener la imagen de los productos desde el modelo 'product.template'
for product in products:
    product_tmpl_id = product['product_tmpl_id'][0]
    product_name = product['name']
    quantity = product['qty_available']  # Obtener la cantidad disponible

    # Obtener la imagen del producto desde el modelo 'product.template'
    product_template = models.execute_kw(db, uid, password,
        'product.template', 'read',
        [[product_tmpl_id]], {'fields': ['image_1920']})
    
    product_info_image = product_template[0]['image_1920'] if 'image_1920' in product_template[0] else ''

    product_info.append({
        'product_id': product['id'],
        'product_name': product_name,
        'product_image': product_info_image,
        'quantity': quantity,
    })

# Convertir la lista en JSON
result_json = json.dumps(product_info, indent=4)

# Imprimir el JSON resultante
print(result_json)
