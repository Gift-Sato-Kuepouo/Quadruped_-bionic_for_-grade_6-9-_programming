#!/usr/bin/env python3
"""
02_square_patrol.py — Puppy Code Academy, Phase 5 (Move)
Walk a square: forward, turn 90°, repeat 4 times.

This is the "waypoint logic" seed for the capstone Explorer track
(SLAM + navigation). Each side of the square = one waypoint leg.

Run:
  Terminal 1:  ros2 launch puppy_control puppy_control.launch.py
  Terminal 2:  python3 02_square_patrol.py
"""

import time

import rclpy
from rclpy.node import Node
from puppy_control_msgs.msg import Velocity

WALK_SPEED = 5.0
TURN_SPEED = 0.3
LEG_TIME = 2.0        # seconds walking per side — calibrate for your floor
TURN_TIME = 1.0       # seconds to turn ~90° — CALIBRATE on your unit!
STOP_HOLD = 0.5
SIDES = 4


class SquarePatrol(Node):
    def __init__(self):
        super().__init__("puppycode_square_patrol")
        self.pub = self.create_publisher(Velocity, "/puppy_control/velocity", 10)
        time.sleep(1.0)

    def move(self, x=0.0, y=0.0, yaw_rate=0.0, duration=1.0):
        msg = Velocity()
        msg.x = float(x)
        msg.y = float(y)
        msg.yaw_rate = float(yaw_rate)
        self.pub.publish(msg)
        time.sleep(duration)
        self.stop()

    def stop(self):
        msg = Velocity()
        msg.x = 0.0
        msg.y = 0.0
        msg.yaw_rate = 0.0
        self.pub.publish(msg)
        time.sleep(STOP_HOLD)


def main():
    rclpy.init()
    node = SquarePatrol()

    try:
        print(f"🐾 Walking a {SIDES}-sided square.")
        print("   Calibrate LEG_TIME and TURN_TIME for your floor and unit.")
        for side in range(1, SIDES + 1):
            print(f"Side {side}/{SIDES}: forward {LEG_TIME}s")
            node.move(x=WALK_SPEED, duration=LEG_TIME)
            if side < SIDES:
                print(f"Side {side}/{SIDES}: left turn {TURN_TIME}s")
                node.move(yaw_rate=TURN_SPEED, duration=TURN_TIME)
        print("✅ Square complete — robot back at start (ish!)")
    except KeyboardInterrupt:
        print("\nInterrupted — stopping safely.")
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
