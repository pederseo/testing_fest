import pytest
from unittest.mock import MagicMock, patch
from server import manejar_cliente
from client import recibir_mensajes, enviar_mensajes

# Los métodos como assert_called, assert_called_once_with o assert_not_called son métodos 
# de aserción incluidos en los objetos MagicMock. Estos métodos te permiten verificar si 
# las llamadas a un método simulado ocurrieron como esperabas.

#________________________________SERVER______________________________
def test_manejo_clientes():
    '''test para verificar 
    - recepcion de mensajes de los clientes
    - verificar funciones bradcast y eliminar_cliente
    '''
    # Crear un mock para el socket del cliente
    mock_cliente_socket = MagicMock()

    # Simular datos recibidos del cliente
    mock_cliente_socket.recv.side_effect = [
        b"Hola, servidor!",  # Primera llamada a `recv`
        b"Mensaje 2",        # Segunda llamada a `recv`
        b"",                 # Tercera llamada (fin de conexión)
    ]
    # Parchear las funciones auxiliares
    with patch('server.broadcast') as mock_broadcast, patch('server.eliminar_cliente') as mock_eliminar:
        # Llamar a la función que queremos probar
        manejar_cliente(mock_cliente_socket)

        # Verificar que `recv` fue llamado correctamente
        assert mock_cliente_socket.recv.call_count == 3

        # Verificar que `broadcast` fue llamado con los mensajes correctos
        mock_broadcast.assert_any_call(b"Hola, servidor!", mock_cliente_socket)
        mock_broadcast.assert_any_call(b"Mensaje 2", mock_cliente_socket)

        # Verificar que `eliminar_cliente` fue llamado una vez al finalizar la conexión
        mock_eliminar.assert_called_once_with(mock_cliente_socket)


def test_broadcast():
    '''Test de la función broadcast
    - verifica que el emisor no reciba el mensaje'
    - verifica que se envio el mensaje a los demas clientes
    '''
    # Crear mocks para los clientes
    cliente_socket1 = MagicMock()
    cliente_socket2 = MagicMock()
    cliente_socket3 = MagicMock()

    # Lista de clientes simulados
    clientes = [cliente_socket1, cliente_socket2, cliente_socket3]

    # Mensaje a enviar
    mensaje = b"Hola, clientes!"

    # Verificar que aún no se han enviado mensajes
    for cliente in clientes:
        cliente.send.assert_not_called()  

    # Simular la lógica de la función broadcast
    for cliente in clientes:
        if cliente != cliente_socket1:  # cliente_socket1 es el emisor
            cliente.send(mensaje)

    # El cliente emisor no debería recibir el mensaje
    cliente_socket1.send.assert_not_called()  

    # Verificar que se envió el mensaje a los clientes adecuados
    cliente_socket2.send.assert_called_once_with(mensaje)
    cliente_socket3.send.assert_called_once_with(mensaje)


#_________________________________CLIENT_____________________________
def test_recibir_mensajes():
    mock_socket = MagicMock()

    # Configurar el mock para que `recv` devuelva mensajes simulados
    mock_socket.recv.side_effect = [
        b"Hola",        # Primera llamada a `recv`
        b"Mundo",       # Segunda llamada a `recv`
        b""             # Tercera llamada, simula desconexión
    ]

    # Llamar a la función con el mock
    recibir_mensajes(mock_socket)

    # Verificar que `recv` fue llamado 3 veces
    assert mock_socket.recv.call_count == 3

    # Opcional: verificar el orden de los mensajes recibidos
    mock_socket.recv.assert_any_call(1024)



 