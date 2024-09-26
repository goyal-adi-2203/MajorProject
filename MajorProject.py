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
import matplotlib.pyplot as plt

resize_factor = 0.1

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
    edged = cv2.Canny(blurred, 30, 100)

    plt.subplot(121), plt.imshow(image, cmap="gray")
    plt.title("Original Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edged, cmap="gray")
    plt.title("Edge Image"), plt.xticks([]), plt.yticks([])



    # dilation and erosion
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=2)
    erosion = cv2.erode(dilated, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # min_cotour_area = 500
    # filtered_contours = [x for x in contours if cv2.contourArea(x) > min_cotour_area]

    filtered_contours = contours

    # If contours are found, get the largest one (assuming the object of interest is the largest)
    if filtered_contours:
        largest_contour = max(filtered_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Draw bounding box and points on the image (for visualization purposes)
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw circles at corners of the bounding box
        cv2.circle(image_resized, (x, y), 5, (0, 0, 255), -1)  # Top-left corner
        cv2.circle(image_resized, (x + w, y), 5, (0, 0, 255), -1)  # Top-right corner
        cv2.circle(image_resized, (x, y + h), 5, (255, 0, 0), -1)  # Bottom-left corner
        cv2.circle(image_resized, (x + w, y + h), 5, (255, 0, 0), -1)  # Bottom-right corner

        # Draw lines to indicate height and width
        cv2.line(image_resized, (x, y), (x, y + h), (255, 255, 0), 2)  # Vertical line (Height)
        cv2.line(image_resized, (x, y), (x + w, y), (255, 255, 0), 2)  # Horizontal line (Width)

        # Show the image with bounding box, points, and lines
        cv2.imshow("Bounding Box with Points", image_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Return the coordinates for width and height
        return (x, y), (x + w, y + h), w, h
    else:
        return None, None, 0, 0

def calculate_object_size(w, h, image_height, focal_length, distance, sensor_length_mm):
    # Object width and height in pixels
    Object_height_on_sensor_mms = (sensor_length_mm * h) / image_height
    Object_width_on_sensor_mms = (sensor_length_mm * w) / image_height

    # Convert object size to meters
    Object_height_meters = (distance * Object_height_on_sensor_mms) / focal_length
    Object_width_meters = (distance * Object_width_on_sensor_mms) / focal_length

    return Object_height_meters, Object_width_meters

# Path to your image
image_path = "pic 45-3.JPG"

# Automatically get the bounding box points and dimensions
p1, p2, width_pixels, height_pixels = get_bounding_box(image_path)

if p1 is not None and p2 is not None:
    print("Bounding box points (Top-left, Bottom-right):", p1, p2)
    print("Width (pixels):", width_pixels)
    print("Height (pixels):", height_pixels)

    focal_length = 4.7  # mm
    distance = 0.45  # meters
    sensor_length_mm = 6.26  # mm
    image_height = 4624  # in pixels

    # Calculate object width and height in meters
    object_height_meters, object_width_meters = calculate_object_size(width_pixels, height_pixels, image_height, focal_length, distance, sensor_length_mm)

    print(f"Object height: {object_height_meters:.6f} meters")
    print(f"Object width: {object_width_meters:.6f} meters")
else:
    print("No object detected.")
