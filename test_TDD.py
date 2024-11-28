from client import enviar_mensajes
import pytest


#__________________________SERVER_________________________________
def test_enviar_mensaje_vacio(mocker):
    # red
    cliente_socket = mocker.Mock()

    # verifica que la función lance un ValueError con el mensaje específico
    with pytest.raises(ValueError, match="Mensaje vacío no permitido"):
        enviar_mensajes(cliente_socket, "")

    # green
def enviar_mensajes(cliente_socket, mensaje):
    if not mensaje.strip(): # elimina caracteres en blanco
        raise ValueError("Mensaje vacío no permitido")
    # enviamos al cliente (simulado aquí como cliente_socket)
    cliente_socket.send(mensaje.encode('utf-8'))

