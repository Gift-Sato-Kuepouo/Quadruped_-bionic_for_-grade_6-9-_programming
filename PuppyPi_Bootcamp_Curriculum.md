# 🐾 PUPPY CODE ACADEMY

### A K–12 AI & Robotics Bootcamp Powered by the PuppyPi Quadruped (Raspberry Pi 5)

> *[IMAGE 1: PuppyPi Advanced Kit — bionic quadruped robot with Raspberry Pi 5, shown in walking pose]*
> *(Insert photo here: `tio.png` — captured with a model that supports image input)*
>
> **Robot:** PuppyPi Robot Dog — AI Embodied Intelligence, ROS quadruped with vision, voice understanding, SLAM mapping & navigation.
> **Reference repo:** https://github.com/Gift-Sato-Kuepouo/Quadruped_-bionic_for_-grade_6-9-_programmin

---

## 1. ELEVATOR PITCH (Interview-Ready, 30 seconds)

> "Puppy Code Academy is a scaffolded K–12 bootcamp where students earn the skills — coding, electronics, IoT, and machine learning — one module at a time, until they can build and program their own AI robot dog. Instead of handing kids a robot and saying 'have fun,' we reverse-engineer the journey: every concept is learned by making something small work, then combined into a capstone where the PuppyPi walks, senses, maps, and responds to voice. Students leave with a portfolio, a physical robot they understand line-by-line, and industry-relevant skills in Python, ROS, sensors, and edge ML."

---

## 2. PROGRAM PHILOSOPHY

| Principle | What it means in practice |
|---|---|
| **Scaffold, don't dump** | No student touches the robot until they've passed "micro-wins" in each skill domain |
| **Build to learn** | Every lesson produces a running artifact (a blink, a sensor read, a dashboard) |
| **Turtle-to-quadruped** | Literally: virtual turtle bots → wheeled robots → legs |
| **Age-tiered pathways** | K–2 (block-based), 3–5 (block → text transition), 6–9 (full text/ROS — matches your repo), 9–12 (advanced ML/SLAM) |
| **Portfolio-driven assessment** | Badge system + GitHub-style project portfolio, not exams |

---

## 3. THE SKILL LADDER (How students reach the capstone)

```
STAGE 6  ★ CAPSTONE: PuppyPi Autonomous Companion        (Weeks 11–12)
           │  integrates everything below
STAGE 5  Robotics & ROS: gait, servos, SLAM, navigation (Weeks 9–10)
           │
STAGE 4  Machine Learning & Vision: classification,
         gesture recognition, voice commands             (Weeks 7–8)
           │
STAGE 3  IoT & Cloud: MQTT, dashboards, remote telemetry (Weeks 5–6)
           │
STAGE 2  Sensors & Electronics: GPIO, ultrasonic, IMU,
         camera, actuators                               (Weeks 3–4)
           │
STAGE 1  Programming Fundamentals: variables, loops,
         functions in Python (Scratch for K–2)           (Weeks 1–2)
           │
STAGE 0  Digital literacy & computational thinking       (Pre-camp)
```

**Key idea for interviews:** *"Each stage's output becomes the next stage's input. Sensor readings feed IoT dashboards; classified images feed robot behaviors; ROS ties it into the capstone. Nothing is taught in isolation."*

---

## 4. DETAILED CURRICULUM — 12-WEEK BOOTCAMP

*(2 sessions/week × 2 hours = 48 contact hours + capstone showcase)*

### 📘 PHASE 1 — CODE (Weeks 1–2)

| Week | Topic | Build Project | Skill Gained |
|---|---|---|---|
| 1 | Sequences, variables, loops, conditionals (Python or Scratch Jr. track) | Virtual pet that responds to inputs | Computational thinking |
| 2 | Functions, debugging, events | Text-based game + "robot" simulator in browser | Python syntax, problem solving |

**Milestone Badge:** `PYTHON_EXPLORER` — student debugs a broken function unprompted.

**Starter code sample (Week 1):**

