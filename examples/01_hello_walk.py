#!/usr/bin/env python3
"""
01_hello_walk.py — Puppy Code Academy, Phase 5 (Move)
First walk with the real PuppyPi.

Verified interface (Hiwonder docs):
  Topic : /puppy_control/velocity
  Type  : puppy_control_msgs/msg/Velocity   (fields: x, y, yaw_rate)
  x       -20.0 .. +20.0 cm/s   (official demos use 5.0)
  yaw_rate -0.89 .. +0.89 rad/s (positive = counterclockwise / left turn)

Run:
  Terminal 1:  ros2 launch puppy_control puppy_control.launch.py
  Terminal 2:  python3 01_hello_walk.py
"""

import time

import rclpy
from rclpy.node import Node
from puppy_control_msgs.msg import Velocity

WALK_SPEED = 5.0      # cm/s — official Hiwonder demo speed
TURN_SPEED = 0.3      # rad/s — gentle left turn (~17 deg/s)
STEP_TIME = 0.8       # seconds of walking per step
TURN_TIME = 0.4       # seconds of turning — calibrate on your unit!
STOP_HOLD = 0.5       # always hold zero velocity ≥ 0.5 s


class HelloWalk(Node):
    def __init__(self):
        super().__init__("puppycode_hello_walk")
        self.pub = self.create_publisher(Velocity, "/puppy_control/velocity", 10)
        time.sleep(1.0)  # let subscribers connect before first command

    def move(self, x=0.0, y=0.0, yaw_rate=0.0, duration=1.0):
        """Publish one velocity command, hold it, then STOP (safe by default)."""
        msg = Velocity()
        msg.x = float(x)
        msg.y = float(y)
        msg.yaw_rate = float(yaw_rate)
        self.pub.publish(msg)
        time.sleep(duration)
        self.stop()

    def stop(self):
        """All-zero velocity — the robot settles into standing."""
        msg = Velocity()
        msg.x = 0.0
        msg.y = 0.0
        msg.yaw_rate = 0.0
        self.pub.publish(msg)
        time.sleep(STOP_HOLD)


def main():
    rclpy.init()
    node = HelloWalk()

    try:
        print("🐾 Place PuppyPi on open floor, then watch...")
        print("1) Walking forward (x=5.0 cm/s for 0.8 s)")
        node.move(x=WALK_SPEED, duration=STEP_TIME)

        print("2) Gentle left turn (yaw_rate=+0.3 for 0.4 s)")
        node.move(yaw_rate=TURN_SPEED, duration=TURN_TIME)

        print("3) Walking forward again")
        node.move(x=WALK_SPEED, duration=STEP_TIME)

        print("4) Sit / stop — done! 🐾")
    except KeyboardInterrupt:
        print("\nInterrupted — stopping safely.")
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
