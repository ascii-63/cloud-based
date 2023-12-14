import cv2
import sys


# RTSP stream URL
rtsp_url = sys.argv[1]

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("Error: Couldn't open the RTSP stream.")
    exit()

# Set the window name and create a window
window_name = rtsp_url
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while True:
    # Read a frame from the RTSP stream
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame from the RTSP stream.")
        break

    # Display the frame
    cv2.imshow(window_name, frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
