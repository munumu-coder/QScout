"""RB protocol implementation for Robobloq Q-Scout.

Header: ``0x52 0x42`` (``"RB"``)
Checksum: ``sum(all_bytes) % 256``
Packet: ``[header 2B][length 1B][orderId 1B][action 1B][payload N][checksum 1B]``

Action codes, payload layouts, and response parsers are defined in
``docs/RB_Protocol_v1.0.md``, originally extracted from MyQode
``app.asar`` -> ``Protocol.js`` (module 99).
"""

from __future__ import annotations

import struct
from enum import IntEnum
from typing import List

HEADER_RB = b'RB'
HEADER = HEADER_RB  # Alias for SDK compatibility
HEADER_LEN = 2
MIN_PACKET_SIZE = 6  # header(2) + length(1) + orderId(1) + action(1) + checksum(1)

MAX_BUFFER_SIZE = 1024  # Prevent unbounded RX buffer growth


class RBPacket:
    """Represents one RB protocol packet.

    Stores only the variable fields: order_id, action, payload.
    Header (0x52 0x42), size, and checksum are computed dynamically
    on serialization (``to_bytes``) to avoid data inconsistency.
    """

    __slots__ = ("order_id", "action", "payload")

    def __init__(self, order_id: int, action: int, payload: bytes = b"") -> None:
        self.order_id = order_id
        self.action = action
        self.payload = payload

    @classmethod
    def from_bytes(cls, data: bytes | bytearray) -> "RBPacket":
        """Parse raw bytes into an RBPacket."""
        order_id, action, payload = parse_packet(data)
        return cls(order_id, action, payload)

    def to_bytes(self) -> bytes:
        """Serialize to wire format (header + size + body + checksum)."""
        return build_packet(self.order_id, self.action, self.payload)

    @property
    def size(self) -> int:
        """Size field value: total bytes in packet."""
        return 6 + len(self.payload)

    def __repr__(self) -> str:
        payload_hex = " ".join(f"{b:02X}" for b in self.payload) or "(empty)"
        return (
            f"RBPacket(order_id={self.order_id}, action=0x{self.action:02X}, "
            f"payload=[{payload_hex}])"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RBPacket):
            return NotImplemented
        return (
            self.order_id == other.order_id
            and self.action == other.action
            and self.payload == other.payload
        )


def _clamp_signed8(v: int) -> int:
    """Clamp *v* to the signed 8-bit range [-128, 127]."""
    return max(-128, min(127, v))


def _clamp_speed(v: int) -> int:
    """Clamp motor speed to [-100, 100] per protocol specification."""
    return max(-100, min(100, v))


class Action(IntEnum):
    """RB action codes extracted from MyQode Protocol.js."""

    GET_DEVICE_INFO = 0x01
    GET_INTERFACE_INFO = 0x02
    GET_ALL_INTERFACE_INFO = 0x03
    GET_MOTOR_INTERFACE_INFO = 0x04
    GET_USER_INTERFACE_INFO = 0x05

    GET_ULTRASONIC = 0xA1
    GET_BUTTON = 0xA2
    GET_VOLTAGE = 0xA3
    GET_LINE_VALUE = 0xA4
    GET_TEMP_HUMIDITY = 0xA5
    GET_LIGHT = 0xA6
    GET_VOICE = 0xA7
    GET_INFRARED = 0xA8
    GET_GYRO = 0xA9
    GET_COLOR = 0xAA
    GET_TOUCH_BUTTON = 0xAB
    GET_TEMP_DUAL = 0xAC
    GET_SIX_LINE = 0xAD
    GET_ROCKER = 0xAE
    GET_FLAME = 0xAF
    GET_GAS = 0xB0
    GET_SPIRAL_POT = 0xB1
    GET_LINE_POT = 0xB2
    GET_EXT_IO_INPUT = 0xB4
    GET_EXT_APC = 0xB5
    GET_EXT_TEMP_HUMI = 0xB6

    SET_LED = 0x10
    SET_MOTOR = 0x11
    SET_ULTRASONIC_LIGHT = 0x12
    SET_BUZZER = 0x13
    SET_MATRIX = 0x14
    LOW_BATTERY = 0x15
    CLICK_BUTTON = 0x16
    SET_WORK_MODE = 0x18
    SET_STEERING_ENGINE = 0x19
    SET_OUT_ENGINE = 0x1A
    SET_RGB_LED_MATRIX = 0x1B
    SET_MP3 = 0x1C
    TOUCH_BUTTON = 0x1D
    SET_FOUR_DIGIT = 0x1E
    SET_FOUR_RGB_LED = 0x1F
    SET_FAN = 0x20
    SET_EXT_IO_OUTPUT = 0x21
    SET_EXT_SERVO_DEGREE = 0x22


