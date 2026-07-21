"""Tests unitarios para connection.py del SDK QScout.

Valida que Connection es un transporte UART puro (Opción A):
- Sin gestión de Order ID.
- Sin lógica de protocolo.
- Solo envío/recepción de bytes.

Usa unittest.mock para simular pyserial.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Añadir src al path para importar connection.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from qscout.connection import Connection


class TestArchitectureOptionA(unittest.TestCase):
    """Verifica que Connection cumple la Opción A (transporte puro)."""

    def test_no_order_manager_attribute(self):
        """Verifica que Connection no tiene atributo _order."""
        conn = Connection()
        self.assertFalse(hasattr(conn, '_order'))

    def test_no_order_manager_import(self):
        """Verifica que Connection no importa OrderManager."""
        # Verificar que el módulo connection no tiene OrderManager en su namespace
        import qscout.connection as conn_module
        self.assertFalse(hasattr(conn_module, 'OrderManager'))

    def test_no_next_order_id_method(self):
        """Verifica que Connection no tiene método next_order_id()."""
        conn = Connection()
        self.assertFalse(hasattr(conn, 'next_order_id'))


class TestConnectionInitialization(unittest.TestCase):
    """Tests para la inicialización de Connection."""

    def test_default_parameters(self):
        """Verifica que los parámetros por defecto son correctos."""
        conn = Connection()
        self.assertEqual(conn._port_name, '/dev/ttyUSB0')
        self.assertEqual(conn._baudrate, 115200)
        self.assertEqual(conn._timeout, 0.5)
        self.assertIsNone(conn._serial)
        self.assertEqual(conn._rx_buffer, bytearray())

    def test_custom_parameters(self):
        """Verifica que los parámetros personalizados se guardan correctamente."""
        conn = Connection(port='/dev/ttyACM0', baudrate=9600, timeout=1.0)
        self.assertEqual(conn._port_name, '/dev/ttyACM0')
        self.assertEqual(conn._baudrate, 9600)
        self.assertEqual(conn._timeout, 1.0)

    def test_no_protocol_objects_created(self):
        """Verifica que no se crean objetos de protocolo al inicializar."""
        conn = Connection()
        # Connection no debe tener atributos relacionados con protocolo (ej: OrderManager)
        self.assertFalse(hasattr(conn, '_order'))
        self.assertFalse(hasattr(conn, '_order_manager'))


class TestOpenClose(unittest.TestCase):
    """Tests para open() y close()."""

    @patch('serial.Serial')
    def test_open(self, mock_serial):
        """Verifica que open() configura correctamente el puerto serial."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.reset_input_buffer = Mock()
        mock_serial.return_value = mock_serial_instance

        conn = Connection()
        conn.open()

        # Verificar que serial.Serial se llamó con los parámetros correctos
        mock_serial.assert_called_once_with(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.5,
            write_timeout=0.5
        )
        self.assertTrue(conn.is_open)
        mock_serial_instance.reset_input_buffer.assert_called_once()

    @patch('serial.Serial')
    def test_close(self, mock_serial):
        """Verifica que close() cierra el puerto serial."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.close = Mock()
        mock_serial.return_value = mock_serial_instance

        conn = Connection()
        conn.open()
        conn.close()

        # Verificar que serial.close() fue llamado
        mock_serial_instance.close.assert_called_once()
        self.assertFalse(conn.is_open)
        self.assertIsNone(conn._serial)

    def test_close_when_not_open(self):
        """Verifica que close() no falla si el puerto no está abierto."""
        conn = Connection()
        conn.close()  # No debe lanzar excepción
        self.assertFalse(conn.is_open)


class TestSend(unittest.TestCase):
    """Tests para send()."""

    @patch('serial.Serial')
    def test_send(self, mock_serial):
        """Verifica que send() envía bytes correctamente."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.write = Mock()
        mock_serial_instance.flush = Mock()
        mock_serial.return_value = mock_serial_instance

        conn = Connection()
        conn.open()
        test_packet = b"RB_TEST_PACKET"
        conn.send(test_packet)

        # Verificar que serial.write() recibió el paquete exacto
        mock_serial_instance.write.assert_called_once_with(test_packet)
        mock_serial_instance.flush.assert_called_once()

    @patch('serial.Serial')
    def test_send_when_not_open(self, mock_serial):
        """Verifica que send() lanza ConnectionError si el puerto no está abierto."""
        conn = Connection()
        with self.assertRaises(ConnectionError):
            conn.send(b"test")

    @patch('serial.Serial')
    def test_send_disconnection_handling(self, mock_serial):
        """Verifica que send() maneja desconexiones."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.write = Mock(side_effect=OSError("Disconnected"))
        mock_serial.return_value = mock_serial_instance

        conn = Connection()
        conn.open()
        with self.assertRaises(ConnectionError):
            conn.send(b"test")
        # Verificar que _serial se establece a None tras la desconexión
        self.assertIsNone(conn._serial)


class TestReceive(unittest.TestCase):
    """Tests para receive()."""

    @patch('serial.Serial')
    @patch('time.monotonic')
    def test_receive_success(self, mock_monotonic, mock_serial):
        """Verifica que receive() devuelve un paquete válido."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.in_waiting = 10
        mock_serial_instance.read = Mock(return_value=b"RB_PACKET")
        mock_serial.return_value = mock_serial_instance
        mock_monotonic.side_effect = [0.0, 0.1]  # Simular tiempo dentro del timeout

        conn = Connection()
        conn.open()
        result = conn.receive(timeout=0.5)

        # Verificar que se leyó el buffer
        mock_serial_instance.read.assert_called_once_with(10)
        self.assertIsNotNone(result)

    @patch('serial.Serial')
    @patch('time.monotonic')
    def test_receive_timeout(self, mock_monotonic, mock_serial):
        """Verifica que receive() devuelve None tras timeout."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.in_waiting = 0
        mock_serial.return_value = mock_serial_instance
        mock_monotonic.side_effect = [0.0, 0.6]  # Simular timeout

        conn = Connection()
        conn.open()
        result = conn.receive(timeout=0.5)

        self.assertIsNone(result)

    @patch('serial.Serial')
    def test_receive_when_not_open(self, mock_serial):
        """Verifica que receive() devuelve None si el puerto no está abierto."""
        conn = Connection()
        result = conn.receive()
        self.assertIsNone(result)


class TestSendReceive(unittest.TestCase):
    """Tests para send_receive()."""

    @patch('serial.Serial')
    @patch('time.monotonic')
    def test_send_receive(self, mock_monotonic, mock_serial):
        """Verifica que send_receive() envía y recibe correctamente."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.write = Mock()
        mock_serial_instance.flush = Mock()
        mock_serial_instance.in_waiting = 10
        mock_serial_instance.read = Mock(return_value=b"RB_RESPONSE")
        mock_serial.return_value = mock_serial_instance
        mock_monotonic.side_effect = [0.0, 0.1]

        conn = Connection()
        conn.open()
        test_packet = b"RB_REQUEST"
        result = conn.send_receive(test_packet, timeout=0.5)

        # Verificar que se envió el paquete
        mock_serial_instance.write.assert_called_once_with(test_packet)
        # Verificar que se recibió la respuesta
        self.assertIsNotNone(result)


