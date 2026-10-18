#!/usr/bin/env python3
"""
03_color_chaser.py — Puppy Code Academy, Phase 4 (Think) + Phase 5 (Move)
Vision-based color tracking: PuppyPi chases a colored object.

Concepts covered:
  - Subscribing to the camera topic /image_raw (sensor_msgs/Image)
  - OpenCV HSV color detection (same approach as Hiwonder's official
    ROS 2 color tracking course)
  - Proportional control: bigger error -> bigger turn
  - Combined translation + rotation commands on /puppy_control/velocity

Run:
  Terminal 1:  ros2 launch puppy_control puppy_control.launch.py
  Terminal 2:  python3 03_color_chaser.py

Tip: wear a red shirt or hold a red ball. Adjust HSV_LOW/HSV_HIGH
under your room's lighting (Hiwonder docs have a color threshold tool).
"""

import time

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from puppy_control_msgs.msg import Velocity

# --- Target color: RED (two HSV bands because red wraps around hue 0) ---
# Tune these with Hiwonder's threshold tool or a sample OpenCV script.
RED_LOW_1, RED_HIGH_1 = (0, 120, 70), (10, 255, 255)
RED_LOW_2, RED_HIGH_2 = (170, 120, 70), (180, 255, 255)

MIN_AREA = 800          # ignore tiny noise blobs (pixels)
MAX_WALK_SPEED = 5.0    # cm/s forward when target is centered & far enough
KP_TURN = 0.6           # proportional gain for turning (rad/s per pixel error)
STOP_HOLD = 0.5


class ColorChaser(Node):
    def __init__(self):
        super().__init__("puppycode_color_chaser")
        self.bridge = CvBridge()
        self.pub = self.create_publisher(Velocity, "/puppy_control/velocity", 10)
        # Compressed image is lighter on the Pi 5; fall back to raw if needed.
        self.sub = self.create_subscription(
            Image, "/image_raw", self.image_callback, 10
        )
        self.lost_frames = 0
        self.get_logger().info("👀 Looking for red objects... move one into view!")

    def image_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        height, width = frame.shape[:2]
        center_x = width // 2

        # Blur + HSV convert + dual-band threshold (red wraps hue)
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, RED_LOW_1, RED_HIGH_1) | cv2.inRange(
            hsv, RED_LOW_2, RED_HIGH_2
        )

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        valid = [c for c in contours if cv2.contourArea(c) > MIN_AREA]

        if not valid:
            self.lost_frames += 1
            # Stop if target lost for ~1 second (assume 15–30 FPS)
            if self.lost_frames > 20:
                self.stop()
            return

        self.lost_frames = 0
        target = max(valid, key=cv2.contourArea)
        (tx, ty), _ = cv2.minEnclosingCircle(target)
        error = tx - center_x  # pixels; + means target is to the right

        # Proportional steering: bigger error -> bigger turn (rad/s)
        yaw_rate = -KP_TURN * (error / (width / 2))  # negative => turn right
        yaw_rate = max(-0.89, min(0.89, yaw_rate))   # clamp to PuppyPi limit

        # Walk slower as the target gets close to frame bottom (near = big area)
        area = cv2.contourArea(target)
        x_speed = MAX_WALK_SPEED * min(1.0, area / 20000.0)
        if area > 25000:  # very close — just turn, don't walk
            x_speed = 0.0

        self.publish(x=x_speed, yaw_rate=yaw_rate)

    def publish(self, x=0.0, yaw_rate=0.0):
        msg = Velocity()
        msg.x = float(x)
        msg.y = 0.0
        msg.yaw_rate = float(yaw_rate)
        self.pub.publish(msg)

    def stop(self):
        self.publish(0.0, 0.0)
        time.sleep(0.0)  # publish once; robot controller holds last command


def main():
    rclpy.init()
    node = ColorChaser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nInterrupted — stopping safely.")
    finally:
        node.stop()
        time.sleep(STOP_HOLD)
        node.stop()  # belt & suspenders
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
