from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

# Define SPI and NRF24L01 Pins for ESP32-WROOM-32
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
csn = Pin(4, mode=Pin.OUT)  # Chip Select
ce = Pin(16, mode=Pin.OUT)   # Chip Enable

# Initialize NRF24L01
nrf = NRF24L01(spi, csn, ce, payload_size=32)
nrf.open_tx_pipe(b"1Node")  # Must match receiver address
nrf.set_power_speed(0, 1)  # Minimum power, 1Mbps speed

# Loop to send commands
while True:
    # Get user input for movement command
    movement = input("Enter movement command (forward, backward, left, right): ").strip().lower()

    if movement in ["forward", "backward", "left", "right"]:
        msg = movement.encode('utf-8')  # Send the movement command
        nrf.send(msg)
        print(f"Sent: {msg.decode('utf-8')}")
    else:
        print("Invalid command. Please enter 'forward', 'backward', 'left', or 'right'.")
    
    time.sleep(1)
