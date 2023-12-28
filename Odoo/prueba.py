import xmlrpc.client

# Configuración
url = 'http://137.184.86.135:8069'  # Asegúrate de que esta URL sea accesible
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Iniciar sesión
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Obtener los modelos
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Número de la máquina que se va a buscar
machine_number = '71'  # Cambiar por el número de máquina recibido
product_name_to_search = f"Maquina {machine_number}"  # Completa el nombre del producto

try:
    # Buscar producto por nombre
    product_ids = models.execute_kw(db, uid, password,
        'product.product', 'search',
        [[['name', '=', product_name_to_search]]],
        {'limit': 1})

    if product_ids:
        product_id = product_ids[0]
        print(f"ID del producto para '{product_name_to_search}': {product_id}")
    else:
        print(f"No se encontró el producto con el nombre '{product_name_to_search}'")

except Exception as e:
    print(f"Se produjo un error al intentar obtener los datos: {e}")
