#!/usr/bin/env python3
"""Phase 3B: Physical validation of Q-Scout robot.

This script performs comprehensive testing of the QScout library
against the actual robot hardware, logging all communication.
"""

import sys
import os
import time
import struct
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from qscout.connection import Connection
from qscout.protocol import (
    Action, Port, OrderManager, sum_check, build_packet,
    build_get_device_info, build_get_ultrasonic, build_get_voltage,
    build_get_button, build_get_light, build_get_line_value,
    build_get_temp_humidity, build_get_voice, build_get_infrared,
    build_get_gyro, build_get_color, build_get_touch_button,
    build_get_temp_dual, build_get_six_line, build_get_rocker,
    build_get_flame, build_get_gas, build_get_spiral_pot,
    build_get_line_pot, build_get_interface_info, build_get_all_interface_info,
    build_get_motor_interface_info, build_get_user_interface_info,
    build_set_led, build_set_motor, build_set_move, build_set_buzzer,
    build_set_ultrasonic_light, build_set_matrix, build_set_work_mode,
    build_set_steering_engine, build_set_out_engine, build_set_rgb_led_matrix,
    build_set_mp3, build_set_fan, build_set_ext_servo_degree,
    build_set_ext_io_output, build_set_four_digit, build_set_four_rgb_led,
    parse_header, parse_order_id, parse_action, parse_length, parse_checksum_ok,
    parse_device_info, parse_voltage, parse_ultrasonic, parse_button,
    parse_light, parse_temp_humidity, parse_voice, parse_infrared,
    parse_gyro, parse_color_rgb, parse_color_grey, parse_touch_button,
    parse_temp_dual, parse_six_line, parse_rocker,
)


class PacketLogger:
    """Logs all TX/RX packets with timestamps and analysis."""

    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f'validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        self.packets = []
        self._log(f'=== QScout Physical Validation Log ===')
        self._log(f'Started: {datetime.now().isoformat()}')
        self._log('')

    def _log(self, msg: str) -> None:
        with open(self.log_file, 'a') as f:
            f.write(msg + '\n')
        print(msg)

    def log_tx(self, packet: bytes, description: str = '') -> None:
        """Log a transmitted packet."""
        self._log(f'TX [{datetime.now().isoformat()}] {description}')
        self._log(f'  Hex: {packet.hex()}')
        self._log(f'  Len: {len(packet)}')
        self._log(f'  Bytes: {list(packet)}')
        self._log(f'  Checksum: {packet[-1]} (calc: {sum_check(packet[:-1])})')
        self._log(f'  Header: {packet[:2]}')
        self._log(f'  Length field: {packet[2]}')
        self._log(f'  Order ID: {packet[3]}')
        self._log(f'  Action: 0x{packet[4]:02X}')
        if len(packet) > 6:
            self._log(f'  Payload: {list(packet[5:-1])}')
        self._log('')
        self.packets.append(('TX', time.time(), packet, description))

    def log_rx(self, packet: bytes, description: str = '') -> None:
        """Log a received packet."""
        self._log(f'RX [{datetime.now().isoformat()}] {description}')
        self._log(f'  Hex: {packet.hex()}')
        self._log(f'  Len: {len(packet)}')
        self._log(f'  Bytes: {list(packet)}')
        self._log(f'  Checksum: {packet[-1]} (calc: {sum_check(packet[:-1])}, valid: {parse_checksum_ok(packet)})')
        self._log(f'  Header: {packet[:2]}')
        self._log(f'  Length field: {packet[2]}')
        self._log(f'  Order ID: {packet[3]}')
        self._log(f'  Action: 0x{packet[4]:02X}')
        if len(packet) > 6:
            self._log(f'  Payload: {list(packet[5:-1])}')
        self._log('')
        self.packets.append(('RX', time.time(), packet, description))

    def log_error(self, msg: str) -> None:
        """Log an error."""
        self._log(f'ERROR [{datetime.now().isoformat()}] {msg}')
        self._log('')

    def log_section(self, title: str) -> None:
        """Log a section header."""
        self._log('')
        self._log(f'=== {title} ===')
        self._log('')

    def get_summary(self) -> dict:
        """Get a summary of all logged packets."""
        tx_count = sum(1 for p in self.packets if p[0] == 'TX')
        rx_count = sum(1 for p in self.packets if p[0] == 'RX')
        return {
            'total_packets': len(self.packets),
            'tx_packets': tx_count,
            'rx_packets': rx_count,
            'log_file': str(self.log_file),
        }


