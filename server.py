import socket
import threading

#_____________________________FUNTIONS_________________________________________
def manejar_cliente(cliente_socket):
    """Función para manejar las conexiones de los clientes."""
    while True:
        try:
            mensaje = cliente_socket.recv(1024)
            if mensaje:
                print(f"Mensaje recibido: {mensaje.decode('utf-8')}")
                broadcast(mensaje, cliente_socket)
            else:
                raise ConnectionError("Cliente desconectado")
        except (ConnectionError, OSError):
            print("Desconexión detectada")
            eliminar_cliente(cliente_socket)
            break

def broadcast(mensaje, cliente_socket):
    """Función para enviar mensajes a todos los clientes."""
    for cliente in list(clientes):  # Itera sobre una copia de la lista
        if cliente != cliente_socket:
            try:
                cliente.send(mensaje)  # Enviar mensaje a otro cliente
            except (BrokenPipeError, OSError):
                print("Cliente desconectado detectado durante el broadcast.")
                eliminar_cliente(cliente)

def eliminar_cliente(cliente_socket):
    """Función para eliminar un cliente de la lista."""
    if cliente_socket in clientes:
        clientes.remove(cliente_socket)
        try:
            cliente_socket.close()
        except OSError:
            pass  # Ignora errores si el socket ya está cerrado

#_______________________________Socket server__________________________________
# configuracion servidor
def server_socket():
    host = 'localhost'
    port = 12345
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, port))  # Vincular el socket a la dirección y puerto
    servidor_socket.listen(5)  # Escuchar hasta 5 conexiones entrantes
    print(f"Servidor escuchando en el puerto {port}")
    return servidor_socket

if __name__ == "__main__":
    servidor_socket = server_socket()

    clientes = []  # Lista para almacenar los sockets de los clientes
    # Aceptar conexiones entrantes
    while True:
        cliente_socket, direccion = servidor_socket.accept()
        clientes.append(cliente_socket)
        print(f"Conexión aceptada de {direccion}")
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente_socket,))
        hilo_cliente.start()