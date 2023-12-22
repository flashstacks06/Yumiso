import xmlrpc.client

# Datos de conexión a Odoo
url = 'http://137.184.86.135:8069/'
db = 'Yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta):
    domain = [('name', '=', nombre_punto_de_venta)]
    pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [domain])

    if pos_config_ids:
        return pos_config_ids[0]
    else:
        raise Exception(f'No se encontró un punto de venta con el nombre: {nombre_punto_de_venta}')

# Nombre del punto de venta a buscar (reemplazar con el nombre correcto)
nombre_punto_de_venta = 'Maquina 21'

try:
    id_punto_de_venta = obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta)
    print(f'El ID del punto de venta "{nombre_punto_de_venta}" es: {id_punto_de_venta}')

except Exception as e:
    print(f'Ocurrió un error: {e}')
