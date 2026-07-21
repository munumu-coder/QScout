"""Regression tests using real packets captured during Phase 3B validation.

These tests use actual packets captured from the Q-Scout robot to ensure
the protocol implementation correctly handles real-world data.
"""

import unittest
from qscout.protocol import (
    Action, Port, sum_check, build_packet, build_get_device_info,
    build_get_ultrasonic, build_get_line_value, build_set_led,
    build_set_move, build_set_buzzer, parse_header, parse_order_id,
    parse_action, parse_length, parse_checksum_ok, parse_device_info,
    parse_ultrasonic, parse_voltage, parse_button, parse_light,
    parse_temp_humidity,
)


class TestRealPacketsTX(unittest.TestCase):
    """Test packet building using real captured packets."""

    def test_get_device_info(self):
        """Test GET_DEVICE_INFO packet matches real capture."""
        # Real captured packet: 52420600019b
        pkt = build_get_device_info(0)
        
        self.assertEqual(pkt, bytes([82, 66, 6, 0, 1, 155]))
        self.assertEqual(pkt.hex(), '52420600019b')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_get_ultrasonic(self):
        """Test GET_ULTRASONIC packet matches real capture."""
        # Real captured packet: 52420701a1013e
        pkt = build_get_ultrasonic(1, 1)
        
        self.assertEqual(pkt, bytes([82, 66, 7, 1, 161, 1, 62]))
        self.assertEqual(pkt.hex(), '52420701a1013e')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_get_line_value(self):
        """Test GET_LINE_VALUE packet matches real capture."""
        # Real captured packet: 5242070aa4034c (Order ID = 10)
        pkt = build_get_line_value(10, 3)
        
        self.assertEqual(pkt, bytes([82, 66, 7, 10, 164, 3, 76]))
        self.assertEqual(pkt.hex(), '5242070aa4034c')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_led_red(self):
        """Test SET_LED RED packet matches real capture."""
        # Real captured packet: 52420a0210fcff0000ab
        pkt = build_set_led(2, Port.BOARD_LED_1, 255, 0, 0)
        
        self.assertEqual(pkt, bytes([82, 66, 10, 2, 16, 252, 255, 0, 0, 171]))
        self.assertEqual(pkt.hex(), '52420a0210fcff0000ab')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_led_green(self):
        """Test SET_LED GREEN packet matches real capture."""
        # Real captured packet: 52420a1210fc00ff00bb
        pkt = build_set_led(18, Port.BOARD_LED_1, 0, 255, 0)
        
        self.assertEqual(pkt, bytes([82, 66, 10, 18, 16, 252, 0, 255, 0, 187]))
        self.assertEqual(pkt.hex(), '52420a1210fc00ff00bb')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_led_blue(self):
        """Test SET_LED BLUE packet matches real capture."""
        # Real captured packet: 52420a1410fc0000ffbd
        pkt = build_set_led(20, Port.BOARD_LED_1, 0, 0, 255)
        
        self.assertEqual(pkt, bytes([82, 66, 10, 20, 16, 252, 0, 0, 255, 189]))
        self.assertEqual(pkt.hex(), '52420a1410fc0000ffbd')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_led_off(self):
        """Test SET_LED OFF packet matches real capture."""
        # Real captured packet: 52420a1510fc000000bf
        pkt = build_set_led(21, Port.BOARD_LED_1, 0, 0, 0)
        
        self.assertEqual(pkt, bytes([82, 66, 10, 21, 16, 252, 0, 0, 0, 191]))
        self.assertEqual(pkt.hex(), '52420a1510fc000000bf')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_move_forward(self):
        """Test SET_MOVE forward packet matches real capture."""
        # Real captured packet: 5242091711001414ed
        pkt = build_set_move(23, 20, 20)
        
        self.assertEqual(pkt, bytes([82, 66, 9, 23, 17, 0, 20, 20, 237]))
        self.assertEqual(pkt.hex(), '5242091711001414ed')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_move_backward(self):
        """Test SET_MOVE backward packet matches real capture."""
        # Real captured packet: 524209191100ecec9f
        pkt = build_set_move(25, -20, -20)
        
        self.assertEqual(pkt, bytes([82, 66, 9, 25, 17, 0, 236, 236, 159]))
        self.assertEqual(pkt.hex(), '524209191100ecec9f')
        self.assertTrue(parse_checksum_ok(pkt))

    def test_set_move_stop(self):
        """Test SET_MOVE stop packet matches real capture."""
        # Real captured packet: 5242091a11000000c8
        pkt = build_set_move(26, 0, 0)
        
        self.assertEqual(pkt, bytes([82, 66, 9, 26, 17, 0, 0, 0, 200]))
        self.assertEqual(pkt.hex(), '5242091a11000000c8')
        self.assertTrue(parse_checksum_ok(pkt))


