import xmlrpc.client
import sys
from datetime import datetime

# Argumentos de la línea de comandos
numero_maquina = sys.argv[1]  # Número de la máquina
correo_cliente = sys.argv[2]  # Correo electrónico del cliente
ids_productos = sys.argv[3:]  # IDs de los productos (separados por espacios)

# URL y credenciales para el servidor XML-RPC
url = 'http://137.184.86.135:8069'
db = 'yumiso'
username = 'info@inventoteca.com'
password = 'Gr4nj3r04dm1n'

# Autenticación
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Objeto para llamadas al servidor XML-RPC
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Función para buscar el ID del producto basado en el número de máquina
def buscar_producto(numero_maquina):
    productos = models.execute_kw(db, uid, password,
        'product.product', 'search_read',
        [[['name', 'ilike', f'Maquina {numero_maquina}']]],
        {'fields': ['id', 'name'], 'limit': 1})
    return productos[0] if productos else None

# Función para buscar el cliente basado en el correo electrónico
def buscar_cliente(correo_cliente):
    cliente = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['email', '=', correo_cliente]]],
        {'fields': ['id', 'email'], 'limit': 1})
    if cliente:
        return {'id': cliente[0]['id'], 'login': cliente[0]['email']}
    else:
        return None
# Crear la orden de reparación
# Crear la orden de reparación
def crear_orden_reparacion(producto_id, cliente_id, ids_productos):
    uom_id = 1  # ID de la Unidad de Medida 'Unidades'
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    location_id_linea = 8  # Asegúrate de que este ID de ubicación de origen exista en tu base de datos
    location_dest_id_linea = 15  # Asegúrate de que este ID de ubicación de destino exista en tu base de datos

    # Asignar un nombre y precio a las líneas de operación basado en el ID del producto
    operations = []
    for pid in map(int, ids_productos):
        # Recuperar precio del producto
        producto_info = models.execute_kw(db, uid, password,
            'product.product', 'search_read',
            [[['id', '=', pid]]],
            {'fields': ['list_price'], 'limit': 1})

        precio_producto = producto_info[0]['list_price'] if producto_info else 0

        operation = (0, 0, {
            'product_id': pid,
            'product_uom_qty': 1,
            'product_uom': uom_id,
            'price_unit': precio_producto,
            'name': f'Part ID {pid}',  # Descripción de la línea de reparación
            'location_id': location_id_linea,  # Ubicación de origen para la línea de reparación
            'location_dest_id': location_dest_id_linea,  # Ubicación de destino para la línea de reparación
        })
        operations.append(operation)
    
    orden_data = {
        'product_id': producto_id,
        'partner_id': cliente_id,
        'location_id': 8,  # Asumiendo que tienes una ubicación con ID 12
        'schedule_date': fecha_actual,
        'product_uom': uom_id,
        'operations': operations,
    }
    
    orden_id = models.execute_kw(db, uid, password, 'repair.order', 'create', [orden_data])
    return orden_id



# ... (El resto del código se mantiene igual)

# Función para confirmar la orden de reparación
def confirmar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_validate', [orden_id])

# Función para iniciar la orden de reparación
def iniciar_orden_reparacion(orden_id):
    models.execute_kw(db, uid, password, 'repair.order', 'action_repair_start', [orden_id])

# ... (resto del código anterior)

# Ejecutar el script
if __name__ == "__main__":
    producto = buscar_producto(numero_maquina)  # Esta llamada debería definir 'producto'
    
    if producto:  # Verificar si 'producto' está definido
        print(producto)
        cliente_info = buscar_cliente(correo_cliente)  # Esta llamada debería definir 'cliente_info'

        if cliente_info:  # Verificar si 'cliente_info' está definido
            print(cliente_info)
            cliente_id = cliente_info['id']
            producto_id = producto['id']
            ids_productos = [int(pid) for pid in ids_productos]  # Convertir a enteros

            orden_id = crear_orden_reparacion(producto_id, cliente_id, ids_productos)
            print(f"Orden de reparación creada con ID: {orden_id}")

            try:
                # Confirmar la orden de reparación
                confirmar_orden_reparacion(orden_id)
                print(f"Orden de reparación confirmada con ID: {orden_id}")
            except xmlrpc.client.Fault as e:
                print(f"No se pudo confirmar la orden de reparación: {e}")

            try:
                # Iniciar la orden de reparación
                iniciar_orden_reparacion(orden_id)
                print(f"Reparación iniciada para la orden con ID: {orden_id}")
            except xmlrpc.client.Fault as e:
                print(f"No se pudo iniciar la reparación: {e}")

        else:
            print("No se pudo encontrar el cliente con el correo proporcionado.")
    else:
        print("No se pudo encontrar el producto con el número de máquina proporcionado.")