class Port:
    """Q-Scout port constants matching MyQode Protocol.js ``ports`` object."""

    BOARD_LED_1 = -4
    BOARD_LED_2 = -5
    BOARD_BUZZER = -6
    BOARD_BUTTON = -7
    INTERFACE_1 = 1
    INTERFACE_2 = 2
    INTERFACE_3 = 3
    INTERFACE_4 = 4
    INTERFACE_5 = 5
    INTERFACE_6 = 6
    INTERFACE_7 = 7
    INTERFACE_8 = 8


class OrderManager:
    """Generates incremental order IDs (2-254) for request/response correlation.

    Order ID 0 is reserved for unsolicited robot reports.
    Order ID 1 is unused.  IDs cycle 2 → 254 → 2.
    """

    def __init__(self) -> None:
        self._next = 2  # Start at 2; 0 and 1 are reserved

    def create(self) -> int:
        """Return the next order ID and advance the counter."""
        order = self._next
        self._next += 1
        if self._next >= 255:
            self._next = 2
        return order


def sum_check(data: bytes) -> int:
    """Compute RB checksum: ``sum(all_bytes) % 256``."""
    return sum(data) % 256


def validate_checksum(packet: bytes | bytearray) -> bool:
    """Return True if the last byte equals the checksum of the rest."""
    if len(packet) < MIN_PACKET_SIZE:
        return False
    return sum_check(packet[:-1]) == packet[-1]


def parse_packet(data: bytes | bytearray) -> tuple[int, int, bytes]:
    """Parse raw bytes into (order_id, action, payload)."""
    from .exceptions import QScoutProtocolError
    if len(data) < MIN_PACKET_SIZE:
        raise QScoutProtocolError(f"Packet too short: {len(data)} bytes")
    if not parse_header(data):
        raise QScoutProtocolError(f"Invalid header: 0x{data[0]:02X} 0x{data[1]:02X}")
    if not parse_checksum_ok(data):
        raise QScoutProtocolError("Checksum mismatch")
    order_id = data[3]
    action = data[4]
    payload = bytes(data[5:-1])
    return order_id, action, payload


def build_packet(order_id: int, action: int, payload: bytes = b'') -> bytes:
    """Build an RB packet with header, length, order, action, payload, and checksum."""
    if not isinstance(order_id, int) or isinstance(order_id, bool):
        raise TypeError(f"order_id must be int, got {type(order_id).__name__}")
    if not isinstance(action, int) or isinstance(action, bool):
        raise TypeError(f"action must be int, got {type(action).__name__}")
    if payload is not None and not isinstance(payload, (bytes, bytearray)):
        raise TypeError(f"payload must be bytes, got {type(payload).__name__}")
    if order_id < 0 or order_id > 254:
        raise ValueError(f"order_id must be 0-254, got {order_id}")
    if action < 0 or action > 255:
        raise ValueError(f"action must be 0-255, got {action}")
    length = HEADER_LEN + 1 + 1 + 1 + len(payload) + 1  # header + len + order + action + payload + checksum
    packet = bytearray()
    packet.extend(HEADER_RB)
    packet.append(length & 0xFF)
    packet.append(order_id & 0xFF)
    packet.append(action & 0xFF)
    packet.extend(payload)
    packet.append(sum_check(bytes(packet)))
    return bytes(packet)


