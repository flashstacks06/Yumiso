import base64
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Verificación de argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Uso: python script.py <mensaje_encriptado>")
    sys.exit(1)

# Datos encriptados desde argumentos de la línea de comandos
encrypted_message = sys.argv[1]

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

# Desencriptar y quitar relleno del mensaje
try:
    decrypted_message = unpad(decrypt_aes(encrypted_message, key, iv)).decode('utf-8').strip()
    print(decrypted_message)
except Exception as e:
    print(f'Error al desencriptar: {e}')
