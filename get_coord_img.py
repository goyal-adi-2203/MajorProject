import cv2

# Global variables to store selected point coordinates
selected_point = None
resize_factor = 0.25

def select_point(event, x, y, flags, param):
    global selected_point

    # If left mouse button is clicked, store the coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)

def get_point_coordinates(image_path):
    global selected_point

    # Read the image
    image = cv2.imread(image_path)
    og_size = image.shape[:2]
    clone = image.copy()

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select Point")
    image = cv2.resize(image, dsize=(int(og_size[1] * resize_factor), int(og_size[0] * resize_factor)))
    cv2.setMouseCallback("Select Point", select_point)

    while True:
        # Display the image and wait for a key press
        cv2.imshow("Select Point", image)
        key = cv2.waitKey(1) & 0xFF

        # If 'r' is pressed, reset the selected point
        if key == ord("r"):
            selected_point = None
            image = clone.copy()

        # If 's' is pressed or a point is selected, break from the loop
        if key == ord("s") or selected_point is not None:
            break

    # Close all OpenCV windows
    cv2.destroyAllWindows()

    if selected_point is not None:
        scaled_point = (int(selected_point[0] / resize_factor), int(selected_point[1]/resize_factor))
        return scaled_point
    else:
        return None

# Path to your image
image_path = "C:/Users/91826/Downloads/pic 2.jpg"

# Get the coordinates of the selected point
p1 = get_point_coordinates(image_path)
selected_point = None
p2 = get_point_coordinates(image_path)


# Display the coordinates
if p1 is not None:
    print("Selected point coordinates:", p1)
else:
    print("No point selected.")

# Display the coordinates
if p2 is not None:
    print("Selected point coordinates 2:", p2)
else:
    print("No point selected.")


focal_length = 4.7 # mm
eq_focal_length = 26 # mm

# ppi = 72 and pixel pitch or dot pitch = 1 / ppi
pixel_pitch = 1/72

image_width = 2080
image_height = 4624

distance = 0.38 # m

sensor_length_mm = 6.26 # mm
sensor_length_pixels = image_height

# print(sensor_length_mm)
# print(sensor_length_pixels)

Object_length_pixels = abs(p1[1] - p2[1])
Object_length_on_sensor_mms = ( sensor_length_mm * Object_length_pixels ) / sensor_length_pixels
Object_length_meters = ( ( distance * Object_length_on_sensor_mms ) / focal_length )

print(Object_length_meters,"Meters")
print(Object_length_on_sensor_mms)

sensor_height = 6.26 # mm
sensor_width = 4.26 # mm

ans = (Object_length_pixels * distance * sensor_height) / (image_height * focal_length)
print("ans : ", ans)


# 4.69×6.26 mm