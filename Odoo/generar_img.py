import xmlrpc.client
import json
import sys
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import re
import os

# Configuración
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Iniciar sesión
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

maquina = sys.argv[1]
n_maquina = f"Maquina {maquina}"

# Obtener la información de los productos
products = models.execute_kw(db, uid, password,
    'product.product', 'search_read',
    [[['available_in_pos', '=', True],
      ['name', 'not in', ['Juegos', 'Premios']]]], {'fields': ['name', 'product_tmpl_id', 'qty_available']})

# Crear una lista para almacenar la información de los productos
product_info = []

# Función para generar y guardar una imagen PNG en la carpeta "img"
def guardar_imagen_png(data_str, nombre_archivo):
    try:
        data_bin = base64.b64decode(data_str)
        imagen = Image.open(io.BytesIO(data_bin))

        # Obtener la ruta completa para guardar la imagen en la carpeta "img"
        img_folder = os.path.join(os.path.dirname(__file__), 'img')
        os.makedirs(img_folder, exist_ok=True)

        img_path = os.path.join(img_folder, nombre_archivo)
        imagen.save(img_path, "PNG")
    except Exception as e:
        print(f'Error al guardar la imagen: {str(e)}')

# Obtener la imagen de los productos desde el modelo 'product.template' y generar imágenes
for product in products:
    product_tmpl_id = product['product_tmpl_id'][0]
    product_name = product['name']
    quantity = product['qty_available']

    product_template = models.execute_kw(db, uid, password,
        'product.template', 'read',
        [[product_tmpl_id]], {'fields': ['image_1920']})

    product_info_image = product_template[0]['image_1920'] if 'image_1920' in product_template[0] else ''

    if product_info_image:
        # Reemplazar espacios en el nombre del archivo con guiones bajos
        product_name = re.sub(r'\s', '_', product_name)
        guardar_imagen_png(product_info_image, f'{product_name}.png')

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