class TestFlush(unittest.TestCase):
    """Tests para flush()."""

    @patch('serial.Serial')
    def test_flush(self, mock_serial):
        """Verifica que flush() limpia los buffers."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial_instance.reset_input_buffer = Mock()
        mock_serial.return_value = mock_serial_instance

        conn = Connection()
        conn.open()
        conn._rx_buffer = bytearray(b"test")
        conn.flush()

        # Verificar que se limpiaron los buffers
        mock_serial_instance.reset_input_buffer.assert_called_once()
        self.assertEqual(conn._rx_buffer, bytearray())

    def test_flush_when_not_open(self):
        """Verifica que flush() no falla si el puerto no está abierto."""
        conn = Connection()
        conn.flush()  # No debe lanzar excepción


class TestListPorts(unittest.TestCase):
    """Tests para list_ports()."""

    @patch('serial.tools.list_ports.comports')
    def test_list_ports(self, mock_comports):
        """Verifica que list_ports() devuelve la lista de puertos."""
        mock_port1 = Mock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port2 = Mock()
        mock_port2.device = '/dev/ttyACM0'
        mock_comports.return_value = [mock_port1, mock_port2]

        ports = Connection.list_ports()
        self.assertEqual(ports, ['/dev/ttyUSB0', '/dev/ttyACM0'])


class TestFindQScout(unittest.TestCase):
    """Tests para find_qscout()."""

    @patch('serial.tools.list_ports.comports')
    def test_find_qscout_by_vid_pid(self, mock_comports):
        """Verifica que find_qscout() detecta el robot por VID:PID."""
        mock_port = Mock()
        mock_port.device = '/dev/ttyUSB0'
        mock_port.vid = 0x1A86
        mock_port.pid = 0x7523
        mock_comports.return_value = [mock_port]

        result = Connection.find_qscout()
        self.assertEqual(result, '/dev/ttyUSB0')

    @patch('serial.tools.list_ports.comports')
    def test_find_qscout_by_description(self, mock_comports):
        """Verifica que find_qscout() detecta el robot por descripción."""
        mock_port = Mock()
        mock_port.device = '/dev/ttyACM0'
        mock_port.description = 'CH340 USB-Serial'
        mock_comports.return_value = [mock_port]

        result = Connection.find_qscout()
        self.assertEqual(result, '/dev/ttyACM0')

    @patch('serial.tools.list_ports.comports')
    def test_find_qscout_not_found(self, mock_comports):
        """Verifica que find_qscout() devuelve None si no se encuentra el robot."""
        mock_port = Mock()
        mock_port.device = '/dev/ttyS0'
        mock_port.vid = 0x1234
        mock_port.pid = 0x5678
        mock_port.description = 'Generic Serial'
        mock_comports.return_value = [mock_port]

        result = Connection.find_qscout()
        self.assertIsNone(result)

    @patch('serial.tools.list_ports.comports')
    def test_find_qscout_no_ports(self, mock_comports):
        """Verifica que find_qscout() devuelve None si no hay puertos."""
        mock_comports.return_value = []

        result = Connection.find_qscout()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