```python
# Virtual Puppy — Week 1
energy = 100
commands = ["walk", "sit", "bark", "rest"]

def respond(command):
    global energy
    if command == "walk" and energy >= 10:
        energy -= 10
        print("🐾 Puppy trots in a circle!")
    elif command == "bark":
        print("Woof! Woof!")
    elif command == "sit":
        print("Puppy sits obediently.")
    elif command == "rest":
        energy = min(100, energy + 20)
        print("Puppy naps. Energy:", energy)
    else:
        print("Puppy is too tired...")

for c in commands:
    respond(c)
```

---

### 📗 PHASE 2 — SENSE (Weeks 3–4)

| Week | Topic | Build Project | Skill Gained |
|---|---|---|---|
| 3 | What is a sensor? GPIO, breadboard LEDs, ultrasonic distance | "Alarm" program: LED + buzzer when object is < 20 cm | Circuit logic, digital I/O |
| 4 | IMU (accelerometer/gyro), servo motors, camera capture | Tilt-servo controller; snapshot-to-file script | Analog/digital data, actuation, PWM |

**Milestone Badge:** `SENSOR_SMITH` — student wires and reads 2 sensors without a diagram.

**Starter code sample (Week 3 — Raspberry Pi GPIO):**

```python
# Proximity Alarm — Week 3
import RPi.GPIO as GPIO
import time

TRIG, ECHO, BUZZER = 17, 27, 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

def distance_cm():
    GPIO.output(TRIG, True); time.sleep(0.00001); GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0: pulse_start = time.time()
    while GPIO.input(ECHO) == 1: pulse_end = time.time()
    return (pulse_end - pulse_start) * 17150

try:
    while True:
        d = distance_cm()
        print(f"Distance: {d:.1f} cm")
        GPIO.output(BUZZER, d < 20)
        time.sleep(0.3)
finally:
    GPIO.cleanup()
```

---

### 📙 PHASE 3 — CONNECT (IoT) (Weeks 5–6)

| Week | Topic | Build Project | Skill Gained |
|---|---|---|---|
| 5 | Networking basics, MQTT publish/subscribe, topics | Send sensor readings to a local broker (Mosquitto) | Pub/sub architecture, protocols |
| 6 | Cloud dashboards (Node-RED / Grafana), Wi-Fi, security basics | Live "Robot Health" dashboard: battery, distance, temp | Data visualization, IoT pipelines |

**Milestone Badge:** `IOT_ARCHITECT` — dashboard updates live from a remote Pi.

**Cross-link:** Students now *see* their sensor data from Phase 2 flowing to the cloud.

**Starter code sample (Week 5 — MQTT telemetry):**

```python
# Robot Telemetry — Week 5
import paho.mqtt.client as mqtt
import json, random, time

client = mqtt.Client("puppy_01")
client.connect("localhost", 1883)

while True:
    telemetry = {
        "battery": round(random.uniform(70, 100), 1),
        "distance_cm": round(random.uniform(10, 200), 1),
        "temperature_c": round(random.uniform(30, 45), 1),
    }
    client.publish("puppy/telemetry", json.dumps(telemetry))
    print("Sent:", telemetry)
    time.sleep(2)
```

**Node-RED flow concept:** `mqtt in (puppy/telemetry) → json → gauge (battery) → chart (distance) → alert (battery < 25%)`

---

### 📕 PHASE 4 — THINK (ML & Vision) (Weeks 7–8)

| Week | Topic | Build Project | Skill Gained |
|---|---|---|---|
| 7 | What is ML? Training vs. inference; Teachable Machine / edge training | Image classifier: 4 hand gestures, 20 samples each | Classification, datasets, overfitting intuition |
| 8 | Voice understanding (speech-to-text, wake words), OpenCV basics | Voice-command parser: "sit", "stand", "forward" | NLP basics, CV pipelines, model deployment on-device |

**Milestone Badge:** `ML_TRAINER` — student improves model accuracy by collecting better data (not by editing code).

**Starter code sample (Week 7 — gesture classification hook):**

