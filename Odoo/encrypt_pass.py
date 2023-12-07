from cryptography.fernet import Fernet

def encrypt_data(cipher, data):
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

if __name__ == "__main__":
    # Clave secreta que deberías guardar de forma segura
    secret_key_str = 'PzvGHUWbE3GNHMgGgU7G4TmxREf99oIbQ7_sGmqo040='

    # Convierte la cadena de clave secreta a bytes
    secret_key = secret_key_str.encode()

    # Inicializa el cifrador con la clave secreta
    cipher = Fernet(secret_key)

    # Ingresa el nombre de usuario y la contraseña desde la terminal
    user = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")

    # Concatena el usuario y la contraseña en el formato requerido
    user_password_data = f"{user}:{password}"

    # Encripta los datos combinados de usuario y contraseña
    encrypted_data = encrypt_data(cipher, user_password_data)

    print(f"Datos encriptados: {encrypted_data}")
