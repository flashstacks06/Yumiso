import xmlrpc.client
import sys
from urllib.parse import quote

def create_google_maps_link(lat, lng):
    encoded_coords = quote(f"{lat},{lng}")
    return f"https://www.google.com/maps?q={encoded_coords}"

def post_message_to_product(url, db, uid, password, product_id, message):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models.execute_kw(db, uid, password,
                      'product.product', 'message_post',
                      [product_id], {'body': message})

def find_product_id(url, db, uid, password, product_name):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    product_ids = models.execute_kw(db, uid, password,
                                    'product.product', 'search',
                                    [[['name', '=', product_name]]],
                                    {'limit': 1})
    return product_ids[0] if product_ids else None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <machine_number> <latitude> <longitude>")
        sys.exit(1)

    # Get the machine number, latitude and longitude from command line arguments
    machine_number = sys.argv[1]
    latitude = sys.argv[2]
    longitude = sys.argv[3]

    # Complete the product name with the machine number
    product_name = f"Maquina {machine_number}"

    # Configuration for Odoo
    url = 'http://137.184.86.135:8069/'
    db = 'yumiso'
    username = 'info@inventoteca.com'
    password = 'Gr4nj3r04dm1n'

    # Start session
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    # Find the product ID by product name
    product_id = find_product_id(url, db, uid, password, product_name)
    if not product_id:
        print(f"No product found with name {product_name}")
        sys.exit(1)

    # Generate the Google Maps link
    link = create_google_maps_link(latitude, longitude)

    # Post the message (Google Maps link) to the product
    post_message_to_product(url, db, uid, password, product_id, link)
    print(f"Mensaje posteado a {product_name}, link: {link}")
