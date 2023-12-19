import xmlrpc.client

# Configuración de la conexión
url = 'http://137.184.86.135:8069/'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Nombre de los modelos
modelo_sesion = 'pos.session'
modelo_config = 'pos.config'
modelo_order = 'pos.order'
modelo_order_line = 'pos.order.line'
modelo_payment = 'account.bank.statement.line' # Replace with the correct model name for payments

def open_pos_session(nombre_punto_venta):
    pos_config_id = models.execute_kw(db, uid, password, modelo_config, 'search', [[['name', '=', nombre_punto_venta]]])[0]
    pos_session_id = models.execute_kw(db, uid, password, modelo_sesion, 'create', [{'config_id': pos_config_id}])
    return pos_session_id

def crear_orden_pos(product_ids_quantities, session_id, cliente_id):
    pos_order_data = {
        'partner_id': cliente_id,
        'session_id': session_id,
        'name': 'Semana 40',
        'amount_tax': 10.0,
        'amount_total': 0.0,
        'amount_paid': 0.0,
        'amount_return': 0.0,
        'lines': [],
    }

    total_amount = 0
    for product_id, quantity in product_ids_quantities.items():
        product_info = models.execute_kw(db, uid, password, 'product.product', 'read', [product_id], {'fields': ['list_price']})
        if product_info:
            subtotal = product_info[0]['list_price'] * quantity
            total_amount += subtotal
            pos_order_data['lines'].append((0, 0, {
                'product_id': product_info[0]['id'],
                'qty': quantity,
                'price_unit': product_info[0]['list_price'],
                'price_subtotal': subtotal,
                'price_subtotal_incl': subtotal,
            }))
    
    pos_order_data['amount_total'] = total_amount
    order_id = models.execute_kw(db, uid, password, modelo_order, 'create', [pos_order_data])
    return order_id

def register_cash_payment(order_id, amount):
    payment_method_id = 1 # Replace with your actual payment method ID

    # Fetch the associated bank statement for the POS session from the order
    order = models.execute_kw(db, uid, password, modelo_order, 'read', [order_id], {'fields': ['session_id']})
    print(order)
    session_id = order[0]['session_id'][0]  # session_id is a tuple (id, name), so we take the first element
    statement_ids = models.execute_kw(db, uid, password, modelo_sesion, 'read', [session_id], {'fields': ['statement_ids']})
    if not statement_ids[0]['statement_ids']:
        raise Exception("No bank statement associated with the POS session.")

    statement_id = statement_ids[0]['statement_ids'][0]  # Assuming the first statement is the one to be used

    # Create a payment
    models.execute_kw(db, uid, password, modelo_payment, 'create', [{
        'statement_id': statement_id,  # Using 'statement_id' instead of 'pos_statement_id'
        'amount': amount,
        'payment_method_id': payment_method_id,
        'ref': 'Payment Reference',  # Add a reference if needed
    }])
def cerrar_sesion_punto_venta(nombre_punto_venta, monto_contado):
    pos_config_ids = models.execute_kw(db, uid, password, modelo_config, 'search', [[['name', '=', nombre_punto_venta]]])
    if not pos_config_ids:
        print("No se encontró el punto de venta con ese nombre.")
        return
    session_ids = models.execute_kw(db, uid, password, modelo_sesion, 'search', [[['config_id', 'in', pos_config_ids], ['state', '!=', 'closed']]])
    if not session_ids:
        print("No se encontró una sesión activa para ese punto de venta.")
        return
    models.execute_kw(db, uid, password, modelo_sesion, 'write', [session_ids[0], {'cash_register_balance_end_real': monto_contado}])
    models.execute_kw(db, uid, password, modelo_sesion, 'action_pos_session_closing_control', [session_ids[0]])
    print(f"Sesión del punto de venta '{nombre_punto_venta}' cerrada correctamente con un monto contado de: ${monto_contado}")

# Main execution
def get_customer_id(email):
    customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', email]]])
    return customer_ids[0] if customer_ids else None

# Main execution
if __name__ == '__main__':
    nombre_punto_venta = input("Ingresa el nombre del punto de venta: ")
    monto_contado = float(input("Monto contado para cerrar la sesión: "))
    product_ids_quantities = eval(input("IDs de productos y cantidades (ejemplo: {1: 2, 3: 1}): "))

    pos_session_id = open_pos_session(nombre_punto_venta)

    # Fetch customer ID
    email_cliente = input("Ingrese el correo del cliente: ")
    cliente_id = get_customer_id(email_cliente)
    if cliente_id is None:
        print("Cliente no encontrado.")
        # Handle the case where the customer is not found
    else:
        order_id = crear_orden_pos(product_ids_quantities, pos_session_id, cliente_id)
        print(f"Orden de punto de venta creada con ID: {order_id}")

        total_amount_to_pay = monto_contado
        register_cash_payment(order_id, total_amount_to_pay)
        cerrar_sesion_punto_venta(nombre_punto_venta, monto_contado)