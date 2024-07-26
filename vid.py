import cv2
import numpy as np


def adjust_tone_curve(image, curve_points_red, curve_points_green, curve_points_blue):
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


def adjust_exposure(image, exposure_factor):
    return np.clip(image * exposure_factor, 0, 255).astype("uint8")


# Load an image
image = cv2.imread("tree.NEF", cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

# Define tone curve points for each channel (example)
curve_points_red = [(0, 0), (64, 70), (128, 128), (192, 180), (255, 255)]
curve_points_green = [(0, 0), (64, 80), (128, 128), (192, 200), (255, 255)]
curve_points_blue = [(0, 0), (64, 90), (128, 128), (192, 210), (255, 255)]

# Adjust the tone curves of the image
adjusted_image = adjust_tone_curve(
    image, curve_points_red, curve_points_green, curve_points_blue
)

# Adjust the exposure of the image
exposure_factor = 1.2  # Slightly increase the exposure
adjusted_image = adjust_exposure(adjusted_image, exposure_factor)

# Define video properties
height, width, _ = image.shape
video_path = "adjusted_video.avi"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 1  # 1 frame per second for simplicity
video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

# Create video frames
for i in range(30):
    video_writer.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    video_writer.write(cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2BGR))

video_writer.release()
