import socket
import threading

#____________________________________FUNCIONES_________________________________________
def recibir_mensajes(cliente_socket):
    '''Función para recibir mensajes del servidor'''

    while True:
        try:
            mensaje = cliente_socket.recv(1024)
            if mensaje:
                print(f"Mensaje recibido: {mensaje.decode('utf-8')}")
            else:
                break
        except:
            print('Algo salio mal')
            break

def enviar_mensajes(cliente_socket):
    '''Función para enviar mensajes al servidor'''

    while True:
        mensaje = input()  # input mensajes del usuario
        cliente_socket.send(mensaje.encode('utf-8'))  # codifica y envia mensajes al servidor

#_________________________________SOCKET CLIENT__________________________________________
def client_socket():
    host = 'localhost'
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, 12345))  # Conectar al servidor
    print("Conectado al servidor")
    return cliente_socket

if __name__ == "__main__":
    # Crear hilos para recibir y enviar mensajes
    CLIENT_SOCKET = client_socket()
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(CLIENT_SOCKET,))
    hilo_recibir.start()

    enviar_mensajes(CLIENT_SOCKET)