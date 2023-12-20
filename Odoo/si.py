import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import sys

# Clave y IV predefinidos
key = 'O1GqAK5igRS-BTYgSVLBvg=='
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='

# Funciones de Desencriptación y Quitar Relleno
def decrypt_aes(encrypted_data, base64_key, base64_iv):
    key = base64.urlsafe_b64decode(base64_key)
    iv = base64.urlsafe_b64decode(base64_iv)
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

    return plaintext

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data

# Datos encriptados proporcionados como argumento de línea de comandos
if len(sys.argv) != 2:
    print("Uso: python decrypt_data.py <datos_encriptados>")
    sys.exit(1)

encrypted_data = sys.argv[1]

try:
    decrypted_data = len(unpad(decrypt_aes(encrypted_data, key, iv)).decode('utf-8').strip())
    print(f'Datos desencriptados: {decrypted_data}')
except Exception as e:
    print(f'Error al desencriptar los datos: {e}')
