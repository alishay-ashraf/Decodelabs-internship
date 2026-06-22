import csv
import time
import random
from datetime import datetime

# Configuration
LOG_FILE = "sensor_data_log.csv"
SIMULATION_DURATION_SECONDS = 30  # How long the simulation runs
READ_INTERVAL_SECONDS = 2         # Time between sensor readings

def generate_sensor_data():
    """Simulates reading data from physical sensors."""
    # Simulate Temperature between 20.0°C and 25.0°C with slight fluctuations
    temperature = round(random.uniform(20.0, 25.0), 2)
    
    # Simulate Humidity between 40% and 60%
    humidity = round(random.uniform(40.0, 60.0), 1)
    
    # Simulate Motion (0 = No Motion, 1 = Motion Detected)
    # 20% chance of detecting motion at any given second
    motion_detected = 1 if random.random() < 0.2 else 0
    
    return temperature, humidity, motion_detected

def initialize_log_file():
    """Creates the CSV file and writes the header if it doesn't exist."""
    try:
        with open(LOG_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)", "Motion Detected"])
            print(f"[INFO] Created new log file: {LOG_FILE}")
    except FileExistsError:
        print(f"[INFO] Appending to existing log file: {LOG_FILE}")

def main():
    print("=========================================")
    print("      IoT SENSOR SIMULATION STARTED      ")
    print("=========================================")
    
    initialize_log_file()
    
    start_time = time.time()
    
    try:
        # Run simulation for the specified duration
        while time.time() - start_time < SIMULATION_DURATION_SECONDS:
            # 1. Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 2. Simulate sensor concepts (Data Collection)
            temp, hum, motion = generate_sensor_data()
            motion_str = "MOTION DETECTED!" if motion == 1 else "No Motion"
            
            # 3. Display sensor values (Real-time Display)
            print(f"[{current_time}] Temp: {temp}°C | Humidity: {hum}% | Motion: {motion_str}")
            
            # 4. Store/Log the generated data (Data Handling)
            with open(LOG_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time, temp, hum, motion])
            
            # Wait for the next reading
            time.sleep(READ_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n[INFO] Simulation stopped early by user.")
        
    print("=========================================")
    print(f"  Simulation complete. Data saved to {LOG_FILE}  ")
    print("=========================================")

if __name__ == "__main__":
    main()