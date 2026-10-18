#!/usr/bin/env python3
"""
04_imu_stumble_alert.py — Puppy Code Academy, Phase 2 (Sense) + Phase 5 (Move)
IMU safety watchdog: walks a short patrol, but STOPS immediately if the
robot tilts too far (stumble / tip-over risk).

Concepts covered:
  - Subscribing to the IMU topic /ros_robot_controller/imu_raw
  - Reading orientation from a quaternion, computing tilt angles
  - Safety-first design: a sensor reading can veto a motion command

Run:
  Terminal 1:  ros2 launch puppy_control puppy_control.launch.py
  Terminal 2:  python3 04_imu_stumble_alert.py

Try it: gently lift one side of the walking robot — it should stop.
"""

import math
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from puppy_control_msgs.msg import Velocity

WALK_SPEED = 5.0
TURN_SPEED = 0.3
PATROL_TIME = 3.0
TILT_LIMIT_DEG = 30.0   # stop if tilted past this
STOP_HOLD = 0.5


def tilt_degrees(orientation) -> float:
    """Roll/pitch tilt from an IMU quaternion (orientation field)."""
    x, y, z, w = orientation.x, orientation.y, orientation.z, orientation.w
    # Roll (rotation about X) and pitch (rotation about Y)
    sinr = 2.0 * (w * x + y * z)
    cosr = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr, cosr)
    sinp = 2.0 * (w * y - z * x)
    pitch = math.asin(max(-1.0, min(1.0, sinp)))
    return math.degrees(max(abs(roll), abs(pitch)))


class ImuStumbleAlert(Node):
    def __init__(self):
        super().__init__("puppycode_imu_stumble_alert")
        self.pub = self.create_publisher(Velocity, "/puppy_control/velocity", 10)
        self.sub = self.create_subscription(Imu, "/ros_robot_controller/imu_raw",
                                            self.imu_callback, 10)
        self.last_tilt = 0.0
        self.stumble = False

    def imu_callback(self, msg: Imu):
        self.last_tilt = tilt_degrees(msg.orientation)
        if self.last_tilt > TILT_LIMIT_DEG and not self.stumble:
            self.stumble = True
            self.get_logger().warn(
                f"⚠️ TILT {self.last_tilt:.0f}° > {TILT_LIMIT_DEG}° — STOPPING!"
            )
            self.stop()

    def publish(self, x=0.0, yaw_rate=0.0):
        msg = Velocity()
        msg.x = float(x)
        msg.y = 0.0
        msg.yaw_rate = float(yaw_rate)
        self.pub.publish(msg)

    def stop(self):
        self.publish(0.0, 0.0)

    def move(self, x=0.0, yaw_rate=0.0, duration=1.0):
        if self.stumble:
            return False
        self.publish(x, yaw_rate)
        # Monitor tilt while moving in small slices
        elapsed = 0.0
        slice_s = 0.1
        while elapsed < duration and not self.stumble:
            time.sleep(slice_s)
            elapsed += slice_s
            rclpy.spin_once(self, timeout_sec=0.0)
        self.stop()
        return not self.stumble


def main():
    rclpy.init()
    node = ImuStumbleAlert()

    try:
        print(f"🐾 Slow patrol with IMU watchdog (stop past {TILT_LIMIT_DEG}° tilt).")
        while not node.stumble:
            print("Walking forward...")
            if not node.move(x=WALK_SPEED, duration=PATROL_TIME):
                break
            print("Turning left...")
            if not node.move(yaw_rate=TURN_SPEED, duration=1.0):
                break
        if node.stumble:
            print(f"🛑 Robot stopped at {node.last_tilt:.0f}° tilt. "
                  "Set it upright and rerun to continue.")
    except KeyboardInterrupt:
        print("\nInterrupted — stopping safely.")
    finally:
        node.stop()
        time.sleep(STOP_HOLD)
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
