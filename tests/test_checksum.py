"""Tests for RB checksum calculation and validation."""

import unittest

from qscout.protocol import (
    HEADER,
    build_packet,
    sum_check,
    parse_packet,
    validate_checksum,
    receive_packet,
    MIN_PACKET_SIZE,
)
from qscout.exceptions import QScoutProtocolError, QScoutConnectionError


class TestChecksum(unittest.TestCase):

    def test_known_packet_checksum(self):
        """Real captured TX packet for GET_DEVICE_INFO."""
        pkt = bytes([0x52, 0x42, 0x06, 0x00, 0x01, 0x9B])
        self.assertEqual(sum_check(pkt[:-1]), 0x9B)

    def test_checksum_is_mod256(self):
        data = bytes(range(0, 256))
        csum = sum_check(data)
        self.assertEqual(csum, sum(data) % 256)

    def test_checksum_of_empty_is_zero(self):
        self.assertEqual(sum_check(b""), 0)

    def test_validate_checksum_passes(self):
        body = bytes([0x52, 0x42, 0x05, 0x01, 0x05, 0x02])
        csum = sum_check(body)
        pkt = body + bytes([csum])
        self.assertTrue(validate_checksum(pkt))

    def test_validate_checksum_fails(self):
        pkt = HEADER + bytes([0x05, 0x01, 0x05, 0x02, 0xFF])
        self.assertFalse(validate_checksum(pkt))

    def test_validate_checksum_too_short(self):
        self.assertFalse(validate_checksum(b"\x52"))

    def test_min_packet_size_is_6(self):
        self.assertEqual(MIN_PACKET_SIZE, 6)


class TestBuildPacket(unittest.TestCase):

    def test_build_minimal(self):
        pkt = build_packet(order_id=0x01, action=0x05)
        self.assertEqual(pkt[:2], HEADER)
        self.assertEqual(pkt[2], 0x06)
        self.assertEqual(pkt[3], 0x01)
        self.assertEqual(pkt[4], 0x05)
        self.assertEqual(len(pkt), 6)

    def test_build_with_payload(self):
        pkt = build_packet(order_id=0x01, action=0x02, payload=b"\x04\x04\x64")
        self.assertEqual(pkt[2], 0x09)
        self.assertEqual(pkt[5:8], b"\x04\x04\x64")
        self.assertEqual(len(pkt), 9)

    def test_build_checksum_valid(self):
        pkt = build_packet(order_id=0x02, action=0x01, payload=b"\x00\x02")
        self.assertTrue(validate_checksum(pkt))

    def test_build_real_motor_packet(self):
        pkt = build_packet(order_id=0x03, action=0x02, payload=b"\x04\x00\x50")
        order_id, action, payload = parse_packet(pkt)
        self.assertEqual(order_id, 0x03)
        self.assertEqual(action, 0x02)
        self.assertEqual(payload, b"\x04\x00\x50")


class TestBuildPacketValidation(unittest.TestCase):

    def test_order_id_too_large(self):
        with self.assertRaises(ValueError):
            build_packet(order_id=256, action=0x01)

    def test_order_id_negative(self):
        with self.assertRaises(ValueError):
            build_packet(order_id=-1, action=0x01)

    def test_action_too_large(self):
        with self.assertRaises(ValueError):
            build_packet(order_id=0x01, action=256)

    def test_action_negative(self):
        with self.assertRaises(ValueError):
            build_packet(order_id=0x01, action=-1)

    def test_order_id_wrong_type(self):
        with self.assertRaises(TypeError):
            build_packet(order_id="1", action=0x01)

    def test_action_wrong_type(self):
        with self.assertRaises(TypeError):
            build_packet(order_id=0x01, action="5")

    def test_payload_wrong_type(self):
        with self.assertRaises(TypeError):
            build_packet(order_id=0x01, action=0x05, payload="hello")

    def test_payload_bytearray_accepted(self):
        pkt = build_packet(order_id=0x01, action=0x05, payload=bytearray(b"\xAA"))
        self.assertEqual(pkt[5], 0xAA)


class TestParsePacket(unittest.TestCase):

    def test_parse_minimal(self):
        raw = build_packet(order_id=0x01, action=0x05)
        oid, act, pl = parse_packet(raw)
        self.assertEqual(oid, 0x01)
        self.assertEqual(act, 0x05)
        self.assertEqual(pl, b"")

    def test_parse_with_payload(self):
        raw = build_packet(order_id=0x02, action=0x02, payload=b"\x01\x02\x03")
        oid, act, pl = parse_packet(raw)
        self.assertEqual(oid, 0x02)
        self.assertEqual(act, 0x02)
        self.assertEqual(pl, b"\x01\x02\x03")

    def test_parse_too_short(self):
        with self.assertRaises(QScoutProtocolError):
            parse_packet(b"\x52\x42\x05")

    def test_parse_bad_header(self):
        with self.assertRaises(QScoutProtocolError):
            parse_packet(b"\x00\x00\x05\x01\x05\x00")

    def test_parse_bad_checksum(self):
        raw = build_packet(order_id=0x01, action=0x05)
        bad = raw[:-1] + bytes([(raw[-1] + 1) % 256])
        with self.assertRaises(QScoutProtocolError):
            parse_packet(bad)

    def test_roundtrip(self):
        original = build_packet(order_id=0x04, action=0x01, payload=b"\xAA\xBB")
        oid, act, pl = parse_packet(original)
        rebuilt = build_packet(order_id=oid, action=act, payload=pl)
        self.assertEqual(original, rebuilt)


class TestReceivePacket(unittest.TestCase):

    def _make_connection(self, data: bytes):
        """Create a mock connection that returns fixed data."""
        class MockConnection:
            def __init__(self, buf):
                self._buf = buf
                self._pos = 0
            def receive(self, size):
                chunk = self._buf[self._pos:self._pos + size]
                self._pos += size
                return chunk
        return MockConnection(data)

    def test_receive_minimal_packet(self):
        pkt = build_packet(order_id=0x01, action=0x05)
        conn = self._make_connection(pkt)
        oid, act, pl = receive_packet(conn)
        self.assertEqual(oid, 0x01)
        self.assertEqual(act, 0x05)
        self.assertEqual(pl, b"")

    def test_receive_packet_with_payload(self):
        pkt = build_packet(order_id=0x02, action=0x02, payload=b"\x01\x02\x03")
        conn = self._make_connection(pkt)
        oid, act, pl = receive_packet(conn)
        self.assertEqual(oid, 0x02)
        self.assertEqual(act, 0x02)
        self.assertEqual(pl, b"\x01\x02\x03")

    def test_receive_no_data(self):
        conn = self._make_connection(b"")
        with self.assertRaises(QScoutConnectionError):
            receive_packet(conn)

    def test_receive_incomplete_header(self):
        conn = self._make_connection(b"\x52\x42")
        with self.assertRaises(QScoutConnectionError):
            receive_packet(conn)


if __name__ == "__main__":
    unittest.main()
