#!/usr/bin/env python3
"""Basic usage examples for QScout library."""

import time
from qscout import QScout
from qscout.connection import Connection


def test_connection():
    """List available serial ports and auto-detect Q-Scout."""
    print('Available ports:', Connection.list_ports())
    detected = Connection.find_qscout()
    print('Auto-detected:', detected)


def example_context_manager():
    """Demonstrate context-manager usage with LED and buzzer."""
    with QScout() as robot:
        print('Connected:', robot.is_connected())

        info = robot.sensors.device_info()
        print('Device info:', info)

        battery = robot.sensors.voltage()
        print('Battery:', battery, '%')

        robot.actuators.beep(440, 200)
        time.sleep(0.3)

        robot.actuators.led(-4, 255, 0, 0)
        time.sleep(1)
        robot.actuators.led(-4, 0, 0, 0)


def example_motors():
    """Demonstrate motor control: forward, backward, turn."""
    with QScout() as robot:
        robot.actuators.forward(100)
        time.sleep(1)
        robot.actuators.stop()

        robot.actuators.backward(100)
        time.sleep(1)
        robot.actuators.stop()

        robot.actuators.turn_left(100)
        time.sleep(0.5)
        robot.actuators.stop()


def example_ultrasonic():
    """Read ultrasonic distance 5 times."""
    with QScout() as robot:
        for _ in range(5):
            dist = robot.sensors.ultrasonic(1)
            print(f'Distance: {dist} mm')
            time.sleep(0.2)


def example_sensors_loop():
    """Read multiple sensors in a loop."""
    with QScout() as robot:
        info = robot.sensors.all_interface_info()
        print('Interface info:', info)

        battery = robot.sensors.voltage()
        print('Battery:', battery)

        light = robot.sensors.light(2)
        print('Light:', light)

        line = robot.sensors.line_value(3)
        print('Line:', line)


if __name__ == '__main__':
    test_connection()
    print()
    example_context_manager()