def receive_packet(connection) -> tuple[int, int, bytes]:
    """Read one complete RB packet from *connection* and return (order_id, action, payload).

    *connection* must have a ``receive(size)`` method that returns bytes.
    """
    from .exceptions import QScoutProtocolError, QScoutConnectionError

    header = connection.receive(HEADER_LEN)
    if len(header) < HEADER_LEN:
        raise QScoutConnectionError("No data received")
    if not parse_header(header):
        raise QScoutProtocolError(
            f"Invalid header: 0x{header[0]:02X} 0x{header[1]:02X}"
        )

    length_byte = connection.receive(1)
    if len(length_byte) < 1:
        raise QScoutConnectionError("Incomplete packet: missing length")
    length = length_byte[0]

    remaining_size = length - HEADER_LEN - 1
    if remaining_size < 0:
        raise QScoutProtocolError(f"Invalid length: {length}")

    remaining = connection.receive(remaining_size)
    if len(remaining) < remaining_size:
        raise QScoutConnectionError("Incomplete packet")

    full = header + length_byte + remaining
    order_id, action, payload = parse_packet(full)
    return order_id, action, payload


def parse_header(data: bytes) -> bool:
    """Return *True* if *data* starts with the RB header ``0x52 0x42``."""
    return len(data) >= HEADER_LEN and data[0] == 0x52 and data[1] == 0x42


def parse_order_id(data: bytes) -> int | None:
    """Extract the order ID from an RB packet, or *None* if invalid."""
    if not parse_header(data) or len(data) < 4:
        return None
    return data[3]


def parse_action(data: bytes) -> int | None:
    """Extract the action code from an RB packet, or *None* if invalid."""
    if not parse_header(data) or len(data) < 5:
        return None
    return data[4]


def parse_length(data: bytes) -> int | None:
    """Extract the length field from an RB packet, or *None* if invalid."""
    if not parse_header(data) or len(data) < 3:
        return None
    return data[2]


def parse_checksum_ok(data: bytes) -> bool:
    """Verify the checksum of an RB packet."""
    if len(data) < MIN_PACKET_SIZE:
        return False
    return sum_check(data[:-1]) == data[-1]


def extract_packets(buffer: bytes) -> tuple[List[bytes], bytes]:
    """Extract complete RB packets from a byte buffer.

    Returns:
        A tuple of (list of valid packets, remaining unparsed bytes).
    """
    packets = []
    i = 0
    while i + MIN_PACKET_SIZE <= len(buffer):
        if not parse_header(buffer[i:i + 2]):
            i += 1
            continue
        pkt_len = buffer[i + 2]
        if i + pkt_len > len(buffer):
            break
        pkt = buffer[i:i + pkt_len]
        if parse_checksum_ok(pkt):
            packets.append(pkt)
        i += pkt_len
    return packets, buffer[i:]


def build_set_led(order_id: int, port: int, r: int, g: int, b: int) -> bytes:
    """Build a ``set_led`` (0x10) packet."""
    payload = struct.pack('<bBBB', _clamp_signed8(port), r & 0xFF, g & 0xFF, b & 0xFF)
    return build_packet(order_id, Action.SET_LED, payload)


def build_set_motor(order_id: int, port: int, speed: int) -> bytes:
    """Build a ``set_motor`` (0x11) single-motor packet."""
    payload = struct.pack('<bb', _clamp_signed8(port), _clamp_speed(speed))
    return build_packet(order_id, Action.SET_MOTOR, payload)


def build_set_move(order_id: int, m1_speed: int, m2_speed: int) -> bytes:
    """Build a ``set_motor`` (0x11) dual-motor packet."""
    payload = struct.pack('<bbb', 0, _clamp_speed(m1_speed), _clamp_speed(m2_speed))
    return build_packet(order_id, Action.SET_MOTOR, payload)


def build_set_ultrasonic_light(order_id: int, port: int, r: int, g: int, b: int) -> bytes:
    """Build a ``set_ultrasonic_light`` (0x12) packet."""
    payload = struct.pack('<bBBB', _clamp_signed8(port), r & 0xFF, g & 0xFF, b & 0xFF)
    return build_packet(order_id, Action.SET_ULTRASONIC_LIGHT, payload)


def build_set_buzzer(order_id: int, port: int, frequency: int, duration_ms: int) -> bytes:
    """Build a ``set_buzzer`` (0x13) packet."""
    payload = struct.pack('<BHH', port & 0xFF, frequency & 0xFFFF, duration_ms & 0xFFFF)
    return build_packet(order_id, Action.SET_BUZZER, payload)


