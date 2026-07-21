"""QScout — native Python library for Robobloq Q-Scout (RB-00002).

Provides motor, LED, buzzer, and sensor control over USB/UART at 115200 baud
using the RB protocol (see ``docs/RB_Protocol_v1.0.md``).

Usage::

    from qscout import QScout

    robot = QScout()           # auto-detect USB port
    robot.connect()
    robot.actuators.forward(100)
    distance = robot.sensors.ultrasonic(1)
    robot.actuators.stop()
    robot.disconnect()

Or use individual modules::

    from qscout.connection import Connection
    from qscout.sensors import Sensors
    from qscout.actuators import Actuators
"""

from .connection import Connection
from .sensors import Sensors
from .actuators import Actuators
from .protocol import Port, Action, OrderManager, build_set_led, build_set_motor
from .protocol import build_set_move, build_set_buzzer


class QScout:
    """High-level interface to a connected Q-Scout robot.

    Wraps :class:`Connection`, :class:`Sensors`, and :class:`Actuators` into
    a single entry-point.  Supports context-manager protocol.
    """

    def __init__(self, port: str | None = None, baudrate: int = 115200) -> None:
        """Create a QScout instance.

        Args:
            port: Serial device path (e.g. ``/dev/ttyUSB0``).
                  If *None*, auto-detects a CH340-based device.
            baudrate: UART baud rate (default 115200).
        """
        if port is None:
            detected = Connection.find_qscout()
            if detected is None:
                raise ConnectionError('Q-Scout not found. Specify port manually or connect via USB.')
            port = detected
        self._connection = Connection(port, baudrate)
        self._order_ids = OrderManager()
        self.sensors = Sensors(
            self._connection,
            self._order_ids,
        )
        self.actuators = Actuators(self._connection, self._order_ids)

    # -- facade convenience methods ------------------------------------------

    def led(self, port: int, r: int, g: int, b: int) -> None:
        """Set LED colour on *port*."""
        oid = self._order_ids.create()
        self._connection.send(build_set_led(oid, port, r, g, b))

    def motor(self, port: int, speed: int) -> None:
        """Set single motor speed on *port*."""
        oid = self._order_ids.create()
        self._connection.send(build_set_motor(oid, port, speed))

    def move(self, left_speed: int, right_speed: int) -> None:
        """Set both motors simultaneously."""
        oid = self._order_ids.create()
        self._connection.send(build_set_move(oid, left_speed, right_speed))

    def stop(self) -> None:
        """Stop both motors."""
        self.move(0, 0)

    def buzzer(self, frequency: int, duration_ms: int) -> None:
        """Activate the on-board buzzer."""
        oid = self._order_ids.create()
        self._connection.send(build_set_buzzer(oid, 0, frequency, duration_ms))

    def get_ultrasonic(self, port: int) -> int | None:
        """Read ultrasonic distance (mm) from *port*.

        Delegates to :meth:`Sensors.ultrasonic`.
        """
        return self.sensors.ultrasonic(port)

    # -- connection management -----------------------------------------------

    def connect(self) -> None:
        """Open the serial connection to the robot."""
        self._connection.open()

    def disconnect(self) -> None:
        """Close the serial connection."""
        self._connection.close()

    def is_connected(self) -> bool:
        """Return *True* if the serial port is open."""
        return self._connection.is_open

    @property
    def connection(self) -> Connection:
        """Return the underlying :class:`Connection` instance."""
        return self._connection

    def __enter__(self) -> 'QScout':
        self.connect()
        return self

    def __exit__(self, *args) -> None:
        self.disconnect()
