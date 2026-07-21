"""Tests unitarios para protocol.py del SDK QScout.

Valida:
- RBPacket (Value Object).
- Checksum (sum_check, validate_checksum).
- Construcción y parseo de paquetes RB.
- OrderManager.
- Builders y parsers críticos.
"""

import unittest
from qscout.protocol import (
    HEADER_RB,
    HEADER_LEN,
    MIN_PACKET_SIZE,
    sum_check,
    validate_checksum,
    build_packet,
    parse_packet,
    extract_packets,
    RBPacket,
    OrderManager,
    Action,
    Port,
    build_set_led,
    build_set_motor,
    build_set_move,
    build_get_ultrasonic,
    parse_ultrasonic,
    parse_device_info,
    parse_voltage,
    parse_line_value,
)
from qscout.exceptions import QScoutProtocolError


class TestRBPacket(unittest.TestCase):
    """Tests para la clase RBPacket."""

    def test_creation(self):
        """Verifica la creación de un RBPacket con valores básicos."""
        packet = RBPacket(order_id=10, action=0x10, payload=b'\x01\x02\x03')
        self.assertEqual(packet.order_id, 10)
        self.assertEqual(packet.action, 0x10)
        self.assertEqual(packet.payload, b'\x01\x02\x03')

    def test_creation_empty_payload(self):
        """Verifica la creación de un RBPacket con payload vacío."""
        packet = RBPacket(order_id=5, action=0x01, payload=b'')
        self.assertEqual(packet.order_id, 5)
        self.assertEqual(packet.action, 0x01)
        self.assertEqual(packet.payload, b'')

    def test_to_bytes_empty_payload(self):
        """Verifica que to_bytes() genera un paquete válido con payload vacío."""
        packet = RBPacket(order_id=0, action=0x01, payload=b'')
        raw = packet.to_bytes()
        # Header (2B) + length (1B) + order_id (1B) + action (1B) + checksum (1B) = 6B
        self.assertEqual(len(raw), 6)
        self.assertEqual(raw[:2], HEADER_RB)
        self.assertEqual(raw[2], 6)  # Length
        self.assertEqual(raw[3], 0)  # Order ID
        self.assertEqual(raw[4], 0x01)  # Action
        # Verificar checksum
        self.assertEqual(raw[-1], sum_check(raw[:-1]) % 256)

    def test_to_bytes_with_payload(self):
        """Verifica que to_bytes() genera un paquete válido con payload."""
        packet = RBPacket(order_id=1, action=0x10, payload=b'\xFC\xFF\x00\x00')
        raw = packet.to_bytes()
        # Header (2B) + length (1B) + order_id (1B) + action (1B) + payload (4B) + checksum (1B) = 10B
        self.assertEqual(len(raw), 10)
        self.assertEqual(raw[:2], HEADER_RB)
        self.assertEqual(raw[2], 10)  # Length
        self.assertEqual(raw[3], 1)  # Order ID
        self.assertEqual(raw[4], 0x10)  # Action
        self.assertEqual(raw[5:9], b'\xFC\xFF\x00\x00')  # Payload
        # Verificar checksum
        self.assertEqual(raw[-1], sum_check(raw[:-1]) % 256)

    def test_from_bytes(self):
        """Verifica que from_bytes() reconstruye correctamente un RBPacket."""
        # Paquete ejemplo: RB 0A 01 10 FC FF 00 00 AA (SET_LED)
        raw_packet = bytes([0x52, 0x42, 0x0A, 0x01, 0x10, 0xFC, 0xFF, 0x00, 0x00, 0xAA])
        packet = RBPacket.from_bytes(raw_packet)
        self.assertEqual(packet.order_id, 1)
        self.assertEqual(packet.action, 0x10)
        self.assertEqual(packet.payload, b'\xFC\xFF\x00\x00')

    def test_from_bytes_minimal(self):
        """Verifica from_bytes() con un paquete mínimo (sin payload)."""
        # Paquete mínimo: RB 06 00 01 9B (GET_DEVICE_INFO)
        raw_packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        packet = RBPacket.from_bytes(raw_packet)
        self.assertEqual(packet.order_id, 0)
        self.assertEqual(packet.action, 0x01)
        self.assertEqual(packet.payload, b'')

    def test_equality(self):
        """Verifica la comparación de objetos RBPacket."""
        packet1 = RBPacket(order_id=1, action=0x10, payload=b'\x01\x02')
        packet2 = RBPacket(order_id=1, action=0x10, payload=b'\x01\x02')
        packet3 = RBPacket(order_id=2, action=0x10, payload=b'\x01\x02')
        self.assertEqual(packet1, packet2)
        self.assertNotEqual(packet1, packet3)

    def test_repr(self):
        """Verifica la representación string de RBPacket."""
        packet = RBPacket(order_id=1, action=0x10, payload=b'\xFC\xFF')
        repr_str = repr(packet)
        self.assertIn("RBPacket", repr_str)
        self.assertIn("order_id=1", repr_str)
        self.assertIn("action=0x10", repr_str)

    def test_size_property(self):
        """Verifica la propiedad size de RBPacket."""
        packet = RBPacket(order_id=1, action=0x10, payload=b'\x01\x02\x03')
        self.assertEqual(packet.size, 6 + 3)  # 6 (header + metadata) + 3 (payload)


