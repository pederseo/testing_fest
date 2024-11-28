import socket
import threading
import time

#el servidor debe estar corriendo para que funcione

def test_multiples_clientes():
    '''test para verificar multiples clientes y mensajes'''
    host, port = 'localhost', 12345
    mensajes = []

    def cliente_envia_recibe(mensaje):
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        cliente_socket.send(mensaje.encode('utf-8'))
        recibido = cliente_socket.recv(1024).decode('utf-8')
        mensajes.append(recibido)
        cliente_socket.close()

    # Crear dos clientes que envíen mensajes
    hilo1 = threading.Thread(target=cliente_envia_recibe, args=("Hola desde cliente 1",))
    hilo2 = threading.Thread(target=cliente_envia_recibe, args=("Hola desde cliente 2",))

    hilo1.start()
    hilo2.start()
    hilo1.join()
    hilo2.join()

    # Verificar los mensajes recibidos
    assert "Hola desde cliente 1" in mensajes
    assert "Hola desde cliente 2" in mensajes


def test_desconexion_cliente():
    """test desconexión repentina de un cliente."""
    host, port = 'localhost', 12345
    mensajes = []

    def cliente_desconecta():
        """Simula un cliente que envía un mensaje y luego se desconecta."""
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        cliente_socket.send(b"Mensaje antes de desconexion")
        time.sleep(0.5)  # Breve retraso para asegurar que el servidor procese el mensaje
        cliente_socket.close()  # Simular desconexión abrupta

    def cliente_activo():
        """Simula un cliente que sigue activo después de la desconexión de otro cliente."""
        time.sleep(1)  # Esperar a que el servidor maneje la desconexión
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        cliente_socket.send(b"Cliente aun activo")
        recibido = cliente_socket.recv(1024).decode('utf-8')
        mensajes.append(recibido)
        cliente_socket.close()

    # Iniciar cliente que se desconecta y otro que permanece activo
    hilo_desconecta = threading.Thread(target=cliente_desconecta)
    hilo_activo = threading.Thread(target=cliente_activo)

    hilo_desconecta.start()
    hilo_activo.start()

    hilo_desconecta.join()
    hilo_activo.join()

    # Verificar que el cliente activo sigue recibiendo mensajes
    assert "Cliente aun activo" in mensajes