```python
# Gesture Classifier Hook — Week 7 (TFLite example)
import numpy as np
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="gestures.tflite")
interpreter.allocate_tensors()
GESTURES = ["open_palm", "fist", "thumbs_up", "peace"]

def classify(frame):
    # frame: preprocessed 224x224 RGB array from the PuppyPi camera
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], frame)
    interpreter.invoke()
    output = interpreter.get_tensor(
        interpreter.get_output_details()[0]["index"])[0]
    return GESTURES[int(np.argmax(output))], float(np.max(output))
```

**Teachable Machine experiment card (hands-on, no code):**
1. Collect 20 samples/class → test accuracy
2. Collect 100 samples/class, varied lighting → test accuracy
3. *Journal question:* "Which mattered more — more data or better data? Why?"

---

### 📓 PHASE 5 — MOVE (Robotics & ROS) (Weeks 9–10)

| Week | Topic | Build Project | Skill Gained |
|---|---|---|---|
| 9 | Quadruped gait theory, inverse kinematics intro, ROS concepts: nodes/topics | PuppyPi: stand, walk, turn via published ROS topics | Robotics control, ROS pub/sub |
| 10 | SLAM mapping + navigation (mapping a room, path planning), obstacle avoidance autonomy | Robot maps classroom and drives a waypoint route | Spatial AI, autonomy integration |

**Milestone Badge:** `ROS_PILOT` — robot completes a mapped waypoint run autonomously.

**Starter code sample (Week 9 — ROS 2 walk command):**

