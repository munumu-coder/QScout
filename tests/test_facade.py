"""Tests for QScout facade and Order ID manager."""

import unittest

from qscout import QScout
from qscout.protocol import OrderManager


class TestQScoutFacade(unittest.TestCase):

    def test_qscout_has_actuators(self):
        self.assertTrue(hasattr(QScout, "led"))
        self.assertTrue(hasattr(QScout, "motor"))
        self.assertTrue(hasattr(QScout, "move"))
        self.assertTrue(hasattr(QScout, "stop"))
        self.assertTrue(hasattr(QScout, "buzzer"))

    def test_qscout_has_sensors(self):
        self.assertTrue(hasattr(QScout, "get_ultrasonic"))

    def test_qscout_repr(self):
        q = QScout.__new__(QScout)
        r = repr(q)
        self.assertIn("QScout", r)

    def test_led_integration(self):
        """Verify _send receives correct bytes for LED command."""
        sent = []

        class FakeConn:
            def send(self, data):
                sent.append(data)
            def receive(self, size):
                return b""

        q = QScout.__new__(QScout)
        q._connection = FakeConn()
        q._order_ids = OrderManager()
        q.led(-4, 255, 0, 0)

        self.assertEqual(len(sent), 1)
        raw = sent[0]
        self.assertEqual(raw[:2], b"\x52\x42")
        self.assertEqual(raw[3], 2)  # order_id
        self.assertEqual(raw[4], 0x10)  # action SET_LED
        self.assertEqual(raw[5], 0xFC)  # port -4
        self.assertEqual(raw[6], 255)  # R
        self.assertEqual(raw[7], 0)  # G
        self.assertEqual(raw[8], 0)  # B

    def test_motor_integration(self):
        sent = []

        class FakeConn:
            def send(self, data):
                sent.append(data)

        q = QScout.__new__(QScout)
        q._connection = FakeConn()
        q._order_ids = OrderManager()
        q.motor(-1, 80)

        raw = sent[0]
        self.assertEqual(raw[4], 0x11)  # action SET_MOTOR
        self.assertEqual(raw[5], 0xFF)  # port -1
        self.assertEqual(raw[6], 80)  # speed

    def test_move_integration(self):
        sent = []

        class FakeConn:
            def send(self, data):
                sent.append(data)

        q = QScout.__new__(QScout)
        q._connection = FakeConn()
        q._order_ids = OrderManager()
        q.move(50, 50)

        raw = sent[0]
        self.assertEqual(raw[4], 0x11)  # action SET_MOTOR
        self.assertEqual(raw[5], 0x00)  # reserved
        self.assertEqual(raw[6], 50)  # left
        self.assertEqual(raw[7], 50)  # right

    def test_buzzer_integration(self):
        sent = []

        class FakeConn:
            def send(self, data):
                sent.append(data)

        q = QScout.__new__(QScout)
        q._connection = FakeConn()
        q._order_ids = OrderManager()
        q.buzzer(440, 500)

        raw = sent[0]
        self.assertEqual(raw[4], 0x13)  # action SET_BUZZER

    def test_order_id_increments(self):
        sent = []

        class FakeConn:
            def send(self, data):
                sent.append(data)

        q = QScout.__new__(QScout)
        q._connection = FakeConn()
        q._order_ids = OrderManager()
        q.led(-4, 255, 0, 0)
        q.led(-4, 0, 0, 0)

        self.assertEqual(sent[0][3], 2)
        self.assertEqual(sent[1][3], 3)


if __name__ == "__main__":
    unittest.main()
