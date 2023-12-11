from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def decrypt_aes(encrypted_data, base64_key, base64_iv):
    key = base64.urlsafe_b64decode(base64_key)
    iv = base64.urlsafe_b64decode(base64_iv)
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

    return plaintext.decode('utf-8', errors='ignore')

# Ejemplo de uso
encrypted_message = 'C17Q3RLzgDonr0cPo81GeU+Sac7T1rBbCfToTs7Z66A=:YV3k/MjWmNQpIe1qwdGyqA=='
key = 'O1GqAK5igRS-BTYgSVLBvg=='  # La clave generada
iv = 'v0kiTpvIvAN1IoFQNyB1IQ=='  # El IV generado

# Divide el mensaje encriptado en dos partes
encrypted_user, encrypted_password = encrypted_message.split(':')

# Desencripta cada parte
decrypted_user = decrypt_aes(encrypted_user, key, iv)
decrypted_password = decrypt_aes(encrypted_password, key, iv)

print(f'{decrypted_user}:{decrypted_password}')


