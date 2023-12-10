from cryptography.fernet import Fernet
import getpass
import paho.mqtt.client as mqtt

def encrypt_data(cipher, data):
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def on_publish(client, userdata, mid):
    print("Datos encriptados publicados en el tópico")
    client.disconnect()  # Desconectar después de publicar el mensaje

if __name__ == "__main__":
    # Clave secreta que deberías guardar de forma segura
    secret_key_str = 'PzvGHUWbE3GNHMgGgU7G4TmxREf99oIbQ7_sGmqo040='

    # Convierte la cadena de clave secreta a bytes
    secret_key = secret_key_str.encode()

    # Inicializa el cifrador con la clave secreta
    cipher = Fernet(secret_key)

    # Ingresa el nombre de usuario y la contraseña desde la terminal
    user = input("Ingrese el nombre de usuario: ")
    password = getpass.getpass("Ingrese la contraseña: ")

    # Concatena el usuario y la contraseña en el formato requerido
    user_password_data = f"{user}:{password}"

    # Encripta los datos combinados de usuario y contraseña
    encrypted_data = encrypt_data(cipher, user_password_data)

    # Configura el cliente MQTT
    client = mqtt.Client()
    client.on_publish = on_publish

    # Conéctate al broker MQTT
    client.connect("137.184.86.135", 1883, 60)

    # Inicia el bucle en segundo plano
    client.loop_start()

    # Publica los datos encriptados en el tópico "usuarios/<correo>"
    topic = f"users/{user}"
    client.publish(topic, encrypted_data)

    # Espera a que se publique el mensaje (puedes ajustar esto según tus necesidades)
    client.loop_stop()

    # Desconecta explícitamente después de detener el bucle
    client.disconnect()
