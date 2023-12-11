import cv2

camera_index = '/dev/video2'

def export_camera_frame(_output_filename):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return

    # Read a single frame from the camera
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame from the camera")
        cap.release()
        return

    # Save the frame as a JPG image
    cv2.imwrite(_output_filename, frame)

    # Release the camera
    cap.release()

    print(f"Frame exported as {output_filename}")

output_filename = "output_image.jpg"  # Change this to the desired output filename
export_camera_frame(output_filename)
