"""Tests for sensor commands via the Sensors class."""

import unittest
from unittest.mock import MagicMock

from qscout.sensors import Sensors
from qscout.protocol import OrderManager


class TestSensors(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.order_ids = OrderManager()
        self.sens = Sensors(self.mock_conn, self.order_ids)

    def test_ultrasonic_sends_and_parses(self):
        # Real ultrasonic response: 52 42 08 01 01 09 C4 6B (distance=2500mm)
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x08, 0x01, 0x01, 0x09, 0xC4, 0x6B]
        )
        distance = self.sens.ultrasonic(port=1)
        self.assertEqual(distance, 2500)

    def test_ultrasonic_returns_none_on_no_response(self):
        self.mock_conn.send_receive.return_value = None
        self.assertIsNone(self.sens.ultrasonic(port=1))

    def test_voltage_parses_correctly(self):
        # Voltage at byte 5 = 0x64 = 100
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x07, 0x01, 0x01, 0x64, 0x01]
        )
        v = self.sens.voltage(port=1)
        self.assertEqual(v, 100)

    def test_voltage_returns_none_on_no_response(self):
        self.mock_conn.send_receive.return_value = None
        self.assertIsNone(self.sens.voltage())

    def test_device_info_parses(self):
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x08, 0x01, 0x03, 0x00, 0x01, 0x01]
        )
        info = self.sens.device_info()
        self.assertEqual(info['hw_version'], 0)
        self.assertEqual(info['sw_version'], 1)

    def test_device_info_returns_none_on_no_response(self):
        self.mock_conn.send_receive.return_value = None
        self.assertIsNone(self.sens.device_info())

    def test_button_parses(self):
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x06, 0x01, 0x01, 0x01]
        )
        self.assertEqual(self.sens.button(port=-7), 1)

    def test_line_value_parses(self):
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x07, 0x01, 0x01, 0x02, 0x9F]
        )
        self.assertEqual(self.sens.line_value(port=3), 2)

    def test_order_id_increments(self):
        self.mock_conn.send_receive.return_value = bytes(
            [0x52, 0x42, 0x08, 0x01, 0x01, 0x09, 0xC4, 0x6B]
        )
        self.sens.ultrasonic(1)
        self.sens.ultrasonic(1)
        reqs = [call[0][0] for call in self.mock_conn.send_receive.call_args_list]
        self.assertEqual(reqs[0][3], 2)
        self.assertEqual(reqs[1][3], 3)


if __name__ == "__main__":
    unittest.main()
