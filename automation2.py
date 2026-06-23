import cv2
import numpy as np

def start_live_inspection():
    # Initialize webcam (0 is usually the default built-in camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video feed.")
        return

    print("Live Inspection Started. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Make a copy for rendering the output overlays
        output_frame = frame.copy()

        # 1. Pre-processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive or simple thresholding depending on room lighting
        # Adjust '100' up or down based on your room's brightness
        _, thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)

        # 2. Contour Detection
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        system_pass = True

        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Ignore tiny noise fragments
            if area < 500:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            # 3. Live Pass/Fail Logic Rules
            # Adjust these pixel area thresholds based on the object you hold up to the camera!
            if area > 50000:  
                # Too large might mean multiple objects or a blockage
                label = "Anomaly"
                color = (0, 0, 255)
                system_pass = False
            elif 10000 <= area <= 45000:
                label = "Passed Part"
                color = (0, 255, 0)
            else:
                label = "Defective/Damaged"
                color = (0, 0, 255)
                system_pass = False

            # Draw real-time overlays
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(output_frame, f"{label} ({int(area)})", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display Live Status Banner
        status_text = "CONVEYOR STATUS: OK" if system_pass else "CONVEYOR STATUS: DEFECT DETECTED"
        status_color = (0, 255, 0) if system_pass else (0, 0, 255)
        cv2.putText(output_frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        # Show live windows
        cv2.imshow("Live Feed", output_frame)
        cv2.imshow("Live Binary Mask", thresholded)

        # Break loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_live_inspection()