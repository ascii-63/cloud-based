import cv2
import numpy as np
import time

# Open the capture device (replace '/dev/media0' with your specific device)
capture = cv2.VideoCapture(2, cv2.CAP_V4L2)

if not capture.isOpened():
    print("Error: Could not open capture device.")
    exit()

while True:
    ret, frame = capture.read()

    if not ret:
        print("Error: Failed to read frame from the capture device.")
        break

    # Extract frame metadata (if available)
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = capture.get(cv2.CAP_PROP_FPS)

    # Get the current timestamp with milliseconds
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime()/1000)
    timestamp = timestamp[:-3]  # Remove the last 3 digits to get milliseconds

    # Print frame metadata including the timestamp with milliseconds
    print(f"Timestamp: {timestamp}, Frame Width: {frame_width}, Frame Height: {frame_height}, Frame FPS: {frame_fps}")

    # Save the frame to a PNG file with the timestamp
    filename = f"captured_frame_{timestamp}.png"
    cv2.imwrite(filename, frame)

    # Display the frame (optional)
    cv2.imshow("Captured Frame", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture device and close the OpenCV window (if opened)
capture.release()
cv2.destroyAllWindows()
