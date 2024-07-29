import cv2
import numpy as np
import rawpy


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
    """
    Adjust the exposure of an image.

    Parameters:
        image (numpy.ndarray): Input image.
        exposure_factor (float): Factor by which to adjust the exposure.
                                 Values > 1 will increase exposure, values < 1 will decrease exposure.

    Returns:
        numpy.ndarray: Image with adjusted exposure.
    """
    return np.clip(image * exposure_factor, 0, 255).astype("uint8")


# Load an image
# image = cv2.imread("tree.jpg", cv2.IMREAD_COLOR)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
raw = rawpy.imread("tree.NEF")
image = raw.postprocess()

TEST = False

final_adjustment = 4
if TEST:
    frames = 10
    dir = "test"
else:
    frames = 120 * 2
    dir = "output"
for i in range(frames):
    # Slightly increase the exposure
    exposure_factor = round(final_adjustment * (i / frames), 4)

    # exposure **must** be adjusted first
    adjusted_image = adjust_exposure(image, exposure_factor)

    # Define tone curve points for each channel (example)
    # base: [(0, 0), (64, 80), (128, 128), (192, 200), (255, 255)]
    # Adjust the tone curves of the image
    curve_points_red = [(30, 0), (130 + i, 255), (200, 0)]
    curve_points_green = [(0, 0), (89 + i, 255), (255, 0)]
    curve_points_blue = [(80, 0), (100 + i, 255), (255, 0)]

    adjusted_image = adjust_tone_curve(
        adjusted_image, curve_points_red, curve_points_green, curve_points_blue
    )
    cv2.imwrite(f"{dir}/{i+1}.png", adjusted_image)
