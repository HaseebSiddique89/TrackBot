from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time
from car_code import move_forward, move_backward, turn_left, turn_right, stop  # Import movement functions from the car code

# Define SPI and NRF24L01 Pins for ESP32 MH-ET LIVE
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
csn = Pin(26, mode=Pin.OUT)   # Chip Select
ce = Pin(25, mode=Pin.OUT)   # Chip Enable

# Initialize NRF24L01
nrf = NRF24L01(spi=spi, cs=csn, ce=ce, payload_size=1)
nrf.open_rx_pipe(1, b"1Node")  # Must match transmitter address
nrf.set_power_speed(0, 1)  # Minimum power, 1Mbps speed
nrf.start_listening()

def execute_command(command):
    # Execute movement based on received command
            if command == 'F':
                print("Moving Forward...")
                move_forward(duration=2)
            elif command == 'B':
                print("Moving Backward...")
                move_backward(duration=2)
            elif command == 'L':
                print("Turning Left...")
                turn_left(duration=0.8)
            elif command == 'R':
                print("Turning Right...")
                turn_right(duration=0.8)
            else:
                print("Unknown command received.")

# Loop to listen for commands
while True:
    if nrf.any():
        while nrf.any():
            received = nrf.recv()
            command = received.decode('utf-8').strip()
            print(f"Received: {command}")
            print("Command Received", command)
            execute_command(command)
            

    else:
        print("Waiting for command...")

    time.sleep(0.5)
