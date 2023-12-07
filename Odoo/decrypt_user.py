from cryptography.fernet import Fernet
import getpass

def initialize_cipher(key):
    return Fernet(key)

def decrypt_data(cipher, encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

if __name__ == "__main__":
    # Ingresa la clave secreta desde la terminal
    secret_key = input("Ingrese la clave secreta: ")

    # Inicializa el cifrador con la clave secreta
    cipher = initialize_cipher(secret_key)

    # Ingresa los datos encriptados desde la terminal
    encrypted_data = input("Ingrese los datos encriptados: ")

    # Descifra los datos
    decrypted_data = decrypt_data(cipher, encrypted_data)

    print(f"Datos descifrados: {decrypted_data}")
