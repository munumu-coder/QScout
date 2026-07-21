"""Actuator control operations for Q-Scout.

Provides methods to control motors, LEDs, buzzer, matrix displays,
servos, fans, and other actuators via SET commands.  All methods
build packets through :mod:`qscout.protocol` and send them via
:class:`~qscout.connection.Connection`.
"""

from __future__ import annotations

from .connection import Connection
from . import protocol


class Actuators:
    """High-level actuator control API.

    All methods are fire-and-forget (no response expected).
    """

    def __init__(self, conn: Connection, order_manager: protocol.OrderManager) -> None:
        """Initialise with an open :class:`Connection` and an :class:`OrderManager`."""
        self._conn = conn
        self._order_ids = order_manager

    def led(self, port: int, r: int, g: int, b: int) -> None:
        """Set LED colour (0x10)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_led(oid, port, r, g, b)
        self._conn.send(pkt)

    def motor(self, port: int, speed: int) -> None:
        """Set single motor speed (0x11)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_motor(oid, port, speed)
        self._conn.send(pkt)

    def move(self, m1_speed: int, m2_speed: int) -> None:
        """Set both motors simultaneously (0x11 dual mode)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_move(oid, m1_speed, m2_speed)
        self._conn.send(pkt)

    def forward(self, speed: int = 150) -> None:
        """Drive both motors forward."""
        self.move(speed, speed)

    def backward(self, speed: int = 150) -> None:
        """Drive both motors backward."""
        self.move(-speed, -speed)

    def turn_left(self, speed: int = 150) -> None:
        """Turn left (left motor reverse, right motor forward)."""
        self.move(-speed, speed)

    def turn_right(self, speed: int = 150) -> None:
        """Turn right (left motor forward, right motor reverse)."""
        self.move(speed, -speed)

    def stop(self) -> None:
        """Stop both motors."""
        self.move(0, 0)

    def ultrasonic_light(self, port: int, r: int, g: int, b: int) -> None:
        """Set ultrasonic sensor LED colour (0x12)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_ultrasonic_light(oid, port, r, g, b)
        self._conn.send(pkt)

    def buzzer(self, frequency: int, duration_ms: int, port: int = -6) -> None:
        """Activate buzzer (0x13)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_buzzer(oid, port, frequency, duration_ms)
        self._conn.send(pkt)

    def beep(self, frequency: int = 440, duration_ms: int = 200) -> None:
        """Emit a short beep on the on-board buzzer."""
        self.buzzer(frequency, duration_ms)

    def matrix(self, port: int, rows: list[int]) -> None:
        """Display pattern on 5x10 LED matrix (0x14)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_matrix(oid, port, rows)
        self._conn.send(pkt)

    def work_mode(self, port: int, mode: int, value: int = 0) -> None:
        """Set work mode (0x18)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_work_mode(oid, port, mode, value)
        self._conn.send(pkt)

    def steering_engine(self, port: int, engine: int, angle_a: int, angle_b: int = 90) -> None:
        """Set servo motor angles (0x19)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_steering_engine(oid, port, engine, angle_a, angle_b)
        self._conn.send(pkt)

    def out_engine(self, port: int, engine: int, speed_a: int, speed_b: int = 0) -> None:
        """Set external DC motor speeds (0x1A)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_out_engine(oid, port, engine, speed_a, speed_b)
        self._conn.send(pkt)

    def rgb_led_matrix(self, port: int, led_data: list[int]) -> None:
        """Display pattern on 12x12 RGB LED matrix (0x1B)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_rgb_led_matrix(oid, port, led_data)
        self._conn.send(pkt)

    def mp3(self, port: int, source: int, command: int, param: int = 0) -> None:
        """Control MP3 module (0x1C)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_mp3(oid, port, source, command, param)
        self._conn.send(pkt)

    def fan(self, port: int, speed: int, direction: int = 1) -> None:
        """Control fan (0x20)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_fan(oid, port, speed, direction)
        self._conn.send(pkt)

    def ext_servo_degree(self, port: int, degree: int) -> None:
        """Set external servo angle (0x22)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_ext_servo_degree(oid, port, degree)
        self._conn.send(pkt)

    def ext_io_output(self, port: int, status: int) -> None:
        """Set external digital output (0x21)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_ext_io_output(oid, port, status)
        self._conn.send(pkt)

    def four_digit(self, port: int, d1: int, d2: int, d3: int, d4: int) -> None:
        """Display four digits on 7-segment display (0x1E)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_four_digit(oid, port, d1, d2, d3, d4)
        self._conn.send(pkt)

    def four_rgb_led(self, port: int, location: int, r: int, g: int, b: int) -> None:
        """Set individual RGB LED colour (0x1F)."""
        oid = self._order_ids.create()
        pkt = protocol.build_set_four_rgb_led(oid, port, location, r, g, b)
        self._conn.send(pkt)
