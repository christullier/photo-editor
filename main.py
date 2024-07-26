import cv2
import matplotlib.pyplot as plt
import numpy as np


def adjust_tone_curve(image, curve_points_red, curve_points_green, curve_points_blue):
    """
    Adjust the tone curve of an image based on given curve points for each channel.

    Parameters:
        image (numpy.ndarray): Input image.
        curve_points_red (list of tuple): List of points defining the tone curve for the red channel.
        curve_points_green (list of tuple): List of points defining the tone curve for the green channel.
        curve_points_blue (list of tuple): List of points defining the tone curve for the blue channel.

    Returns:
        numpy.ndarray: Image with adjusted tone curves.
    """
    # Create lookup tables for each color channel
    full_range = np.arange(256)
    lut_red = np.interp(
        full_range, [p[0] for p in curve_points_red], [p[1] for p in curve_points_red]
    ).astype("uint8")
    lut_green = np.interp(
        full_range,
        [p[0] for p in curve_points_green],
        [p[1] for p in curve_points_green],
    ).astype("uint8")
    lut_blue = np.interp(
        full_range, [p[0] for p in curve_points_blue], [p[1] for p in curve_points_blue]
    ).astype("uint8")

    # Split the image into its color channels
    b, g, r = cv2.split(image)

    # Apply the lookup table to each channel
    r_adjusted = cv2.LUT(r, lut_red)
    g_adjusted = cv2.LUT(g, lut_green)
    b_adjusted = cv2.LUT(b, lut_blue)

    # Merge the channels back into an image
    adjusted_image = cv2.merge((b_adjusted, g_adjusted, r_adjusted))

    return adjusted_image


# Load an image
image = cv2.imread("tree.jpg", cv2.IMREAD_COLOR)
cv2.imwrite("pre.png", image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
cv2.imwrite("post.png", image)
# Define tone curve points for each channel (example)
curve_points_red = [(10, 255), (64, 70), (128, 128), (192, 180), (255, 255)]
curve_points_green = [(20, 255), (64, 80), (128, 128), (192, 200), (255, 255)]
curve_points_blue = [(37, 0), (64, 90), (128, 128), (192, 210), (255, 255)]

# Adjust the tone curves of the image
adjusted_image = adjust_tone_curve(
    image, curve_points_red, curve_points_green, curve_points_blue
)

cv2.imwrite("out.png", adjusted_image)

# Display the original and adjusted images
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Adjusted Image")
plt.imshow(adjusted_image)
plt.axis("off")

plt.show()
