"""QScout SDK exceptions.

Jerarquía de excepciones para el SDK Robobloq Q-Scout.
"""


class QScoutError(Exception):
    """Error base del SDK."""
    pass


class QScoutProtocolError(QScoutError):
    """Error relacionado con el protocolo RB.
    
    Ejemplos:
    - Checksum inválido.
    - Paquete mal formado.
    - Datos incompatibles con el protocolo.
    """
    pass


class QScoutChecksumError(QScoutProtocolError):
    """Error específico de checksum inválido en un paquete RB."""
    pass


class QScoutConnectionError(QScoutError):
    """Error relacionado con la conexión UART.
    
    Ejemplos:
    - Puerto no encontrado.
    - Desconexión inesperada.
    - Fallo de comunicación serial.
    """
    pass