```python
# PuppyPi Walk Command — Week 9 (ROS 2)
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Walker(Node):
    def __init__(self):
        super().__init__("puppy_walker")
        self.pub = self.create_publisher(String, "/puppy/motion", 10)

    def move(self, command: str):
        msg = String(); msg.data = command
        self.pub.publish(msg)
        self.get_logger().info(f"Command sent: {command}")

def main():
    rclpy.init(); walker = Walker()
    for cmd in ["stand", "walk_forward", "turn_left", "walk_forward", "sit"]:
        walker.move(cmd)
        rclpy.spin_once(walker, timeout_sec=2.0)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

**SLAM mini-lesson (Week 10) — conceptual loop:**
```
sensor scan → match to map → update map → plan path → send velocity → repeat
```
Students run the loop with pen-and-paper maps *before* touching the real SLAM stack.

---

### 🏆 PHASE 6 — CAPSTONE (Weeks 11–12)

**Students choose a track and BUILD:**

| Track | Challenge | Skills integrated |
|---|---|---|
| 🗺️ **Explorer** | Autonomous SLAM mapping + waypoint delivery of an object | ROS, SLAM, navigation, gait |
| 🛡️ **Guardian** | Vision + voice-activated sentry: detects person → sends IoT alert → follows | ML, IoT, CV, motion |
| 🎾 **Athlete** | Ball-tracking fetch behavior using CV + gait control | CV, control loops, motion |
| 🎤 **Companion** | ChatGPT/API-driven voice Q&A robot with expressive movements | NLP, API integration, motion |

**Deliverables:**
- Working robot demo (5-minute live run)
- Presentation (why this behavior? what failed? what's next?)
- Code repository (commit history shows iteration)
- Design journal — failures documented count as learning evidence

**Week 11:** Build + iterate (daily stand-ups: "yesterday / today / blocker")
**Week 12:** Polish + showcase event for families, community, and local media

---

## 5. AGE-TIERED ADAPTATIONS

| Track | Ages | Adaptation |
|---|---|---|
| **Sprouts** | K–2 | ScratchJr → virtual PuppyPi on screen; unplugged gait activities (kids *are* the legs: one student = one leg, they choreograph the walk) |
| **Builders** | 3–5 | Scratch → micro:bit sensors → guided PuppyPi demos, block-to-text bridge |
| **Engineers** | 6–9 | Full 12-week track (matches the GitHub repo's grade 6–9 focus) |
| **Researchers** | 9–12 | Add: train custom TF Lite models on-device, ROS2 launch files, compare SLAM algorithms (GMapping vs. Cartographer) |

---

## 6. ASSESSMENT & OUTCOMES

**Badge stack (earn all 6 = "Certified PuppyPi Developer"):**

```
PYTHON_EXPLORER → SENSOR_SMITH → IOT_ARCHITECT → ML_TRAINER → ROS_PILOT → CAPSTONE_DEV
```

**Capstone rubric:**

| Dimension | Weight | What assessors look for |
|---|---|---|
| Functionality | 30% | Robot completes its stated behavior reliably |
| Code quality | 20% | Readable, modular, commented where non-obvious |
| Data/ML justification | 20% | Can explain dataset choices, accuracy, failure cases |
| Presentation | 15% | Clear narrative, handles Q&A |
| Design journal | 15% | Documents failures, iterations, reflections |

**Graduate outcomes:** reads/writes Python, wires sensors, builds an IoT pipeline, trains a classifier, runs ROS nodes, explains SLAM — plus a physical portfolio robot.

---

## 7. KIT & LOGISTICS (Interview trivia-proof)

### Hardware per robot
- PuppyPi Advanced Kit + **Raspberry Pi 5 (4GB)**
- 12× serial bus servos (legs + posture)
- Ultrasonic distance sensor, IMU, camera module
- Battery pack + charger

### Software stack
- Raspberry Pi OS · Python 3 · ROS 2 Humble
- Mosquitto MQTT · Node-RED / Grafana
- OpenCV · TFLite / Teachable Machine
- Gazebo (simulation track for zero-hardware schools)

### Scaling models

| Model | Ratio | Cost impact |
|---|---|---|
| 1:1 | 1 robot/student | ~$4–6K per student (grant/sponsor dependent) |
| Build station (recommended) | 1 robot / 3 students | 60% cost cut; rotational roles: coder, wire-tech, tester |
| Hybrid sim | 1 robot / 6 students + Gazebo | 85% cost cut; every student codes daily in sim, weekly hardware验证 |

### Safety protocol
- Servo torque handling rules (hands clear of joints during motion tests)
- Battery charging procedure (supervised charging station, no overnight on wood)
- Workbench setup checklist + ESD basics
- **Instructor ratio:** 1 lead + 1 floating TA per 12 students

---

## 8. IMPACT METRICS & EVALUATION FRAMEWORK

What gets measured gets funded, improved, and replicated. This framework turns the bootcamp into **evidence** — for grants, school boards, sponsors, and continuous improvement.

### Logic model (theory of change)

```
INPUTS                ACTIVITIES             OUTPUTS              OUTCOMES              IMPACT
─────────            ──────────             ──────              ────────              ──────
Raspberry Pi 5   →   48 hrs of build-  →   Badges earned   →   CS self-efficacy  →   Diverse, durable
PuppyPi kits          based instruction     Capstone demos       Skill mastery          STEM pipeline
Instructors       →   Mentorship       →   Portfolio repos  →   Pathway entry     →   (3–5 yr): more
Funding/grants        & showcases           Showcase events       Persistence            students in
Curriculum        →   IoT/ML/ROS labs  →   Dashboards &     →   Interest in CS/  →    advanced STEM
                      trained models        trained models        robotics careers       coursework &
                                                                                         tech roles
