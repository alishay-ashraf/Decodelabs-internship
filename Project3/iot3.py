import time
from gpiozero import DistanceSensor
from Adafruit_IO import Client, MQTTClient

# --- Adafruit IO Credentials ---
ADAFRUIT_IO_USERNAME = "YOUR_ADAFRUIT_IO_USERNAME"
ADAFRUIT_IO_KEY      = "YOUR_ADAFRUIT_IO_KEY"
FEED_KEY             = "security-distance"

# --- Hardware Setup ---
# gpiozero handles the ultrasonic math automatically.
# Queue_len=1 helps get immediate, real-time readings.
sensor = DistanceSensor(echo=24, trigger=23, queue_len=1)

# --- Initialize Adafruit IO REST Client ---
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

print("Security Node Initialized. Connecting to Adafruit IO...")

try:
    while True:
        # gpiozero returns distance in meters, convert to centimeters
        distance_cm = round(sensor.distance * 100, 1)
        
        # Guard against out-of-range sensor spikes
        if distance_cm < 400:
            print(f"Current Distance: {distance_cm} cm")
            
            try:
                # Publish data to your Adafruit IO feed
                aio.send_data(FEED_KEY, distance_cm)
                print("Telemetry successfully streamed to cloud.")
            except Exception as e:
                print(f"Failed to send data: {e}")
                
        # Throttling rate: Adafruit free tier allows 30 data points per minute
        # Sleeping for 3 seconds keeps us well under the rate limit.
        time.sleep(3)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")