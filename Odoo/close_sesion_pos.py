import xmlrpc.client
from datetime import datetime
from xmlrpc.client import Fault

# Datos de conexión a Odoo
url = 'http://137.184.117.41:8069'
db = 'yumiso'
username = 'cbernalestrella@gmail.com'
password = '12345678'

# Conexión al servidor de Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def cerrar_sesion_por_nombre_punto_de_venta(nombre_punto_de_venta, monto_pago):
    # Obtener la sesión abierta para el punto de venta
    domain = [('config_id.name', '=', nombre_punto_de_venta), ('state', '=', 'opened')]
    session_id = models.execute_kw(db, uid, password, 'pos.session', 'search', [domain], {'limit': 1})

    if session_id:
        # Crear el pago
        payment_data = {
            'payment_method_id': 1,  # ID del método de pago (Efectivo)
            'amount': monto_pago,
            'payment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'session_id': session_id[0],
            'pos_order_id': False,  # Establecer el campo pos_order_id en False
        }
        payment_id = models.execute_kw(db, uid, password, 'pos.payment', 'create', [payment_data])

        # Cerrar la sesión
        models.execute_kw(db, uid, password, 'pos.session', 'button_closing_control', [[session_id[0]]])
        print(f'Sesión de punto de venta cerrada con ID: {session_id[0]}, Pago realizado: {monto_pago}')

    else:
        print(f'No hay sesiones abiertas para el punto de venta: {nombre_punto_de_venta}')

# Nombre del punto de venta para cerrar la sesión (reemplazar con el nombre correcto)
nombre_punto_de_venta_para_cerrar = 'Maquina 21'

try:
    # Solicitar el monto de pago al usuario
    monto_pago = float(input('Ingrese el monto de pago para cerrar la sesión: '))

    # Cerrar la sesión de punto de venta con monto de pago
    cerrar_sesion_por_nombre_punto_de_venta(nombre_punto_de_venta_para_cerrar, monto_pago)
    print(f'Sesión de punto de venta cerrada para: {nombre_punto_de_venta_para_cerrar}, Pago total: {monto_pago}')

except ValueError:
    print('Ingrese un monto de pago válido.')

except Fault as e:
    print(f'Ocurrió un error: {e}')
