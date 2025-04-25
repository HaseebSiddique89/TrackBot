# TrackBot 🚗  
**An IoT-Powered Three-Wheeled Smart Car with Obstacle Detection, Environment Sensing, and NRF Communication**

---

## 📌 Project Overview

**TrackBot** is a three-wheeled, smart IoT car designed to navigate, communicate, and analyze its surroundings in real-time. This innovative robotic vehicle integrates multiple sensing and control technologies to achieve autonomous features such as obstacle detection, environmental monitoring, and message-based control via NRF communication.

It’s equipped with a 360-degree ultrasonic sensor for dynamic obstacle detection, an LCD for real-time feedback, and a BMP180 barometric sensor to measure temperature, humidity, and altitude. The car can be operated via a remote or through message-based commands using NRF transmitters and receivers. It also features **Dead Reckoning** capabilities for estimating position when GPS is unavailable.

---

## 🚀 Features

- 🔄 **360° Obstacle Detection** using a rotating ultrasonic sensor.
- 🧠 **Dead Reckoning** using individual wheel RPM sensors.
- 🛰️ **NRF Communication** for wireless messaging-based control.
- 📡 **Remote-Controlled and Message-Controlled** operation modes.
- 🌡️ **Environmental Monitoring** using BMP180 (Temperature, Humidity, Altitude).
- 📺 **LCD Display** to visualize obstacles and surrounding environment.
- 🔋 **Battery-powered, portable design** with optimized microcontroller logic.

---

## 🧰 Technologies & Components Used

| Component                | Purpose                                  |
|--------------------------|-------------------------------------------|
| **Arduino/ESP Microcontroller** | Main processing unit                     |
| **NRF24L01 Transmitter/Receiver** | Wireless communication between controller and car |
| **Ultrasonic Sensor (HC-SR04)** | Obstacle detection                       |
| **Servo Motor**          | 360° ultrasonic sensor rotation           |
| **BMP180 Barometric Sensor** | Temperature, humidity & altitude sensing |
| **LCD Display (16x2 or I2C)** | Visual feedback and obstacle visualization |
| **DC Motors with Motor Driver** | Movement control                        |
| **Chassis with 3 wheels** | Physical robot body                      |
| **Power Supply / Battery Pack** | Power source                          |

---

## 🛠️ How It Works

1. **NRF Control**: The user sends predefined messages via NRF transmitter, which the car receives using its NRF receiver module. These messages trigger movement commands.
2. **Remote Mode**: Manual control using a remote to operate the car’s movement.
3. **Obstacle Detection**: The ultrasonic sensor continuously rotates 360° using a servo motor, identifying objects in the vicinity. Obstacles are visualized on the LCD.
4. **Environment Sensing**: The BMP180 sensor constantly updates environmental data, which can be shown on the LCD.
5. **Dead Reckoning**: The car estimates its position based on motor rotation and sensor inputs even in GPS-denied areas.

---

Will provide the working video and snaps soon, stay tuned :) 
