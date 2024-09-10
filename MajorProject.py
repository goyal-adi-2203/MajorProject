# import cv2

# # Global variables to store selected point coordinates
# selected_point = None
# resize_factor = 0.25

# def select_point(event, x, y, flags, param):
#     global selected_point

#     # If left mouse button is clicked, store the coordinates
#     if event == cv2.EVENT_LBUTTONDOWN:
#         selected_point = (x, y)

# def get_point_coordinates(image_path):
#     global selected_point

#     # Read the image
#     image = cv2.imread(image_path)
#     og_size = image.shape[:2]
#     clone = image.copy()

#     # Create a window and bind the mouse callback function
#     cv2.namedWindow("Select Point")
#     image = cv2.resize(image, dsize=(int(og_size[1] * resize_factor), int(og_size[0] * resize_factor)))
#     cv2.setMouseCallback("Select Point", select_point)

#     while True:
#         # Display the image and wait for a key press
#         cv2.imshow("Select Point", image)
#         key = cv2.waitKey(1) & 0xFF

#         # If 'r' is pressed, reset the selected point
#         if key == ord("r"):
#             selected_point = None
#             image = clone.copy()

#         # If 's' is pressed or a point is selected, break from the loop
#         if key == ord("s") or selected_point is not None:
#             break

#     # Close all OpenCV windows
#     cv2.destroyAllWindows()

#     if selected_point is not None:
#         scaled_point = (int(selected_point[0] / resize_factor), int(selected_point[1]/resize_factor))
#         return scaled_point
#     else:
#         return None

# # Path to your image
# image_path = "Screenshot (2).png"

# # Get the coordinates of the selected point
# p1 = get_point_coordinates(image_path)
# selected_point = None
# p2 = get_point_coordinates(image_path)


# # Display the coordinates
# if p1 is not None:
#     print("Selected point coordinates:", p1)
# else:
#     print("No point selected.")

# # Display the coordinates
# if p2 is not None:
#     print("Selected point coordinates 2:", p2)
# else:
#     print("No point selected.")


# focal_length = 4.7 # mm
# eq_focal_length = 26 # mm

# # ppi = 72 and pixel pitch or dot pitch = 1 / ppi
# pixel_pitch = 1/72

# image_width = 2080
# image_height = 4624

# distance = 0.38 # m

# sensor_length_mm = 6.26 # mm
# sensor_length_pixels = image_height

# # print(sensor_length_mm)
# # print(sensor_length_pixels)

# Object_length_pixels = abs(p1[1] - p2[1])
# Object_length_on_sensor_mms = ( sensor_length_mm * Object_length_pixels ) / sensor_length_pixels
# Object_length_meters = ( ( distance * Object_length_on_sensor_mms ) / focal_length )

# print(Object_length_meters,"Meters")
# print(Object_length_on_sensor_mms)

# sensor_height = 6.26 # mm
# sensor_width = 4.26 # mm

# ans = (Object_length_pixels * distance * sensor_height) / (image_height * focal_length)
# print("ans : ", ans)


# # 4.69×6.26 mm

import cv2
import numpy as np

resize_factor = 0.25

def get_bounding_box(image_path):
    # Read the image
    image = cv2.imread(image_path)
    og_size = image.shape[:2]
    image_resized = cv2.resize(image, dsize=(int(og_size[1] * resize_factor), int(og_size[0] * resize_factor)))

    # Convert to grayscale
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform Canny edge detection
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found, get the largest one (assuming the object of interest is the largest)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Draw bounding box and points on the image (for visualization purposes)
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw circles at top-left (p1) and bottom-right (p2) of the bounding box
        cv2.circle(image_resized, (x, y), 5, (0, 0, 255), -1)  # Top-left corner
        cv2.circle(image_resized, (x + w, y + h), 5, (255, 0, 0), -1)  # Bottom-right corner

        # Draw a line between the two points to visualize the distance
        cv2.line(image_resized, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # Show the image with bounding box, points, and distance line
        cv2.imshow("Bounding Box with Points", image_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Return the coordinates of the top-left and bottom-right corners of the bounding box
        return (x, y), (x + w, y + h)
    else:
        return None, None

def calculate_object_size(p1, p2, image_height, focal_length, distance, sensor_length_mm):
    Object_length_pixels = abs(p1[1] - p2[1])
    Object_length_on_sensor_mms = (sensor_length_mm * Object_length_pixels) / image_height
    Object_length_meters = (distance * Object_length_on_sensor_mms) / focal_length
    return Object_length_meters, Object_length_on_sensor_mms

# Path to your image
image_path = "Screenshot (2).png"

# Automatically get the bounding box points
p1, p2 = get_bounding_box(image_path)

if p1 is not None and p2 is not None:
    print("Bounding box points:", p1, p2)

    focal_length = 4.7  # mm
    distance = 0.38  # meters
    sensor_length_mm = 6.26  # mm
    image_height = 4624  # in pixels

    # Calculate object size
    object_size_meters, object_size_on_sensor_mm = calculate_object_size(p1, p2, image_height, focal_length, distance, sensor_length_mm)

    print(f"Object size: {object_size_meters:.6f} meters")
    print(f"Object size on sensor: {object_size_on_sensor_mm:.6f} mm")
else:
    print("No object detected.")