class TestRealPacketsRX(unittest.TestCase):
    """Test response parsing using real captured packets."""

    def test_device_info_response(self):
        """Test parsing real GET_DEVICE_INFO response."""
        # Real captured response: 52420800030001a0
        pkt = bytes([82, 66, 8, 0, 3, 0, 1, 160])
        
        self.assertTrue(parse_checksum_ok(pkt))
        self.assertEqual(parse_header(pkt), True)
        self.assertEqual(parse_order_id(pkt), 0)
        self.assertEqual(parse_action(pkt), 3)  # Action is 0x03, NOT 0x01!
        
        info = parse_device_info(pkt)
        self.assertEqual(info['hw_version'], 0)
        self.assertEqual(info['sw_version'], 1)

    def test_ultrasonic_response(self):
        """Test parsing real GET_ULTRASONIC response."""
        # Real captured response: 524208010109c46b
        pkt = bytes([82, 66, 8, 1, 1, 9, 196, 107])
        
        self.assertTrue(parse_checksum_ok(pkt))
        self.assertEqual(parse_header(pkt), True)
        self.assertEqual(parse_order_id(pkt), 1)
        self.assertEqual(parse_action(pkt), 1)  # Action is 0x01, NOT 0xA1!
        
        distance = parse_ultrasonic(pkt)
        self.assertEqual(distance, 2500)  # 9*256 + 196 = 2500mm

    def test_line_value_response(self):
        """Test parsing real GET_LINE_VALUE response."""
        # Real captured response: 5242070a0102a8 (Order ID = 10)
        pkt = bytes([82, 66, 7, 10, 1, 2, 168])
        
        self.assertTrue(parse_checksum_ok(pkt))
        self.assertEqual(parse_header(pkt), True)
        self.assertEqual(parse_order_id(pkt), 10)
        self.assertEqual(parse_action(pkt), 1)  # Action is 0x01, NOT 0xA4!
        
        # Line value is at offset 5
        self.assertEqual(pkt[5], 2)

    def test_set_led_response(self):
        """Test parsing real SET_LED response."""
        # Real captured response: 52420602019d
        pkt = bytes([82, 66, 6, 2, 1, 157])
        
        self.assertTrue(parse_checksum_ok(pkt))
        self.assertEqual(parse_header(pkt), True)
        self.assertEqual(parse_order_id(pkt), 2)
        self.assertEqual(parse_action(pkt), 1)  # Action is 0x01, NOT 0x10!
        
        # SET responses have no payload
        self.assertEqual(len(pkt), 6)

    def test_order_id_matching(self):
        """Test that Order ID matches between request and response."""
        # Request Order ID = 5
        request_pkt = build_get_ultrasonic(5, 1)
        self.assertEqual(request_pkt[3], 5)
        
        # Response Order ID should be 5
        response_pkt = bytes([82, 66, 8, 5, 1, 9, 196, 107])
        self.assertEqual(response_pkt[3], 5)
        
        # Order IDs match
        self.assertEqual(request_pkt[3], response_pkt[3])

    def test_action_code_mismatch(self):
        """Test that Action code does NOT match between request and response."""
        # Request Action = 0xA1
        request_pkt = build_get_ultrasonic(1, 1)
        self.assertEqual(request_pkt[4], 0xA1)
        
        # Response Action = 0x01 (NOT 0xA1!)
        response_pkt = bytes([82, 66, 8, 1, 1, 9, 196, 107])
        self.assertEqual(response_pkt[4], 0x01)
        
        # Action codes do NOT match
        self.assertNotEqual(request_pkt[4], response_pkt[4])


class TestChecksumVerification(unittest.TestCase):
    """Test checksum calculation and verification."""

    def test_all_real_packets_valid(self):
        """Test that all real captured packets have valid checksums."""
        real_packets = [
            bytes([82, 66, 6, 0, 1, 155]),      # GET_DEVICE_INFO TX
            bytes([82, 66, 8, 0, 3, 0, 1, 160]), # GET_DEVICE_INFO RX
            bytes([82, 66, 7, 1, 161, 1, 62]),   # GET_ULTRASONIC TX
            bytes([82, 66, 8, 1, 1, 9, 196, 107]), # GET_ULTRASONIC RX
            bytes([82, 66, 7, 10, 164, 3, 76]),  # GET_LINE_VALUE TX (Order ID = 10)
            bytes([82, 66, 7, 10, 1, 2, 168]),   # GET_LINE_VALUE RX (Order ID = 10)
            bytes([82, 66, 10, 2, 16, 252, 255, 0, 0, 171]), # SET_LED TX
            bytes([82, 66, 6, 2, 1, 157]),       # SET_LED RX
        ]
        
        for pkt in real_packets:
            self.assertTrue(
                parse_checksum_ok(pkt),
                f'Checksum invalid for packet: {pkt.hex()}'
            )

    def test_checksum_formula(self):
        """Test checksum formula matches real packets."""
        # Test with known packet
        pkt = bytes([82, 66, 6, 0, 1, 155])
        expected_checksum = 155
        calculated_checksum = sum(pkt[:-1]) % 256
        
        self.assertEqual(calculated_checksum, expected_checksum)


if __name__ == '__main__':
    unittest.main()
