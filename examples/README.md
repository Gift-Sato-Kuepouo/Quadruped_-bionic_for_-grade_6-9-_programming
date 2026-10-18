# 🐾 PuppyPi Sample Code (ROS 2)

Real, runnable Python programs for the **Hiwonder PuppyPi** (Raspberry Pi 5, ROS 2 Humble). These use the robot's **verified** interfaces from the official Hiwonder documentation:

| Interface | Topic | Message type |
|---|---|---|
| Motion control | `/puppy_control/velocity` | `puppy_control_msgs/msg/Velocity` (fields: `x`, `y`, `yaw_rate`) |
| Camera | `/image_raw` | `sensor_msgs/msg/Image` |
| IMU | `/ros_robot_controller/imu_raw` | `sensor_msgs/msg/Imu` |

## Motion parameter limits (official Hiwonder spec)

| Parameter | Range | Meaning |
|---|---|---|
| `x` | **-20.0 to +20.0** cm/s | Forward (+) / backward (−) walking speed. Official demos use **5.0**. |
| `y` | -20.0 to +20.0 cm/s | Lateral (sideways) speed. |
| `yaw_rate` | **-0.89 to +0.89** rad/s | Turning speed. Positive = counterclockwise (left turn). 1 rad/s ≈ 57.3°/s. |

## Setup (do this once per session)

1. Power on PuppyPi and connect via VNC (see Hiwonder docs §3.3–3.4).
2. Switch to the **ROS 2** environment using the ROS version switch tool.
3. Open a ROS 2 terminal and start the motion control node:

```bash
ros2 launch puppy_control puppy_control.launch.py
```

4. Open a **second** ROS 2 terminal. This is where you run the examples:

```bash
cd ~/puppypi/examples   # or wherever you copied these files
python3 01_hello_walk.py
```

> The motion control launch file must be running in the first terminal or the robot will not move.

## Safety rules (read before every session)

1. **Clear floor, open space** — at least 2 m of clear area on all sides.
2. **Hands clear of the legs** while a program is running (8 coreless servos have real torque).
3. **Always stop** — every example publishes an all-zero velocity message when it finishes or if you press `Ctrl+C`. Never kill a script with the robot mid-stride without it.
4. **Start slow** — keep `x` at 5.0 until you've watched the robot walk; don't max out 20.0 on day one.
5. **Calibrate turns** — gait timing means short `yaw_rate` bursts can turn more than expected. Test each turn duration in an open area first.

## The examples

| File | Bootcamp phase | What it teaches |
|---|---|---|
| [`01_hello_walk.py`](./01_hello_walk.py) | Phase 5 — Move | Publishing velocity commands: stand → walk → turn → stop |
| [`02_square_patrol.py`](./02_square_patrol.py) | Phase 5 — Move | Sequencing moves into a pattern (waypoint logic for capstone) |
| [`03_color_chaser.py`](./03_color_chaser.py) | Phase 4 — Think | Subscribing to `/image_raw`, OpenCV color detection, steering with proportional control |
| [`04_imu_stumble_alert.py`](./04_imu_stumble_alert.py) | Phase 2/5 | Subscribing to IMU data, safety logic: stop walking if the robot tilts too far |

## No robot handy?

The official PuppyPi repo ships a **Gazebo simulation** (Hiwonder docs §22, ROS 2 Simulation Course) so students can develop `01` and `02` in sim before touching hardware. See https://github.com/Hiwonder/PuppyPi

---

*Sample code for Puppy Code Academy — matched to the Hiwonder PuppyPi v2.0 ROS 2 stack.*