def build_set_matrix(order_id: int, port: int, rows: list[int]) -> bytes:
    """Build a ``set_matrix`` (0x14) packet for a 5x10 LED matrix."""
    payload = bytearray([port & 0xFF])
    for row in rows[:10]:
        payload.extend(struct.pack('>H', row & 0xFFFF))
    while len(payload) < 21:
        payload.extend(b'\x00\x00')
    return build_packet(order_id, Action.SET_MATRIX, bytes(payload))


def build_set_work_mode(order_id: int, port: int, mode: int, value: int) -> bytes:
    """Build a ``set_work_mode`` (0x18) packet."""
    payload = struct.pack('<bBB', _clamp_signed8(port), mode & 0xFF, value & 0xFF)
    return build_packet(order_id, Action.SET_WORK_MODE, payload)


def build_set_steering_engine(order_id: int, port: int, engine: int, angle_a: int, angle_b: int) -> bytes:
    """Build a ``set_Steering_engine`` (0x19) packet."""
    payload = struct.pack('<bBBB', _clamp_signed8(port), engine & 0xFF, angle_a & 0xFF, angle_b & 0xFF)
    return build_packet(order_id, Action.SET_STEERING_ENGINE, payload)


def build_set_out_engine(order_id: int, port: int, engine: int, speed_a: int, speed_b: int) -> bytes:
    """Build a ``set_Out_engine`` (0x1A) packet."""
    payload = struct.pack('<bBbb', _clamp_signed8(port), engine & 0xFF,
                          _clamp_speed(speed_a), _clamp_speed(speed_b))
    return build_packet(order_id, Action.SET_OUT_ENGINE, payload)


def build_set_rgb_led_matrix(order_id: int, port: int, led_data: List[int]) -> bytes:
    """Build a ``set_rgbLedMatrix`` (0x1B) packet for a 12x12 RGB LED matrix."""
    payload = bytearray([_clamp_signed8(port)])
    payload.extend(bytes([d & 0xFF for d in led_data[:144]]))
    while len(payload) < 145:
        payload.append(0)
    return build_packet(order_id, Action.SET_RGB_LED_MATRIX, bytes(payload))


def build_set_mp3(order_id: int, port: int, source: int, command: int, param: int) -> bytes:
    """Build a ``set_mp3_sensor`` (0x1C) packet."""
    payload = struct.pack('<bBBB', _clamp_signed8(port), source & 0xFF, command & 0xFF, param & 0xFF)
    return build_packet(order_id, Action.SET_MP3, payload)


def build_set_fan(order_id: int, port: int, speed: int, direction: int) -> bytes:
    """Build a ``set_fan`` (0x20) packet."""
    payload = struct.pack('<bBb', _clamp_signed8(port), speed & 0xFF, max(-1, min(1, direction)))
    return build_packet(order_id, Action.SET_FAN, payload)


def build_set_ext_servo_degree(order_id: int, port: int, degree: int) -> bytes:
    """Build a ``set_ext_servo_degree`` (0x22) packet."""
    payload = struct.pack('<bB', _clamp_signed8(port), degree & 0xFF)
    return build_packet(order_id, Action.SET_EXT_SERVO_DEGREE, payload)


def build_set_ext_io_output(order_id: int, port: int, status: int) -> bytes:
    """Build a ``set_ext_IO_output`` (0x21) packet."""
    payload = struct.pack('<bb', _clamp_signed8(port), max(0, min(1, status)))
    return build_packet(order_id, Action.SET_EXT_IO_OUTPUT, payload)


def build_set_four_digit(order_id: int, port: int, d1: int, d2: int, d3: int, d4: int) -> bytes:
    """Build a ``control_four_digital_value`` (0x1E) packet."""
    payload = struct.pack('<bBBBB', _clamp_signed8(port), d1 & 0xFF, d2 & 0xFF, d3 & 0xFF, d4 & 0xFF)
    return build_packet(order_id, Action.SET_FOUR_DIGIT, payload)


