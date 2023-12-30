import xmlrpc.client

# Configuración
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Iniciar sesión en Odoo y obtener UID
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Obtener el objeto models para realizar operaciones
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Numero de máquina deseado
numero_maquina = '70'  # Ejemplo de número de máquina
maquina = f"Maquina {numero_maquina}"

# Buscar el punto de venta con el número de máquina
punto_venta_id = models.execute_kw(db, uid, password,
    'pos.config', 'search',
    [[['name', '=', maquina]]],
    {'limit': 1})

#print(punto_venta_id)

# Asegúrate de que encontraste un punto de venta
if punto_venta_id:
    # Buscar la orden más nueva que tenga solo los dos productos "Juego" y "Premios"
    order_ids = models.execute_kw(db, uid, password,
        'pos.order', 'search',
        [[['session_id.config_id', '=', punto_venta_id[0]],
          ['lines.product_id.name', 'in', ['Juegos', 'Premios']],
          ['state', '=', 'done']]],  # Asegúrate de que la orden está pagada
        {'limit': 1, 'order': 'date_order desc'})  # Orden más reciente
    #print(order_ids)

    # Asegúrate de que encontraste una orden
    if order_ids:
        # Leer los datos de la orden
        order_data = models.execute_kw(db, uid, password,
            'pos.order', 'read',
            [order_ids],
            {'fields': ['lines']})
        #print(order_data)
        
        # Ahora busca la cantidad del producto "Premios"
        for line in order_data[0]['lines']:
            line_data = models.execute_kw(db, uid, password,
                'pos.order.line', 'read',
                [line],
                {'fields': ['product_id', 'qty']})
            
            if line_data[0]['product_id'][1] == 'Premios':
                cantidad_premios = line_data[0]['qty']
                print("Cantidad de Premios:", cantidad_premios)
                break
else:
    print("No se encontró el punto de venta con el número de máquina proporcionado.")