class TestChecksum(unittest.TestCase):
    """Tests para funciones de checksum."""

    def test_sum_check_basic(self):
        """Verifica sum_check() con datos simples."""
        data = bytes([0x52, 0x42, 0x06, 0x00, 0x01])
        checksum = sum_check(data)
        self.assertEqual(checksum, (0x52 + 0x42 + 0x06 + 0x00 + 0x01) % 256)

    def test_sum_check_empty(self):
        """Verifica sum_check() con datos vacíos."""
        self.assertEqual(sum_check(b''), 0)

    def test_sum_check_overflow(self):
        """Verifica sum_check() con valores que desbordan uint8."""
        data = bytes([0xFF, 0xFF, 0xFF])
        self.assertEqual(sum_check(data), (0xFF + 0xFF + 0xFF) % 256)

    def test_validate_checksum_valid(self):
        """Verifica validate_checksum() con un paquete válido."""
        # Paquete válido: RB 06 00 01 9B (sum = 0x52 + 0x42 + 0x06 + 0x00 + 0x01 = 0x9B)
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        self.assertTrue(validate_checksum(packet))

    def test_validate_checksum_invalid(self):
        """Verifica validate_checksum() con un paquete inválido."""
        # Paquete inválido: checksum incorrecto
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x00])
        self.assertFalse(validate_checksum(packet))

    def test_validate_checksum_too_short(self):
        """Verifica validate_checksum() con un paquete demasiado corto."""
        packet = bytes([0x52, 0x42])  # Solo header
        self.assertFalse(validate_checksum(packet))


class TestBuildPacket(unittest.TestCase):
    """Tests para build_packet()."""

    def test_build_packet_empty_payload(self):
        """Verifica build_packet() con payload vacío."""
        packet = build_packet(order_id=0, action=0x01, payload=b'')
        self.assertEqual(len(packet), 6)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[2], 6)  # Length
        self.assertEqual(packet[3], 0)  # Order ID
        self.assertEqual(packet[4], 0x01)  # Action
        self.assertTrue(validate_checksum(packet))

    def test_build_packet_with_payload(self):
        """Verifica build_packet() con payload."""
        packet = build_packet(order_id=10, action=0x10, payload=b'\xFC\xFF\x00\x00')
        self.assertEqual(len(packet), 10)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[2], 10)  # Length
        self.assertEqual(packet[3], 10)  # Order ID
        self.assertEqual(packet[4], 0x10)  # Action
        self.assertEqual(packet[5:9], b'\xFC\xFF\x00\x00')  # Payload
        self.assertTrue(validate_checksum(packet))

    def test_build_packet_invalid_order_id(self):
        """Verifica build_packet() con order_id inválido."""
        with self.assertRaises(ValueError):
            build_packet(order_id=255, action=0x01, payload=b'')
        with self.assertRaises(ValueError):
            build_packet(order_id=-1, action=0x01, payload=b'')

    def test_build_packet_invalid_action(self):
        """Verifica build_packet() con action inválido."""
        with self.assertRaises(ValueError):
            build_packet(order_id=1, action=256, payload=b'')
        with self.assertRaises(ValueError):
            build_packet(order_id=1, action=-1, payload=b'')


