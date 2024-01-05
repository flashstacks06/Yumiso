import xmlrpc.client

def pay_order(url, db, username, password, order_id, payment_amount):
    # Información para la autenticación
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    print(uid)
    if uid is None:
        raise Exception("Autenticación fallida.")

    # Conexión al modelo pos.order
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Leer el monto total de la orden y el monto ya pagado
    order_data = models.execute_kw(db, uid, password,
                                   'pos.order', 'read',
                                   [order_id, ['amount_total', 'amount_paid']])
    
    if not order_data:
        raise Exception("Orden no encontrada.")
    
    order = order_data[0]
    amount_paid = order['amount_paid'] or 0.0
    amount_total = order['amount_total']
    
    # Actualizar el monto pagado
    new_amount_paid = amount_paid + payment_amount
    models.execute_kw(db, uid, password,
                      'pos.order', 'write',
                      [order_id, {'amount_paid': new_amount_paid}])
    
    # Si el nuevo monto pagado cubre el total, cambiar el estado a 'done'
    if new_amount_paid >= amount_total:
        models.execute_kw(db, uid, password,
                          'pos.order', 'write',
                          [order_id, {'state': 'done'}])

    return "Orden pagada y actualizada correctamente."

# Ejemplo de uso
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'
order_id = 61  # Reemplazar con el ID real de la orden
payment_amount = 2.0  # Reemplazar con el monto real a pagar

try:
    result = pay_order(url, db, username, password, order_id, payment_amount)
    print(result)
except Exception as e:
    print(f"Error: {e}")
