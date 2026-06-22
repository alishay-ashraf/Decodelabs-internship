import time
import random  # Simulating hardware input for demonstration

# ==========================================
# 1. FIELD CALIBRATION ANCHORS
# ==========================================
# Calibrated raw ADC values based on your environment [cite: 95, 96]
ADC_DRY = 3200  # Raw value in dry air/sand [cite: 93, 97]
ADC_WET = 1200  # Raw value fully submerged [cite: 94, 97]

# ==========================================
# 2. CONTROL LOOP HYSTERESIS CONFIGURATION
# ==========================================
# Dual-thresholds prevent catastrophic relay chattering [cite: 23, 124]
PUMP_ON_THRESHOLD = 30   # Turn pump ON when moisture drops below 30%
PUMP_OFF_THRESHOLD = 60  # Keep pumping until moisture reaches a safe 60%

# ==========================================
# 3. EMA FILTER CONFIGURATION
# ==========================================
ALPHA = 0.2  # Smoothing factor capturing slow environmental changes [cite: 91]
ema_signal = None  # Holds the running filtered state [cite: 90]

# Track current state of the physical actuator relay
pump_is_on = False


def read_raw_adc_hardware():
    """
    Simulates reading from a 12-bit ADC (0 to 4095)[cite: 75, 76].
    In real hardware, replace this with your driver library, e.g.:
    adc.read_uv() or analog_in.value
    """
    # Simulating a dry environment with high-frequency Wi-Fi/CPU noise [cite: 67, 86]
    base_dry_reading = 3100
    noise = random.randint(-150, 150)
    return base_dry_reading + noise


def map_and_constrain(raw_val, from_low, from_high, to_low, to_high):
    """
    Normalizes raw readings into safe, discrete percentages[cite: 92, 107].
    """
    # Linear mapping formula equivalent to Arduino's map() [cite: 107]
    numerator = (raw_val - from_low) * (to_high - to_low)
    denominator = from_high - from_low
    mapped_val = to_low + (numerator / denominator)
    
    # CRITICAL: Constrain to prevent downstream math logic failures [cite: 108, 109]
    constrained_val = max(to_low, min(to_high, mapped_val))
    return constrained_val


# ==========================================
# MAIN CLOSED-LOOP CONTROL EXECUTION [cite: 8, 19]
# ==========================================
print("Initializing Autonomous Irrigation Controller...\n")

try:
    while True:
        # Step A: Get raw noisy analog hardware telemetry [cite: 21, 87]
        raw_adc = read_raw_adc_hardware()
        
        # Step B: Apply Exponential Moving Average (EMA) [cite: 89, 90]
        if ema_signal is None:
            ema_signal = raw_adc  # Initialize filter with first value
        else:
            ema_signal = (ALPHA * raw_adc) + ((1 - ALPHA) * ema_signal)
            
        # Step C: Normalize and safely constrain the telemetry data [cite: 92, 108]
        # Note: ADC_DRY maps to 0% moisture, ADC_WET maps to 100% moisture [cite: 67, 97, 107]
        moisture_percentage = map_and_constrain(ema_signal, ADC_DRY, ADC_WET, 0, 100)        
        # Step D: Process Closed-Loop Hysteresis Logic Gate [cite: 8, 23]
        if not pump_is_on and moisture_percentage < PUMP_ON_THRESHOLD:
            pump_is_on = True
            print(f"[ACTUATOR] ON -> Soil is too dry ({moisture_percentage:.1f}%). Triggering 5V Relay[cite: 23, 24].")
        elif pump_is_on and moisture_percentage > PUMP_OFF_THRESHOLD:
            pump_is_on = False
            print(f"[ACTUATOR] OFF -> Target moisture hit ({moisture_percentage:.1f}%). Shutting down Relay[cite: 24].")
            
        # Logging standard telemetry stream
        print(f"Raw ADC: {raw_adc} | EMA Filtered ADC: {ema_signal:.1f} | Clean Moisture: {moisture_percentage:.1f}% | Pump Active: {pump_is_on}")
        
        time.sleep(1.0)  # Continuous execution loop sampling period

except KeyboardInterrupt:
    print("\nController safely shut down.")