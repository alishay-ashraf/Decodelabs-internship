import time
import random

def simulate_environment():
    print("--- Smart Environmental Monitor (Python Simulation) ---")
    print("Press Ctrl+C to stop.\n")
    
    while True:
        # Generate random realistic sensor readings
        temperature = round(random.uniform(20.0, 35.0), 1)
        humidity = round(random.uniform(40.0, 70.0), 1)
        
        # Display sensor values (Console acting as the "Serial Monitor")
        print(f"[{time.strftime('%H:%M:%S')}] Temp: {temperature}°C | Humidity: {humidity}%")
        
        # Basic Automation Logic (Task 4)
        if temperature > 30.0:
            print("  ⚠️ ALERT: High temperature detected! Triggering cooling logic...")
        
        # Wait 2 seconds before sampling again
        time.sleep(2)

if __name__ == "__main__":
    try:
        simulate_environment()
    except KeyboardInterrupt:
        print("\nSimulation stopped safely.")