class TestParsePacket(unittest.TestCase):
    """Tests para parse_packet()."""

    def test_parse_packet_valid(self):
        """Verifica parse_packet() con un paquete válido."""
        packet = bytes([0x52, 0x42, 0x0A, 0x01, 0x10, 0xFC, 0xFF, 0x00, 0x00, 0xAA])
        order_id, action, payload = parse_packet(packet)
        self.assertEqual(order_id, 1)
        self.assertEqual(action, 0x10)
        self.assertEqual(payload, b'\xFC\xFF\x00\x00')

    def test_parse_packet_too_short(self):
        """Verifica parse_packet() con un paquete demasiado corto."""
        packet = bytes([0x52, 0x42])  # Solo header
        with self.assertRaises(QScoutProtocolError):
            parse_packet(packet)

    def test_parse_packet_invalid_header(self):
        """Verifica parse_packet() con header inválido."""
        packet = bytes([0x00, 0x00, 0x06, 0x00, 0x01, 0x9B])
        with self.assertRaises(QScoutProtocolError):
            parse_packet(packet)

    def test_parse_packet_invalid_checksum(self):
        """Verifica parse_packet() con checksum inválido."""
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x00])  # Checksum incorrecto
        with self.assertRaises(QScoutProtocolError):
            parse_packet(packet)


class TestExtractPackets(unittest.TestCase):
    """Tests para extract_packets()."""

    def test_extract_single_packet(self):
        """Verifica extract_packets() con un solo paquete."""
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        packets, remaining = extract_packets(packet)
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0], packet)
        self.assertEqual(remaining, b'')

    def test_extract_multiple_packets(self):
        """Verifica extract_packets() con múltiples paquetes concatenados."""
        packet1 = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        packet2 = bytes([0x52, 0x42, 0x0A, 0x01, 0x10, 0xFC, 0xFF, 0x00, 0x00, 0xAA])
        buffer = packet1 + packet2
        packets, remaining = extract_packets(buffer)
        self.assertEqual(len(packets), 2)
        self.assertEqual(packets[0], packet1)
        self.assertEqual(packets[1], packet2)
        self.assertEqual(remaining, b'')

    def test_extract_incomplete_buffer(self):
        """Verifica extract_packets() con buffer incompleto."""
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01])  # Falta checksum
        packets, remaining = extract_packets(packet)
        self.assertEqual(len(packets), 0)
        self.assertEqual(remaining, packet)

    def test_extract_with_garbage(self):
        """Verifica extract_packets() con datos basura antes del header."""
        garbage = bytes([0x00, 0x01, 0x02])
        packet = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        buffer = garbage + packet
        packets, remaining = extract_packets(buffer)
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0], packet)
        self.assertEqual(remaining, b'')


class TestOrderManager(unittest.TestCase):
    """Tests para OrderManager."""

    def test_initial_order_id(self):
        """Verifica que el primer Order ID es 2."""
        manager = OrderManager()
        self.assertEqual(manager.create(), 2)

    def test_sequential_order_ids(self):
        """Verifica que los Order IDs son secuenciales."""
        manager = OrderManager()
        self.assertEqual(manager.create(), 2)
        self.assertEqual(manager.create(), 3)
        self.assertEqual(manager.create(), 4)

    def test_cyclic_behavior(self):
        """Verifica el comportamiento cíclico (2-254)."""
        manager = OrderManager()
        # Avanzar hasta 254
        for _ in range(252):
            manager.create()
        self.assertEqual(manager.create(), 254)
        # Siguiente debe ser 2
        self.assertEqual(manager.create(), 2)

    def test_range_validation(self):
        """Verifica que los Order IDs están en el rango 2-254."""
        manager = OrderManager()
        for _ in range(100):
            order_id = manager.create()
            self.assertTrue(2 <= order_id <= 254)


