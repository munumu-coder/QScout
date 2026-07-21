#!/usr/bin/env python3
"""QScout Full Demo — Official reference example.

Demonstrates the complete workflow for controlling a Q-Scout robot:
  1. Auto-detect the robot on USB
  2. Open the connection
  3. Read device information
  4. Control LEDs
  5. Play a sound
  6. Read a sensor
  7. Move the robot
  8. Stop the robot
  9. Close the connection

Requirements:
  - Q-Scout robot connected via USB
  - Python 3.10+
  - pyserial installed

Usage:
  python examples/full_demo.py
"""

import time
from qscout import QScout
from qscout.connection import Connection
from qscout.protocol import Port


def main():
    # ──────────────────────────────────────────────
    # Step 1: Locate the robot
    # ──────────────────────────────────────────────
    print('=== QScout Full Demo ===')
    print()

    print('Scanning for Q-Scout robot...')
    detected_port = Connection.find_qscout()

    if detected_port is None:
        print('ERROR: Q-Scout not found.')
        print('Make sure the robot is connected via USB.')
        return

    print(f'Robot found on {detected_port}')
    print()

    # ──────────────────────────────────────────────
    # Step 2: Open the connection
    # ──────────────────────────────────────────────
    robot = QScout(port=detected_port)
    robot.connect()

    print(f'Connected: {robot.is_connected()}')
    print()

    try:
        # ──────────────────────────────────────────
        # Step 3: Read device information
        # ──────────────────────────────────────────
        print('--- Device Information ---')
        info = robot.sensors.device_info()
        if info:
            print(f'  Hardware version: {info.get("hw_version")}')
            print(f'  Software version: {info.get("sw_version")}')
        else:
            print('  No response (device may not support this command)')
        print()

        # ──────────────────────────────────────────
        # Step 4: LED control
        # ──────────────────────────────────────────
        print('--- LED Control ---')
        led = Port.BOARD_LED_1  # On-board LED, port -4

        colors = [
            ('RED',    255, 0,   0),
            ('GREEN',  0,   255, 0),
            ('BLUE',   0,   0,   255),
            ('WHITE',  255, 255, 255),
        ]

        for name, r, g, b in colors:
            print(f'  Setting LED to {name}...')
            robot.actuators.led(led, r, g, b)
            time.sleep(0.8)

        # Turn off LED
        print('  Turning LED off...')
        robot.actuators.led(led, 0, 0, 0)
        print()

        # ──────────────────────────────────────────
        # Step 5: Buzzer sound
        # ──────────────────────────────────────────
        print('--- Buzzer ---')
        print('  Beep at 440Hz for 300ms...')
        robot.actuators.beep(440, 300)
        time.sleep(0.5)
        print()

        # ──────────────────────────────────────────
        # Step 6: Read sensor
        # ──────────────────────────────────────────
        print('--- Ultrasonic Sensor (port 1) ---')
        distance = robot.sensors.ultrasonic(Port.INTERFACE_1)
        if distance is not None:
            print(f'  Distance: {distance} mm')
        else:
            print('  No response (sensor may not be connected)')
        print()

        # ──────────────────────────────────────────
        # Step 7: Move the robot
        # ──────────────────────────────────────────
        print('--- Motor Control ---')
        speed = 80  # Valid range: -100 to 100

        print(f'  Moving forward at speed {speed}...')
        robot.actuators.forward(speed)
        time.sleep(1.5)

        # ──────────────────────────────────────────
        # Step 8: Stop the robot
        # ──────────────────────────────────────────
        print('  Stopping...')
        robot.actuators.stop()
        time.sleep(0.5)

        print()

        # ──────────────────────────────────────────
        # Step 9: Close the connection
        # ──────────────────────────────────────────
        print('--- Cleanup ---')

    finally:
        robot.disconnect()
        print(f'Connected: {robot.is_connected()}')
        print()
        print('=== Demo complete ===')


if __name__ == '__main__':
    main()