def build_set_four_rgb_led(order_id: int, port: int, location: int, r: int, g: int, b: int) -> bytes:
    """Build a ``control_four_rgbled`` (0x1F) packet."""
    payload = struct.pack('<bBBBBB', _clamp_signed8(port), location & 0xFF, r & 0xFF, g & 0xFF, b & 0xFF)
    return build_packet(order_id, Action.SET_FOUR_RGB_LED, payload)


def build_get_device_info(order_id: int) -> bytes:
    """Build a ``get_device_info`` (0x01) packet."""
    return build_packet(order_id, Action.GET_DEVICE_INFO)


def build_get_interface_info(order_id: int, port: int) -> bytes:
    """Build a ``get_interface_info`` (0x02) packet."""
    return build_packet(order_id, Action.GET_INTERFACE_INFO, struct.pack('<b', _clamp_signed8(port)))


def build_get_all_interface_info(order_id: int) -> bytes:
    """Build a ``get_all_interface_info`` (0x03) packet."""
    return build_packet(order_id, Action.GET_ALL_INTERFACE_INFO)


def build_get_motor_interface_info(order_id: int) -> bytes:
    """Build a ``get_motor_interface_info`` (0x04) packet."""
    return build_packet(order_id, Action.GET_MOTOR_INTERFACE_INFO)


def build_get_user_interface_info(order_id: int) -> bytes:
    """Build a ``get_user_interface_info`` (0x05) packet."""
    return build_packet(order_id, Action.GET_USER_INTERFACE_INFO)


def build_get_ultrasonic(order_id: int, port: int) -> bytes:
    """Build a ``get_ultrasonic_value`` (0xA1) packet."""
    return build_packet(order_id, Action.GET_ULTRASONIC, struct.pack('<b', _clamp_signed8(port)))


def build_get_button(order_id: int, port: int) -> bytes:
    """Build a ``get_button_info`` (0xA2) packet."""
    return build_packet(order_id, Action.GET_BUTTON, struct.pack('<b', _clamp_signed8(port)))


def build_get_voltage(order_id: int, port: int) -> bytes:
    """Build a ``get_voltage`` (0xA3) packet."""
    return build_packet(order_id, Action.GET_VOLTAGE, struct.pack('<b', _clamp_signed8(port)))


def build_get_line_value(order_id: int, port: int) -> bytes:
    """Build a ``get_Line_value`` (0xA4) packet."""
    return build_packet(order_id, Action.GET_LINE_VALUE, struct.pack('<b', _clamp_signed8(port)))


def build_get_temp_humidity(order_id: int, port: int) -> bytes:
    """Build a ``get_ltemperature_humidity_value`` (0xA5) packet."""
    return build_packet(order_id, Action.GET_TEMP_HUMIDITY, struct.pack('<b', _clamp_signed8(port)))


def build_get_light(order_id: int, port: int) -> bytes:
    """Build a ``get_light_sensor_value`` (0xA6) packet."""
    return build_packet(order_id, Action.GET_LIGHT, struct.pack('<b', _clamp_signed8(port)))


def build_get_voice(order_id: int, port: int) -> bytes:
    """Build a ``get_voice_sensor_value`` (0xA7) packet."""
    return build_packet(order_id, Action.GET_VOICE, struct.pack('<b', _clamp_signed8(port)))


def build_get_infrared(order_id: int, port: int) -> bytes:
    """Build a ``get_infrared_value`` (0xA8) packet."""
    return build_packet(order_id, Action.GET_INFRARED, struct.pack('<b', _clamp_signed8(port)))


def build_get_gyro(order_id: int, port: int, gyro_type: int = 0) -> bytes:
    """Build a ``get_gyro_sensor_value`` (0xA9) packet."""
    return build_packet(order_id, Action.GET_GYRO, struct.pack('<bb', _clamp_signed8(port), gyro_type & 0xFF))


def build_get_color(order_id: int, port: int, color_type: int = 0) -> bytes:
    """Build a ``get_color_sensor_value`` (0xAA) packet."""
    return build_packet(order_id, Action.GET_COLOR, struct.pack('<bb', _clamp_signed8(port), color_type & 0xFF))


