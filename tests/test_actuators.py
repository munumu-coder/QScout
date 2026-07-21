"""Tests for actuator commands via the Actuators class."""

import struct
import unittest
from unittest.mock import MagicMock

from qscout.actuators import Actuators
from qscout.protocol import OrderManager, Action


class TestActuators(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.order_ids = OrderManager()
        self.act = Actuators(self.mock_conn, self.order_ids)

    def test_led_sends_correct_packet(self):
        self.act.led(port=-4, r=255, g=0, b=0)
        self.mock_conn.send.assert_called_once()
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[:2], b'RB')
        self.assertEqual(pkt[3], 2)
        self.assertEqual(pkt[4], Action.SET_LED)

    def test_led_payload_format(self):
        self.act.led(port=-4, r=255, g=0, b=0)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[5:9], struct.pack('<bBBB', -4, 255, 0, 0))



    def test_motor_sends_correct_action(self):
        self.act.motor(port=-1, speed=80)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[4], Action.SET_MOTOR)
        self.assertEqual(pkt[5], 0xFF)
        self.assertEqual(pkt[6], 80)

    def test_motor_speed_clamped(self):
        self.act.motor(port=1, speed=200)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 100)

    def test_motor_speed_negative_clamped(self):
        self.act.motor(port=1, speed=-200)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], (-100) & 0xFF)

    def test_motor_stop(self):
        self.act.motor(port=-1, speed=0)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 0)

    def test_move_sends_correct_action(self):
        self.act.move(m1_speed=50, m2_speed=50)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[4], Action.SET_MOTOR)
        self.assertEqual(pkt[5], 0x00)
        self.assertEqual(pkt[6], 50)
        self.assertEqual(pkt[7], 50)

    def test_move_different_speeds(self):
        self.act.move(m1_speed=80, m2_speed=-80)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 80)
        self.assertEqual(pkt[7], (-80) & 0xFF)

    def test_move_speed_clamped(self):
        self.act.move(m1_speed=150, m2_speed=150)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 100)
        self.assertEqual(pkt[7], 100)

    def test_forward(self):
        self.act.forward(100)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 100)
        self.assertEqual(pkt[7], 100)

    def test_backward(self):
        self.act.backward(100)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], (-100) & 0xFF)
        self.assertEqual(pkt[7], (-100) & 0xFF)

    def test_turn_left(self):
        self.act.turn_left(100)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], (-100) & 0xFF)
        self.assertEqual(pkt[7], 100)

    def test_turn_right(self):
        self.act.turn_right(100)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 100)
        self.assertEqual(pkt[7], (-100) & 0xFF)

    def test_stop(self):
        self.act.stop()
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[6], 0)
        self.assertEqual(pkt[7], 0)

    def test_buzzer_sends_correct_action(self):
        self.act.buzzer(frequency=440, duration_ms=500)
        pkt = self.mock_conn.send.call_args[0][0]
        self.assertEqual(pkt[4], Action.SET_BUZZER)

    def test_buzzer_payload(self):
        self.act.buzzer(frequency=1000, duration_ms=100)
        pkt = self.mock_conn.send.call_args[0][0]
        freq = struct.unpack_from("<H", pkt, 6)[0]
        dur = struct.unpack_from("<H", pkt, 8)[0]
        self.assertEqual(freq, 1000)
        self.assertEqual(dur, 100)

    def test_order_id_increments(self):
        self.act.led(-4, 255, 0, 0)
        self.act.led(-4, 0, 0, 0)
        pkts = [call[0][0] for call in self.mock_conn.send.call_args_list]
        self.assertEqual(pkts[0][3], 2)
        self.assertEqual(pkts[1][3], 3)


if __name__ == "__main__":
    unittest.main()