def analyze_packet(packet: bytes) -> dict:
    """Analyze a packet and return its structure."""
    if len(packet) < 6:
        return {'error': 'Packet too short'}
    
    result = {
        'header': packet[:2],
        'length': packet[2],
        'order_id': packet[3],
        'action': f'0x{packet[4]:02X}',
        'checksum_valid': parse_checksum_ok(packet),
    }
    
    if len(packet) > 6:
        result['payload'] = list(packet[5:-1])
    
    return result


def test_device_info(conn: Connection, logger: PacketLogger) -> dict:
    """Test GET_DEVICE_INFO command."""
    logger.log_section('TEST: GET_DEVICE_INFO (0x01)')
    
    order = conn.next_order_id()
    pkt = build_get_device_info(order)
    logger.log_tx(pkt, 'GET_DEVICE_INFO')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'DEVICE_INFO response')
        info = parse_device_info(response)
        logger._log(f'  Parsed: {info}')
        return info
    else:
        logger.log_error('No response received')
        return {}


def test_ultrasonic(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_ULTRASONIC command."""
    logger.log_section(f'TEST: GET_ULTRASONIC (0xA1) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_ultrasonic(order, port)
    logger.log_tx(pkt, f'GET_ULTRASONIC port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'ULTRASONIC response')
        distance = parse_ultrasonic(response)
        logger._log(f'  Distance: {distance} mm')
        return {'distance': distance}
    else:
        logger.log_error('No response received')
        return {}


def test_voltage(conn: Connection, logger: PacketLogger) -> dict:
    """Test GET_VOLTAGE command."""
    logger.log_section('TEST: GET_VOLTAGE (0xA3)')
    
    order = conn.next_order_id()
    pkt = build_get_voltage(order, 1)
    logger.log_tx(pkt, 'GET_VOLTAGE')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'VOLTAGE response')
        voltage = parse_voltage(response)
        logger._log(f'  Voltage: {voltage}%')
        return {'voltage': voltage}
    else:
        logger.log_error('No response received')
        return {}


def test_button(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_BUTTON command."""
    logger.log_section(f'TEST: GET_BUTTON (0xA2) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_button(order, port)
    logger.log_tx(pkt, f'GET_BUTTON port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'BUTTON response')
        state = parse_button(response)
        logger._log(f'  Button state: {state}')
        return {'state': state}
    else:
        logger.log_error('No response received')
        return {}


def test_light(conn: Connection, logger: PacketLogger, port: int = 2) -> dict:
    """Test GET_LIGHT command."""
    logger.log_section(f'TEST: GET_LIGHT (0xA6) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_light(order, port)
    logger.log_tx(pkt, f'GET_LIGHT port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'LIGHT response')
        light = parse_light(response)
        logger._log(f'  Light level: {light}')
        return {'light': light}
    else:
        logger.log_error('No response received')
        return {}


def test_temp_humidity(conn: Connection, logger: PacketLogger, port: int = 2) -> dict:
    """Test GET_TEMP_HUMIDITY command."""
    logger.log_section(f'TEST: GET_TEMP_HUMIDITY (0xA5) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_temp_humidity(order, port)
    logger.log_tx(pkt, f'GET_TEMP_HUMIDITY port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'TEMP_HUMIDITY response')
        data = parse_temp_humidity(response)
        logger._log(f'  Temperature: {data}')
        return data
    else:
        logger.log_error('No response received')
        return {}


def test_line_value(conn: Connection, logger: PacketLogger, port: int = 3) -> dict:
    """Test GET_LINE_VALUE command."""
    logger.log_section(f'TEST: GET_LINE_VALUE (0xA4) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_line_value(order, port)
    logger.log_tx(pkt, f'GET_LINE_VALUE port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'LINE_VALUE response')
        if len(response) >= 6:
            value = response[5]
            logger._log(f'  Line value: {value}')
            return {'value': value}
    else:
        logger.log_error('No response received')
    return {}


def test_voice(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_VOICE command."""
    logger.log_section(f'TEST: GET_VOICE (0xA7) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_voice(order, port)
    logger.log_tx(pkt, f'GET_VOICE port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'VOICE response')
        if len(response) >= 7:
            value = response[5] * 256 + response[6]
            logger._log(f'  Voice level: {value}')
            return {'level': value}
    else:
        logger.log_error('No response received')
    return {}


def test_infrared(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_INFRARED command."""
    logger.log_section(f'TEST: GET_INFRARED (0xA8) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_infrared(order, port)
    logger.log_tx(pkt, f'GET_INFRARED port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'INFRARED response')
        state = parse_infrared(response)
        logger._log(f'  Infrared state: {state}')
        return {'state': state}
    else:
        logger.log_error('No response received')
        return {}


def test_gyro(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_GYRO command."""
    logger.log_section(f'TEST: GET_GYRO (0xA9) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_gyro(order, port)
    logger.log_tx(pkt, f'GET_GYRO port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'GYRO response')
        data = parse_gyro(response)
        logger._log(f'  Gyro XYZ: {data}')
        return {'xyz': data}
    else:
        logger.log_error('No response received')
        return {}


def test_color(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_COLOR command."""
    logger.log_section(f'TEST: GET_COLOR (0xAA) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_color(order, port)
    logger.log_tx(pkt, f'GET_COLOR port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'COLOR response')
        data = parse_color_rgb(response)
        logger._log(f'  Color RGB: {data}')
        return data
    else:
        logger.log_error('No response received')
        return {}


def test_touch_button(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_TOUCH_BUTTON command."""
    logger.log_section(f'TEST: GET_TOUCH_BUTTON (0xAB) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_touch_button(order, port)
    logger.log_tx(pkt, f'GET_TOUCH_BUTTON port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'TOUCH_BUTTON response')
        buttons = parse_touch_button(response)
        logger._log(f'  Buttons pressed: {buttons}')
        return {'buttons': buttons}
    else:
        logger.log_error('No response received')
        return {}


def test_rocker(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_ROCKER command."""
    logger.log_section(f'TEST: GET_ROCKER (0xAE) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_rocker(order, port)
    logger.log_tx(pkt, f'GET_ROCKER port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'ROCKER response')
        data = parse_rocker(response)
        logger._log(f'  Rocker XY: {data}')
        return {'xy': data}
    else:
        logger.log_error('No response received')
        return {}


def test_interface_info(conn: Connection, logger: PacketLogger, port: int = 1) -> dict:
    """Test GET_INTERFACE_INFO command."""
    logger.log_section(f'TEST: GET_INTERFACE_INFO (0x02) on port {port}')
    
    order = conn.next_order_id()
    pkt = build_get_interface_info(order, port)
    logger.log_tx(pkt, f'GET_INTERFACE_INFO port={port}')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'INTERFACE_INFO response')
        if len(response) >= 6:
            info = {'type': response[5]}
            if len(response) >= 14:
                info['ports'] = list(response[5:14])
            logger._log(f'  Interface info: {info}')
            return info
    else:
        logger.log_error('No response received')
    return {}


def test_all_interface_info(conn: Connection, logger: PacketLogger) -> dict:
    """Test GET_ALL_INTERFACE_INFO command."""
    logger.log_section('TEST: GET_ALL_INTERFACE_INFO (0x03)')
    
    order = conn.next_order_id()
    pkt = build_get_all_interface_info(order)
    logger.log_tx(pkt, 'GET_ALL_INTERFACE_INFO')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'ALL_INTERFACE_INFO response')
        if len(response) >= 6:
            info = {'interfaces': list(response[5:-1])}
            logger._log(f'  All interfaces: {info}')
            return info
    else:
        logger.log_error('No response received')
    return {}


def test_motor_interface_info(conn: Connection, logger: PacketLogger) -> dict:
    """Test GET_MOTOR_INTERFACE_INFO command."""
    logger.log_section('TEST: GET_MOTOR_INTERFACE_INFO (0x04)')
    
    order = conn.next_order_id()
    pkt = build_get_motor_interface_info(order)
    logger.log_tx(pkt, 'GET_MOTOR_INTERFACE_INFO')
    
    response = conn.send_receive(pkt, timeout=1.0)
    if response:
        logger.log_rx(response, 'MOTOR_INTERFACE_INFO response')
        if len(response) >= 6:
            info = {'motor_a': response[5], 'motor_b': response[6]}
            logger._log(f'  Motor info: {info}')
            return info
    else:
        logger.log_error('No response received')
    return {}


def test_set_led(conn: Connection, logger: PacketLogger, port: int, r: int, g: int, b: int) -> dict:
    """Test SET_LED command."""
    logger.log_section(f'TEST: SET_LED (0x10) port={port} RGB=({r},{g},{b})')
    
    order = conn.next_order_id()
    pkt = build_set_led(order, port, r, g, b)
    logger.log_tx(pkt, f'SET_LED port={port} RGB=({r},{g},{b})')
    
    response = conn.send_receive(pkt, timeout=0.5)
    if response:
        logger.log_rx(response, 'SET_LED response')
        return {'response': list(response)}
    else:
        logger._log('  No response (expected for SET commands)')
        return {}


def test_set_buzzer(conn: Connection, logger: PacketLogger, frequency: int, duration: int) -> dict:
    """Test SET_BUZZER command."""
    logger.log_section(f'TEST: SET_BUZZER (0x13) freq={frequency} dur={duration}')
    
    order = conn.next_order_id()
    pkt = build_set_buzzer(order, Port.BOARD_BUZZER, frequency, duration)
    logger.log_tx(pkt, f'SET_BUZZER freq={frequency} dur={duration}')
    
    response = conn.send_receive(pkt, timeout=0.5)
    if response:
        logger.log_rx(response, 'SET_BUZZER response')
        return {'response': list(response)}
    else:
        logger._log('  No response (expected for SET commands)')
        return {}


def test_set_move(conn: Connection, logger: PacketLogger, m1: int, m2: int) -> dict:
    """Test SET_MOVE (dual motor) command."""
    logger.log_section(f'TEST: SET_MOVE (0x11) M1={m1} M2={m2}')
    
    order = conn.next_order_id()
    pkt = build_set_move(order, m1, m2)
    logger.log_tx(pkt, f'SET_MOVE M1={m1} M2={m2}')
    
    response = conn.send_receive(pkt, timeout=0.5)
    if response:
        logger.log_rx(response, 'SET_MOVE response')
        return {'response': list(response)}
    else:
        logger._log('  No response (expected for SET commands)')
        return {}


def test_set_motor(conn: Connection, logger: PacketLogger, port: int, speed: int) -> dict:
    """Test SET_MOTOR (single motor) command."""
    logger.log_section(f'TEST: SET_MOTOR (0x11) port={port} speed={speed}')
    
    order = conn.next_order_id()
    pkt = build_set_motor(order, port, speed)
    logger.log_tx(pkt, f'SET_MOTOR port={port} speed={speed}')
    
    response = conn.send_receive(pkt, timeout=0.5)
    if response:
        logger.log_rx(response, 'SET_MOTOR response')
        return {'response': list(response)}
    else:
        logger._log('  No response (expected for SET commands)')
        return {}


def test_response_structure(conn: Connection, logger: PacketLogger) -> None:
    """Test response structure by analyzing multiple responses."""
    logger.log_section('TEST: Response Structure Analysis')
    
    # Test multiple sensors to understand response format
    tests = [
        ('GET_VOLTAGE', lambda: build_get_voltage(conn.next_order_id(), 1)),
        ('GET_ULTRASONIC', lambda: build_get_ultrasonic(conn.next_order_id(), 1)),
        ('GET_BUTTON', lambda: build_get_button(conn.next_order_id(), 1)),
        ('GET_LIGHT', lambda: build_get_light(conn.next_order_id(), 2)),
    ]
    
    for name, builder in tests:
        pkt = builder()
        logger.log_tx(pkt, f'{name} (structure test)')
        response = conn.send_receive(pkt, timeout=1.0)
        if response:
            logger.log_rx(response, f'{name} response (structure)')
            logger._log(f'  Analysis: {analyze_packet(response)}')
        else:
            logger.log_error(f'{name}: No response')


def run_all_tests(port: str = '/dev/ttyUSB0') -> dict:
    """Run all validation tests."""
    logger = PacketLogger('logs')
    results = {}
    
    logger.log_section('PHASE 3B: PHYSICAL VALIDATION')
    logger._log(f'Robot port: {port}')
    logger._log(f'Start time: {datetime.now().isoformat()}')
    logger._log('')
    
    try:
        # Open connection
        conn = Connection(port)
        conn.open()
        logger._log(f'Connection opened: {conn.is_open}')
        logger._log(f'Port: {conn._port_name}')
        logger._log(f'Baudrate: {conn._baudrate}')
        logger._log('')
        
        # Test 1: Device Info
        results['device_info'] = test_device_info(conn, logger)
        time.sleep(0.5)
        
        # Test 2: Response Structure
        test_response_structure(conn, logger)
        time.sleep(0.5)
        
        # Test 3: Ultrasonic
        results['ultrasonic'] = test_ultrasonic(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 4: Voltage
        results['voltage'] = test_voltage(conn, logger)
        time.sleep(0.5)
        
        # Test 5: Button
        results['button'] = test_button(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 6: Light
        results['light'] = test_light(conn, logger, port=2)
        time.sleep(0.5)
        
        # Test 7: Temp/Humidity (may not be connected)
        results['temp_humidity'] = test_temp_humidity(conn, logger, port=2)
        time.sleep(0.5)
        
        # Test 8: Line Value
        results['line_value'] = test_line_value(conn, logger, port=3)
        time.sleep(0.5)
        
        # Test 9: Voice
        results['voice'] = test_voice(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 10: Infrared
        results['infrared'] = test_infrared(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 11: Interface Info
        results['interface_info'] = test_interface_info(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 12: All Interface Info
        results['all_interface_info'] = test_all_interface_info(conn, logger)
        time.sleep(0.5)
        
        # Test 13: Motor Interface Info
        results['motor_interface_info'] = test_motor_interface_info(conn, logger)
        time.sleep(0.5)
        
        # Test 14: LED Test (RED)
        logger._log('>>> Please observe the robot LED <<<')
        results['led_red'] = test_set_led(conn, logger, Port.BOARD_LED_1, 255, 0, 0)
        time.sleep(2)
        
        # Turn off LED
        test_set_led(conn, logger, Port.BOARD_LED_1, 0, 0, 0)
        time.sleep(0.5)
        
        # Test 15: LED Test (GREEN)
        logger._log('>>> Please observe the robot LED <<<')
        results['led_green'] = test_set_led(conn, logger, Port.BOARD_LED_1, 0, 255, 0)
        time.sleep(2)
        
        # Turn off LED
        test_set_led(conn, logger, Port.BOARD_LED_1, 0, 0, 0)
        time.sleep(0.5)
        
        # Test 16: LED Test (BLUE)
        logger._log('>>> Please observe the robot LED <<<')
        results['led_blue'] = test_set_led(conn, logger, Port.BOARD_LED_1, 0, 0, 255)
        time.sleep(2)
        
        # Turn off LED
        test_set_led(conn, logger, Port.BOARD_LED_1, 0, 0, 0)
        time.sleep(0.5)
        
        # Test 17: Buzzer Test
        logger._log('>>> Please listen for the buzzer <<<')
        results['buzzer'] = test_set_buzzer(conn, logger, 440, 500)
        time.sleep(1)
        
        # Test 18: Motor Test (very low speed)
        logger._log('>>> Please observe motor movement <<<')
        logger._log('>>> WARNING: Very low speed for safety <<<')
        results['motor_forward_slow'] = test_set_move(conn, logger, 20, 20)
        time.sleep(2)
        
        # Stop motors
        test_set_move(conn, logger, 0, 0)
        time.sleep(0.5)
        
        # Test 19: Motor Test (backward, very low speed)
        logger._log('>>> Please observe motor movement <<<')
        results['motor_backward_slow'] = test_set_move(conn, logger, -20, -20)
        time.sleep(2)
        
        # Stop motors
        test_set_move(conn, logger, 0, 0)
        time.sleep(0.5)
        
        # Test 20: Gyro (may not be connected)
        results['gyro'] = test_gyro(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 21: Color (may not be connected)
        results['color'] = test_color(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 22: Touch Button (may not be connected)
        results['touch_button'] = test_touch_button(conn, logger, port=1)
        time.sleep(0.5)
        
        # Test 23: Rocker (may not be connected)
        results['rocker'] = test_rocker(conn, logger, port=1)
        time.sleep(0.5)
        
        # Close connection
        conn.close()
        logger._log(f'Connection closed: {not conn.is_open}')
        
    except Exception as e:
        logger.log_error(f'Exception: {e}')
        import traceback
        logger._log(traceback.format_exc())
    
    # Log summary
    logger.log_section('TEST SUMMARY')
    summary = logger.get_summary()
    logger._log(f'Total packets: {summary["total_packets"]}')
    logger._log(f'TX packets: {summary["tx_packets"]}')
    logger._log(f'RX packets: {summary["rx_packets"]}')
    logger._log(f'Log file: {summary["log_file"]}')
    logger._log('')
    logger._log('Results:')
    for key, value in results.items():
        logger._log(f'  {key}: {value}')
    
    return {
        'results': results,
        'summary': summary,
        'log_file': summary['log_file'],
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QScout Phase 3B Validation')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--auto', action='store_true', help='Run automatically without prompt')
    args = parser.parse_args()
    
    print('=== QScout Phase 3B Physical Validation ===')
    print(f'Port: {args.port}')
    print('')
    
    if not args.auto:
        print('IMPORTANT: Please ensure the robot is connected and powered on.')
        print('The test will control LEDs, buzzer, and motors at low speed.')
        print('')
        try:
            input('Press Enter to start tests...')
        except EOFError:
            pass
        print('')
    
    results = run_all_tests(args.port)
    
    print('')
    print('=== Tests Complete ===')
    print(f'Log file: {results["log_file"]}')
    print('Please review the log file for detailed packet analysis.')
