# Chat Server con Pruebas Unitarias e Integración

Este proyecto implementa un servidor de chat simple utilizando **sockets**, **threading** y **pytest** para realizar pruebas unitarias e integración, con el fin de garantizar el correcto funcionamiento del sistema. Se han aplicado principios de **TDD (Test-Driven Development)** para el desarrollo de funcionalidades críticas, y se han implementado pruebas que validan el comportamiento de la aplicación.

## Requisitos

El proyecto utiliza las siguientes dependencias:

- `pytest`: Framework de pruebas unitarias para Python.
- `pytest-mock`: Complemento de `pytest` para simular objetos en las pruebas.
- `socket`: Biblioteca estándar de Python para manejar la comunicación de red.
- `threading`: Biblioteca estándar de Python para manejar hilos y operaciones concurrentes.

### Instalación

Para instalar las dependencias necesarias, ejecuta:

```bash
pip install pytest pytest-mock
