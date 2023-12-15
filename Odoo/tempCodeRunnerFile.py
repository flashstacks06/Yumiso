import xmlrpc.client

# Configura la URL de tu instancia Odoo y las credenciales de acceso
url = "http://137.184.86.135:8069"
db = "yumiso"
username = "info@inventoteca.com"
password = "Gr4nj3r04dm1n"

try:
    # Conecta con el servidor XML-RPC de Odoo
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})

    if uid:
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

        # Busca todas las órdenes de reparación para "Maquina 12" como producto a reparar
        search_domain = [('product_id.name', '=', 'Maquina 12')]
        repair_ids = models.execute_kw(db, uid, password, 'repair.order', 'search', [search_domain])

        # Verifica si encontró alguna orden de reparación
        if repair_ids:
            # Lee los detalles de las órdenes de reparación encontradas
            repair_orders = models.execute_kw(db, uid, password, 'repair.order', 'read', [repair_ids], {'fields': ['name', 'state', 'partner_id', 'product_id']})
            
            # Filtra las órdenes por el estado 'draft'
            draft_orders = [order for order in repair_orders if order['state'] == 'draft']

            if draft_orders:
                print(f"Se encontraron las siguientes órdenes de reparación en estado 'draft' para 'Maquina 12':")
                for order in draft_orders:
                    print(f"ID: {order['id']}, Referencia: {order['name']}, Estado: {order['state']}, Cliente: {order['partner_id'][1]}")
            else:
                print("No hay órdenes de reparación en estado 'draft' para 'Maquina 12'.")
        else:
            print("No se encontraron órdenes de reparación para 'Maquina 12'.")
    else:
        print("No se pudo autenticar en la instancia de Odoo.")

except Exception as e:
    print(f"Ha ocurrido un error: {e}")
