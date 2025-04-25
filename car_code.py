from machine import Pin, PWM, I2C
import time
import math
from bmp180 import BMP180

# Define motor control pins
in1 = Pin(5, Pin.OUT)   # Right Motor IN1
in2 = Pin(18, Pin.OUT)  # Right Motor IN2
ena = PWM(Pin(4), freq=1000)  # Right Motor Speed Control

in3 = Pin(19, Pin.OUT)  # Left Motor IN3
in4 = Pin(21, Pin.OUT)  # Left Motor IN4
enb = PWM(Pin(15), freq=1000)  # Left Motor Speed Control

# Define RPM sensor pins
rpm_sensor_right = Pin(22, Pin.IN)  # Right wheel RPM sensor
rpm_sensor_left = Pin(23, Pin.IN)   # Left wheel RPM sensor

# Robot Parameters
WHEEL_DIAMETER = 0.065  # 6.5 cm (adjust based on actual wheel size)
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER  # Distance per full wheel rotation
AXLE_LENGTH = 0.15  # Distance between wheels (15 cm)
PULSES_PER_REVOLUTION = 40  # Encoder pulses per full rotation

# Variables for RPM calculation
right_pulse_count = 0
left_pulse_count = 0
movement_log = []  # Stores movements for Dead Reckoning

# BMP180 Sensor Initialization
bus = I2C(scl=Pin(32), sda=Pin(33), freq=100000)  # I2C setup for BMP180 on ESP32
bmp180 = BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

# Function to read BMP180 sensor data
def read_bmp180():
    temp = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude

    print("\n--- BMP180 Sensor Data ---")
    print(f"Temperature: {temp:.2f} °C")
    print(f"Pressure: {p:.2f} Pa")
    print(f"Altitude: {altitude:.2f} m")
    print("--------------------------")

# Interrupt handlers for RPM counting
def count_right_pulse(pin):
    global right_pulse_count
    right_pulse_count += 1

def count_left_pulse(pin):
    global left_pulse_count
    left_pulse_count += 1

# Attach interrupts
rpm_sensor_right.irq(trigger=Pin.IRQ_RISING, handler=count_right_pulse)
rpm_sensor_left.irq(trigger=Pin.IRQ_RISING, handler=count_left_pulse)

# Function to move forward and log movement
def move_forward(speed=800, duration=2, log_movement=True):
    global right_pulse_count, left_pulse_count
    right_pulse_count, left_pulse_count = 0, 0  # Reset counts

    in1.value(1)
    in2.value(0)
    ena.duty(speed)  # Right motor forward

    in3.value(0)
    in4.value(1)
    enb.duty(speed)  # Left motor forward

    time.sleep(duration)
    stop()

    distance = ((right_pulse_count + left_pulse_count) / 2) * (WHEEL_CIRCUMFERENCE / PULSES_PER_REVOLUTION)

    if log_movement:
        movement_log.append(("forward", duration, distance))

# Function to move backward and log movement
def move_backward(speed=800, duration=2, log_movement=True):
    global right_pulse_count, left_pulse_count
    right_pulse_count, left_pulse_count = 0, 0  # Reset counts

    in1.value(0)
    in2.value(1)
    ena.duty(speed)  # Right motor backward

    in3.value(1)
    in4.value(0)
    enb.duty(speed)  # Left motor backward

    time.sleep(duration)
    stop()

    distance = ((right_pulse_count + left_pulse_count) / 2) * (WHEEL_CIRCUMFERENCE / PULSES_PER_REVOLUTION)

    if log_movement:
        movement_log.append(("backward", duration, distance))

# Function to turn left and log movement
def turn_left(speed=800, duration=0.8, log_movement=True):
    in1.value(1)
    in2.value(0)
    ena.duty(speed)  # Right motor forward

    in3.value(1)
    in4.value(0)
    enb.duty(speed)  # Left motor backward

    time.sleep(duration)
    stop()

    if log_movement:
        movement_log.append(("left", duration, 45))

# Function to turn right and log movement
def turn_right(speed=800, duration=0.8, log_movement=True):
    in1.value(0)
    in2.value(1)
    ena.duty(speed)  # Right motor backward

    in3.value(0)
    in4.value(1)
    enb.duty(speed)  # Left motor forward

    time.sleep(duration)
    stop()

    if log_movement:
        movement_log.append(("right", duration, 45))

# Function to stop motors
def stop():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)
    ena.duty(0)
    enb.duty(0)

# Function to return to the starting position using Dead Reckoning
def dead_reckoning():
    print("Returning to start position...")
    while movement_log:
        action, duration, value = movement_log.pop()
        if action == "forward":
            move_backward(duration=duration, log_movement=False)
        elif action == "backward":
            move_forward(duration=duration, log_movement=False)
        elif action == "left":
            turn_right(log_movement=False)  
        elif action == "right":
            turn_left(log_movement=False)

    print("Back at start position!")