def build_get_touch_button(order_id: int, port: int) -> bytes:
    """Build a ``get_touch_button`` (0xAB) packet."""
    return build_packet(order_id, Action.GET_TOUCH_BUTTON, struct.pack('<b', _clamp_signed8(port)))


def build_get_temp_dual(order_id: int, port: int, temp_type: int = 0) -> bytes:
    """Build a ``get_tow_temperature_value`` (0xAC) packet."""
    return build_packet(order_id, Action.GET_TEMP_DUAL, struct.pack('<bb', _clamp_signed8(port), temp_type & 0xFF))


def build_get_six_line(order_id: int, port: int) -> bytes:
    """Build a ``get_six_line_value`` (0xAD) packet."""
    return build_packet(order_id, Action.GET_SIX_LINE, struct.pack('<b', _clamp_signed8(port)))


def build_get_rocker(order_id: int, port: int) -> bytes:
    """Build a ``get_rocker`` (0xAE) packet."""
    return build_packet(order_id, Action.GET_ROCKER, struct.pack('<b', _clamp_signed8(port)))


def build_get_flame(order_id: int, port: int) -> bytes:
    """Build a ``get_flame_sensor`` (0xAF) packet."""
    return build_packet(order_id, Action.GET_FLAME, struct.pack('<b', _clamp_signed8(port)))


def build_get_gas(order_id: int, port: int) -> bytes:
    """Build a ``get_gas_sensor`` (0xB0) packet."""
    return build_packet(order_id, Action.GET_GAS, struct.pack('<b', _clamp_signed8(port)))


def build_get_spiral_pot(order_id: int, port: int) -> bytes:
    """Build a ``get_spiral_potentiometer`` (0xB1) packet."""
    return build_packet(order_id, Action.GET_SPIRAL_POT, struct.pack('<b', _clamp_signed8(port)))


def build_get_line_pot(order_id: int, port: int) -> bytes:
    """Build a ``get_linePotentiometer_sensor`` (0xB2) packet."""
    return build_packet(order_id, Action.GET_LINE_POT, struct.pack('<b', _clamp_signed8(port)))


def build_get_ext_io_input(order_id: int, port: int) -> bytes:
    """Build a ``get_ext_IO_input`` (0xB4) packet."""
    return build_packet(order_id, Action.GET_EXT_IO_INPUT, struct.pack('<b', _clamp_signed8(port)))


def build_get_ext_apc(order_id: int, port: int) -> bytes:
    """Build a ``get_ext_APC`` (0xB5) packet."""
    return build_packet(order_id, Action.GET_EXT_APC, struct.pack('<b', _clamp_signed8(port)))


def build_get_ext_temp_humi(order_id: int, port: int) -> bytes:
    """Build a ``get_ext_tempandHumi`` (0xB6) packet."""
    return build_packet(order_id, Action.GET_EXT_TEMP_HUMI, struct.pack('<b', _clamp_signed8(port)))


def parse_device_info(data: bytes) -> dict:
    """Parse a ``get_device_info`` response into ``{action, hw_version, sw_version}``."""
    if len(data) < 7:
        return {}
    return {'action': data[4], 'hw_version': data[5], 'sw_version': data[6]}


def parse_interface_info(data: bytes) -> dict:
    """Parse a ``get_interface_info`` response."""
    if len(data) < 5:
        return {}
    if len(data) >= 14:
        return {'ports': list(data[4:14])}
    return {'type': data[4]}


def parse_motor_interface_info(data: bytes) -> dict:
    """Parse a ``get_motor_interface_info`` response into ``{motor_a, motor_b}``."""
    if len(data) < 6:
        return {}
    return {'motor_a': data[4], 'motor_b': data[5]}


def parse_voltage(data: bytes) -> int | None:
    """Parse battery level (0-100%) from a ``get_voltage`` response."""
    if len(data) < 6:
        return None
    return data[5]


def parse_ultrasonic(data: bytes) -> int | None:
    """Parse distance in mm from a ``get_ultrasonic_value`` response."""
    if len(data) < 7:
        return None
    return data[5] * 256 + data[6]


def parse_button(data: bytes) -> int | None:
    """Parse button state (0/1) from a ``get_button_info`` response."""
    if len(data) < 6:
        return None
    return data[5]


