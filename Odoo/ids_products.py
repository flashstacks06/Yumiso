import xmlrpc.client

URL_DEL_ODOO = 'http://137.184.86.135:8069/'
DB_NAME = 'yumiso'
USERNAME = 'info@inventoteca.com'
PASSWORD = 'Gr4nj3r04dm1n'

# Conectarse a Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL_DEL_ODOO))
uid = common.authenticate(DB_NAME, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL_DEL_ODOO))

# Obtener IDs de productos
def obtener_ids_productos():
    domain = []  # Puedes definir filtros aquí si es necesario
    fields = ['id', 'name']  # Campos que deseas recuperar, por ejemplo 'id' y 'name'

    productos = models.execute_kw(DB_NAME, uid, PASSWORD, 'product.template', 'search_read', [domain], {'fields': fields})
    
    # Extraer los IDs y nombres de los productos
    info_productos = [(producto['id'], producto['name']) for producto in productos]
    
    return info_productos

# Ejemplo de cómo usar la función
if __name__ == '__main__':
    try:
        # Obtener IDs y nombres de productos
        info_productos = obtener_ids_productos()

        # Imprimir la información de los productos
        for id, name in info_productos:
            print(f"ID: {id}, Nombre: {name}")

    except Exception as e:
        print(f'Ocurrió un error: {e}')