```

### KPI dashboard (per cohort)

| Dimension | Metric | Target | How measured | When |
|---|---|---|---|---|
| **Skill mastery** | Badge completion rate (all 6) | ≥ 80% of completers | Badge tracker | Weekly |
| **Skill mastery** | Pre/post coding assessment score gain | ≥ 40% average gain | 15-min scratch/Python quiz (unplugged + code-reading) | Week 1 vs. Week 12 |
| **Engagement** | Session attendance | ≥ 85% | Sign-in sheet | Per session |
| **Engagement** | Voluntary "after-hours" project time | ≥ 50% of students at least once | Self-report + lab log | Weeks 5–12 |
| **Efficacy** | CS self-efficacy survey (1–5 Likert, 8 items) | ≥ 0.8 point mean increase | Validated short survey | Week 1 vs. Week 12 |
| **Mindset** | Growth mindset items ("I can get better at coding") | ≥ 75% agree/strongly agree | Survey item | Week 12 |
| **Capstone** | Functional demo success (live rubric) | ≥ 70% of teams | Capstone rubric | Week 12 |
| **Capstone** | Presentation Q&A (handles 2 questions) | ≥ 75% of students | Assessor checklist | Week 12 |
| **Pathway** | Enroll in continued activity (club, next camp, competition) within 6 months | ≥ 40% | Follow-up survey | 3 & 6 months post |
| **Equity** | Participation from underrepresented groups & free/reduced-lunch students | ≥ proportional to school demographics | Registration data | Per cohort |

### Assessment instruments (built into the bootcamp, not bolted on)

1. **Pre/Post skills check (15 min, Weeks 1 & 12)**
   - 5 code-reading questions (spot the bug in a loop, predict output)
   - 5 concept questions (what does a sensor do? what is training data?)
   - 1 transfer task: "Explain to a friend how the robot knew to turn."

2. **Weekly exit ticket (2 min, every session)**
   - *Today I built... / Today I got stuck on... / Next time I'll try...*
   - Feeds instructor's Monday planning + Bug Zoo

3. **Design journal rubric (portfolio, graded)**
   - Depth of reflection (0–3), documentation of failed attempts (0–3), connection of skills across phases (0–3)

4. **Capstone rubric** (see Section 6 — Functionality, Code quality, ML justification, Presentation, Journal)

5. **3 & 6-month follow-up survey**
   - Continued activity? Interest in CS careers (yes/unsure/no)? Willingness to mentor next cohort?

### Data pipeline

```
Exit tickets ──┐
Badge tracker ─┼─▶ Cohort dashboard (spreadsheet or lightweight Grafana)
Rubric scores ─┤      │
Surveys pre/post┘      ├─▶ Quarterly impact report (for funders/school board)
                       ├─▶ Curriculum improvement log (which week had lowest exit-ticket confidence?)
                       └─▶ Public anonymized summary (for website/marketing)
```

### Continuous improvement cadence

| When | Action |
|---|---|
| Weekly | Review exit tickets; reteach concepts with < 60% confidence |
| After Week 6 (midpoint) | Check KPI leading indicators (attendance, badge pace); intervene on at-risk students |
| After capstone | Full rubric analysis — which phase's skills were weakest in demos? |
| 2 weeks post-cohort | Instructor debrief; write "lessons learned" into curriculum changelog |
| 3 & 6 months | Pathway follow-up; update recruitment targets |

### Reporting templates (for grants & boards)

**One-page cohort impact report:**
```
COHORT: [name/dates]    ENROLLED: [n]    COMPLETED: [n]  ([%])
BADGES EARNED: [avg per student]
PRE→POST SKILL GAIN: [x]% avg
SELF-EFFICACY GAIN: [+x.x] on 5-pt scale
CAPSTONE DEMOS SUCCESSFUL: [n]/[n] teams
PATHWAY CONTINUATION: [x]% (6-month follow-up)
STUDENT QUOTE: "..."
```

### Why this matters (talking point)

> "We don't just hope the bootcamp works — every session produces data. Exit tickets catch struggling students within a week, pre/post assessments prove skill gains, and 6-month follow-up shows whether we're actually feeding the STEM pipeline. That's how you take a great camp and make it a fundable, replicable program."

---

## 9. 12-WEEK AT-A-GLANCE CALENDAR

```
Wk 1–2   ██ CODE        Python/Scratch fundamentals, virtual pet
Wk 3–4   ██ SENSE       GPIO, ultrasonic, IMU, servo, camera
Wk 5–6   ██ CONNECT     MQTT, Node-RED/Grafana IoT dashboards
Wk 7–8   ██ THINK       ML classification, gestures, voice
Wk 9–10  ██ MOVE        ROS 2 gait control, SLAM, navigation
Wk 11–12 ★★ CAPSTONE   Build, iterate, showcase
```

---

*Puppy Code Academy — because every student should feel what it's like to bring a machine to life with their own code.* 🐾
