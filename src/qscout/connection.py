"""Serial connection to Q-Scout robot over USB.

Uses pyserial to communicate at 115200 baud, 8N1.  Handles packet framing
via :func:`qscout.protocol.extract_packets`.
"""

from __future__ import annotations

import time
from typing import Optional

import serial
import serial.tools.list_ports

from . import protocol
from .protocol import MAX_BUFFER_SIZE


class Connection:
    """Manages a serial connection to the Q-Scout robot.

    Provides low-level ``send`` / ``receive`` as well as automatic
    packet extraction.
    """

    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 115200,
                 timeout: float = 0.5) -> None:
        """Initialise the connection (does not open the port yet).

        Args:
            port: Serial device path.
            baudrate: UART baud rate.
            timeout: Read/write timeout in seconds.
        """
        self._port_name = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._serial: Optional[serial.Serial] = None
        self._rx_buffer = bytearray()

    @staticmethod
    def list_ports() -> list[str]:
        """Return a list of available serial port device paths."""
        return [p.device for p in serial.tools.list_ports.comports()]

    @staticmethod
    def find_qscout() -> Optional[str]:
        """Auto-detect a Q-Scout USB device.

        Detection priority:
        1. VID:PID = 1A86:7523 (CH340 USB-Serial converter)
        2. Description contains 'CH340', 'USB-Serial', or 'USB Serial'

        Returns:
            The device path if found, otherwise *None*.
        """
        # CH340 USB-Serial converter VID:PID
        CH340_VID = 0x1A86
        CH340_PID = 0x7523

        for p in serial.tools.list_ports.comports():
            # Primary: Check VID:PID (most reliable across Linux distributions)
            if hasattr(p, 'vid') and hasattr(p, 'pid'):
                if p.vid == CH340_VID and p.pid == CH340_PID:
                    return p.device

            # Secondary: Check description (fallback)
            desc = (p.description or '').lower()
            if 'ch340' in desc or 'usb-serial' in desc or 'usb serial' in desc:
                return p.device

        return None

    def open(self) -> None:
        """Open the serial port."""
        self._serial = serial.Serial(
            port=self._port_name,
            baudrate=self._baudrate,
            timeout=self._timeout,
            write_timeout=self._timeout,
        )
        self._serial.reset_input_buffer()
        self._rx_buffer.clear()

    def close(self) -> None:
        """Close the serial port."""
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._serial = None
        self._rx_buffer.clear()

    @property
    def is_open(self) -> bool:
        """Return *True* if the serial port is open."""
        return self._serial is not None and self._serial.is_open

    def write(self, data: bytes) -> None:
        """Write raw bytes to the serial port."""
        if not self.is_open:
            raise ConnectionError('Serial port not open')
        self._serial.write(data)
        self._serial.flush()

    def read(self, size: int = 1) -> bytes:
        """Read *size* bytes from the serial port."""
        if not self.is_open:
            raise ConnectionError('Serial port not open')
        return self._serial.read(size)

    def send(self, packet: bytes) -> None:
        """Send an RB packet."""
        try:
            self.write(packet)
        except (serial.SerialException, OSError):
            self._serial = None
            raise ConnectionError('Serial port disconnected during send')

    def receive(self, timeout: float = 0.5) -> Optional[bytes]:
        """Wait for and return the next complete RB packet, or *None* on timeout.

        Prevents infinite loops by checking serial port state and limiting
        buffer growth.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                if not self.is_open:
                    return None
                waiting = self._serial.in_waiting
                if waiting > 0:
                    self._rx_buffer.extend(self._serial.read(waiting))
                    # Prevent unbounded buffer growth
                    if len(self._rx_buffer) > MAX_BUFFER_SIZE:
                        self._rx_buffer = self._rx_buffer[-MAX_BUFFER_SIZE:]
                    packets, remaining = protocol.extract_packets(bytes(self._rx_buffer))
                    self._rx_buffer = bytearray(remaining)
                    if packets:
                        return packets[-1]
                else:
                    time.sleep(0.005)
            except (serial.SerialException, OSError):
                # Serial port disconnected or error
                self._serial = None
                return None
        return None

    def send_receive(self, packet: bytes, timeout: float = 0.5) -> Optional[bytes]:
        """Send an RB packet and wait for the response."""
        self.send(packet)
        return self.receive(timeout)

    def flush(self) -> None:
        """Discard any buffered input data."""
        if self.is_open:
            self._serial.reset_input_buffer()
            self._rx_buffer.clear()
