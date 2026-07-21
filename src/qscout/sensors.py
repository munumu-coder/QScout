"""Sensor read operations for Q-Scout.

Each method builds the appropriate GET request via :mod:`qscout.protocol`,
sends it through the :class:`~qscout.connection.Connection`, and parses
the response.
"""

from __future__ import annotations

from .connection import Connection
from . import protocol


class Sensors:
    """High-level sensor reading API.

    All methods accept a *port* argument (see :class:`qscout.protocol.Port`)
    and return *None* if no response is received.
    """

    def __init__(self, conn: Connection, order_manager: protocol.OrderManager) -> None:
        """Initialise with an open :class:`Connection` and an :class:`OrderManager`."""
        self._conn = conn
        self._order_ids = order_manager

    def device_info(self) -> dict | None:
        """Read device hardware and software version (0x01)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_device_info(oid)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_device_info(resp) if resp else None

    def interface_info(self, port: int) -> int | None:
        """Read the sensor type connected to *port* (0x02)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_interface_info(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_interface_info(resp).get('type') if resp else None

    def all_interface_info(self) -> list | None:
        """Read sensor types for all ports (0x03)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_all_interface_info(oid)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_interface_info(resp).get('ports') if resp else None

    def motor_interface_info(self) -> dict | None:
        """Read motor interface info (0x04)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_motor_interface_info(oid)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_motor_interface_info(resp) if resp else None

    def user_interface_info(self) -> list | None:
        """Read user interface info (0x05)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_user_interface_info(oid)
        resp = self._conn.send_receive(pkt)
        if not resp:
            return None
        if len(resp) >= 13:
            return list(resp[4:13])
        return list(resp[4:8]) if len(resp) > 4 else []

    def voltage(self, port: int = 1) -> int | None:
        """Read battery level 0-100% (0xA3)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_voltage(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_voltage(resp) if resp else None

    def ultrasonic(self, port: int) -> int | None:
        """Read ultrasonic distance in mm (0xA1)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_ultrasonic(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_ultrasonic(resp) if resp else None

    def button(self, port: int) -> int | None:
        """Read button state 0/1 (0xA2)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_button(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_button(resp) if resp else None

    def line_value(self, port: int) -> int | None:
        """Read line-following sensor value (0xA4)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_line_value(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_line_value(resp) if resp else None

    def temperature_humidity(self, port: int) -> dict | None:
        """Read temperature and humidity (0xA5)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_temp_humidity(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_temp_humidity(resp) if resp else None

    def light(self, port: int) -> int | None:
        """Read light level 0-1023 (0xA6)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_light(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_light(resp) if resp else None

    def voice(self, port: int) -> int | None:
        """Read sound level (0xA7)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_voice(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_voice(resp) if resp else None

    def infrared(self, port: int) -> int | None:
        """Read PIR motion detection 0/1 (0xA8)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_infrared(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_infrared(resp) if resp else None

    def gyro(self, port: int, gyro_type: int = 0) -> list | None:
        """Read gyroscope XYZ values (0xA9)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_gyro(oid, port, gyro_type)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_gyro(resp) if resp else None

    def color_rgb(self, port: int) -> dict | None:
        """Read RGB color values (0xAA, type=0)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_color(oid, port, 0)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_color_rgb(resp) if resp else None

    def color_grey(self, port: int) -> int | None:
        """Read greyscale value (0xAA, type=1)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_color(oid, port, 1)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_color_grey(resp) if resp else None

    def touch_button(self, port: int) -> list:
        """Read pressed touch buttons (0xAB)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_touch_button(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_touch_button(resp) if resp else []

    def temperature_dual(self, port: int, temp_type: int = 0) -> str | None:
        """Read dual temperature sensor (0xAC)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_temp_dual(oid, port, temp_type)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_temp_dual(resp) if resp else None

    def six_line(self, port: int) -> int | None:
        """Read 6-channel line sensor bitmask (0xAD)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_six_line(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_six_line(resp) if resp else None

    def rocker(self, port: int) -> list | None:
        """Read joystick X/Y values (0xAE)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_rocker(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_rocker(resp) if resp else None

    def flame(self, port: int) -> int | None:
        """Read flame sensor value (0xAF)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_flame(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None

    def gas(self, port: int) -> int | None:
        """Read gas sensor value (0xB0)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_gas(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None

    def spiral_pot(self, port: int) -> int | None:
        """Read spiral potentiometer value (0xB1)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_spiral_pot(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None

    def line_pot(self, port: int) -> int | None:
        """Read line potentiometer value (0xB2)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_line_pot(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None

    def ext_io_input(self, port: int) -> int | None:
        """Read external digital input (0xB4)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_ext_io_input(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint8(resp, 5) if resp else None

    def ext_apc(self, port: int) -> int | None:
        """Read external analog input (0xB5)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_ext_apc(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None

    def ext_temp_humi(self, port: int) -> int | None:
        """Read external temperature+humidity sensor (0xB6)."""
        oid = self._order_ids.create()
        pkt = protocol.build_get_ext_temp_humi(oid, port)
        resp = self._conn.send_receive(pkt)
        return protocol.parse_uint16_be(resp, 5) if resp else None
