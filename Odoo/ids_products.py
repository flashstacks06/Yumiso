import xmlrpc.client

URL_DEL_ODOO = 'http://137.184.117.41:8069'  # Nueva URL de Odoo
DB_NAME = 'yumiso'  # Nuevo nombre de la base de datos
USERNAME = 'cbernalestrella@gmail.com'  # Nuevo nombre de usuario
PASSWORD = '12345678'  # Nueva contraseña

# Conectarse a Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL_DEL_ODOO))
uid = common.authenticate(DB_NAME, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL_DEL_ODOO))

# Obtener IDs de productos en inventario
def obtener_ids_productos_en_inventario():
    domain = [('product_id', '!=', False)]  # Filtrar productos con ID no nulo
    fields = ['product_id']  # Campo que deseas recuperar

    productos_en_inventario = models.execute_kw(DB_NAME, uid, PASSWORD, 'stock.quant', 'search_read', [domain], {'fields': fields})
    
    # Extraer solo los IDs de los productos
    ids_productos_en_inventario = [producto['product_id'][0] for producto in productos_en_inventario]
    
    return ids_productos_en_inventario

# Ejemplo de cómo usar la función
if __name__ == '__main__':
    try:
        # Obtener IDs de productos en inventario
        ids_productos_en_inventario = obtener_ids_productos_en_inventario()

        # Imprimir IDs de productos en inventario
        print("IDs de productos en inventario:", ids_productos_en_inventario)

    except Exception as e:
        print(f'Ocurrió un error: {e}')