def parse_line_value(data: bytes) -> int | None:
    """Parse line sensor value from a ``get_Line_value`` response."""
    if len(data) < 6:
        return None
    return data[5]


def parse_temp_humidity(data: bytes) -> dict | None:
    """Parse temperature and humidity from a ``get_ltemperature_humidity_value`` response."""
    if len(data) < 9:
        return None
    humidity = float(f'{data[5]}.{data[6]}')
    temperature = float(f'{data[7]}.{data[8]}')
    return {'temperature': temperature, 'humidity': humidity}


def parse_light(data: bytes) -> int | None:
    """Parse light level (0-1023) from a ``get_light_sensor_value`` response."""
    if len(data) < 7:
        return None
    return data[5] * 256 + data[6]


def parse_voice(data: bytes) -> int | None:
    """Parse sound level from a ``get_voice_sensor_value`` response."""
    if len(data) < 7:
        return None
    return data[5] * 256 + data[6]


def parse_infrared(data: bytes) -> int | None:
    """Parse PIR motion (0/1) from a ``get_infrared_value`` response."""
    if len(data) < 6:
        return None
    return data[5]


def parse_gyro(data: bytes) -> list | None:
    """Parse gyroscope XYZ values from a ``get_gyro_sensor_value`` response."""
    if len(data) < 15:
        return None
    x_sign = data[6]
    x_val = data[7] * 256 + data[8]
    y_sign = data[9]
    y_val = data[10] * 256 + data[11]
    z_sign = data[12]
    z_val = data[13] * 256 + data[14]
    x = x_val // 100 * (-1 if x_sign else 1)
    y = y_val // 100 * (-1 if y_sign else 1)
    z = z_val // 100 * (-1 if z_sign else 1)
    return [x, y, z]


def parse_color_rgb(data: bytes) -> dict | None:
    """Parse RGB color values from a ``get_color_sensor_value`` response."""
    if len(data) < 14:
        return None
    return {
        'r': data[6] * 256 + data[7],
        'g': data[8] * 256 + data[9],
        'b': data[10] * 256 + data[11],
        'clear': data[12] * 256 + data[13],
    }


def parse_color_grey(data: bytes) -> int | None:
    """Parse greyscale value from a ``get_color_sensor_value`` response."""
    if len(data) < 8:
        return None
    return data[6] * 256 + data[7]


def parse_touch_button(data: bytes) -> list:
    """Parse pressed button indices from a ``get_touch_button`` response."""
    if len(data) < 7:
        return []
    param = (data[5] * 256 + data[6]) // 2
    buttons = []
    i = 1
    while param:
        if param & 1:
            buttons.append(i)
        param >>= 1
        i += 1
    return buttons


def parse_temp_dual(data: bytes) -> str | None:
    """Parse dual temperature value from a ``get_tow_temperature_value`` response."""
    if len(data) < 8:
        return None
    sign = '' if data[5] else '-'
    value = (data[6] * 256 + data[7]) / 100.0
    return f'{sign}{value:.2f}'


def parse_six_line(data: bytes) -> int | None:
    """Parse 6-channel line sensor bitmask from a ``get_six_line_value`` response."""
    if len(data) < 6:
        return None
    return data[5]


def parse_rocker(data: bytes) -> list | None:
    """Parse joystick X/Y values from a ``get_rocker`` response."""
    if len(data) < 11:
        return None
    x_sign = data[5]
    x_val = data[6] * 256 + data[7]
    x = -x_val if x_sign == 2 else x_val
    y_sign = data[8]
    y_val = data[9] * 256 + data[10]
    y = -y_val if y_sign == 2 else y_val
    return [x, y]


def parse_uint16_be(data: bytes, offset: int) -> int | None:
    """Read a big-endian uint16 from *data* at *offset*, or *None* if too short."""
    if len(data) < offset + 2:
        return None
    return data[offset] * 256 + data[offset + 1]


def parse_uint8(data: bytes, offset: int) -> int | None:
    """Read a uint8 from *data* at *offset*, or *None* if too short."""
    if len(data) < offset + 1:
        return None
    return data[offset]
