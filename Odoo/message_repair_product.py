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

# Mensaje a escribir en el producto de la orden de reparación
mensaje = "Ubicación"
# Publicar el mensaje en el producto de la orden de reparación
models.execute_kw(db, uid, password,
    'product.product', 'message_post',
    [25], {'body': mensaje})
