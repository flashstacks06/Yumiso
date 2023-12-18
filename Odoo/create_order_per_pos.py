import xmlrpc.client

# Datos de conexión a Odoo
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

def obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta):
    domain = [('name', '=', nombre_punto_de_venta)]
    pos_config_ids = models.execute_kw(db, uid, password, 'pos.config', 'search', [domain])

    if pos_config_ids:
        return pos_config_ids[0]
    else:
        raise Exception(f'No se encontró un punto de venta con el nombre: {nombre_punto_de_venta}')

def buscar_cliente_por_correo(correo_cliente):
    domain = [('email', '=', correo_cliente)]
    cliente = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], {'fields': ['id']})

    if cliente:
        return cliente[0]['id']
    else:
        raise Exception(f'No se encontró un cliente con el correo: {correo_cliente}')

def iniciar_sesion_pos(id_punto_de_venta):
    # Crear una sesión de punto de venta
    session_data = {
        'config_id': id_punto_de_venta,
        'user_id': uid,
    }

    session_id = models.execute_kw(db, uid, password, 'pos.session', 'create', [session_data])
    return session_id

def crear_orden_pos(product_ids, session_id, cliente_id):
    pos_order_data = {
        'partner_id': cliente_id,  # ID del cliente
        'session_id': session_id,  # ID de la sesión de punto de venta
        'name': 'Semana 40',  # Nombre de la sesión
        'amount_tax': 10.0,  # Valor correcto para amount_tax
        'amount_total': 0.0,  # Valor inicial para amount_total
        'amount_paid': 0.0,  # Valor inicial para amount_paid
        'amount_return': 0.0,  # Valor inicial para amount_return
        'lines': [],
    }

    for product_id in product_ids:
        # Obtener información del producto
        product_info = models.execute_kw(db, uid, password, 'product.template', 'read', [product_id], {'fields': ['id', 'name', 'list_price']})

        if product_info:
            # Calcular subtotal
            subtotal = product_info[0]['list_price'] * 2

            # Agregar línea de pedido al diccionario
            pos_order_data['lines'].append((0, 0, {
                'product_id': product_info[0]['id'],
                'qty': 2,
                'price_unit': product_info[0]['list_price'],
                'price_subtotal': subtotal,
                'price_subtotal_incl': subtotal,
                'full_product_name': product_info[0]['name'],
            }))

    # Calcular y establecer el valor de amount_total
    pos_order_data['amount_total'] = sum(line[2]['qty'] * line[2]['price_unit'] for line in pos_order_data['lines'])

    # Crear la orden de punto de venta
    order_id = models.execute_kw(db, uid, password, 'pos.order', 'create', [pos_order_data])
    return order_id

# Nombre del punto de venta a buscar (reemplazar con el nombre correcto)
nombre_punto_de_venta = 'Maquina 12'

try:
    id_punto_de_venta = obtener_id_punto_de_venta_por_nombre(nombre_punto_de_venta)
    print(f'El ID del punto de venta "{nombre_punto_de_venta}" es: {id_punto_de_venta}')

    # Ingresar el correo del cliente
    correo_cliente = input('Ingrese el correo del cliente: ')

    # Buscar el ID del cliente por correo
    cliente_id = buscar_cliente_por_correo(correo_cliente)
    print(f'El ID del cliente con correo "{correo_cliente}" es: {cliente_id}')

    # Iniciar la sesión de punto de venta
    sesion_pos_id = iniciar_sesion_pos(id_punto_de_venta)
    print(f'Sesión de punto de venta iniciada con ID: {sesion_pos_id}')

    # Productos a agregar a la orden (reemplazar con los IDs correctos)
    productos_a_agregar = [30, 18, 66, 67]

    if productos_a_agregar:
        # Crear la orden de punto de venta en la sesión existente
        orden_pos_id = crear_orden_pos(productos_a_agregar, sesion_pos_id, cliente_id)
        print(f'Orden de punto de venta creada con ID: {orden_pos_id}')
    else:
        print('La lista de productos está vacía.')

except Exception as e:
    print(f'Ocurrió un error: {e}')