class TestBuildersAndParsers(unittest.TestCase):
    """Tests para funciones builder y parser críticas."""

    def test_build_set_led(self):
        """Verifica build_set_led()."""
        packet = build_set_led(order_id=1, port=-4, r=255, g=0, b=0)
        self.assertEqual(len(packet), 10)  # Header (2) + length (1) + order_id (1) + action (1) + payload (4) + checksum (1)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[4], Action.SET_LED)
        self.assertTrue(validate_checksum(packet))

    def test_build_set_motor(self):
        """Verifica build_set_motor()."""
        packet = build_set_motor(order_id=1, port=1, speed=50)
        self.assertEqual(len(packet), 8)  # Header (2) + length (1) + order_id (1) + action (1) + payload (2) + checksum (1)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[4], Action.SET_MOTOR)
        self.assertTrue(validate_checksum(packet))

    def test_build_set_move(self):
        """Verifica build_set_move()."""
        packet = build_set_move(order_id=1, m1_speed=50, m2_speed=50)
        self.assertEqual(len(packet), 9)  # Header (2) + length (1) + order_id (1) + action (1) + payload (3) + checksum (1)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[4], Action.SET_MOTOR)
        self.assertTrue(validate_checksum(packet))

    def test_build_get_ultrasonic(self):
        """Verifica build_get_ultrasonic()."""
        packet = build_get_ultrasonic(order_id=1, port=1)
        self.assertEqual(len(packet), 7)  # Header (2) + length (1) + order_id (1) + action (1) + payload (1) + checksum (1)
        self.assertEqual(packet[:2], HEADER_RB)
        self.assertEqual(packet[4], Action.GET_ULTRASONIC)
        self.assertTrue(validate_checksum(packet))

    def test_parse_ultrasonic(self):
        """Verifica parse_ultrasonic()."""
        # Respuesta real: 52 42 08 01 01 09 C4 6B (distancia = 2500 mm)
        response = bytes([0x52, 0x42, 0x08, 0x01, 0x01, 0x09, 0xC4, 0x6B])
        distance = parse_ultrasonic(response)
        self.assertEqual(distance, 2500)  # 0x09 * 256 + 0xC4 = 2500

    def test_parse_device_info(self):
        """Verifica parse_device_info()."""
        # Respuesta simulada: RB 08 00 03 00 01 A0 (hw_version=0, sw_version=1)
        response = bytes([0x52, 0x42, 0x08, 0x00, 0x03, 0x00, 0x01, 0xA0])
        info = parse_device_info(response)
        self.assertEqual(info['action'], 0x03)
        self.assertEqual(info['hw_version'], 0)
        self.assertEqual(info['sw_version'], 1)

    def test_parse_voltage(self):
        """Verifica parse_voltage()."""
        # Respuesta: RB 07 01 01 64 01 (voltage = 100% = 0x64)
        response = bytes([0x52, 0x42, 0x07, 0x01, 0x01, 0x64, 0x01])
        voltage = parse_voltage(response)
        self.assertEqual(voltage, 100)

    def test_parse_line_value(self):
        """Verifica parse_line_value()."""
        # Respuesta: RB 07 01 01 02 9F (line_value = 2)
        response = bytes([0x52, 0x42, 0x07, 0x01, 0x01, 0x02, 0x9F])
        line_value = parse_line_value(response)
        self.assertEqual(line_value, 2)


if __name__ == '__main__':
    unittest.main()
