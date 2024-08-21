import cv2
import numpy as np
import rawpy

from masking import apply_mask


def get_lut(full_range, curve_points):
    lut = np.interp(
        full_range,
        [p[0] for p in curve_points],
        [p[1] for p in curve_points],
    ).astype("uint8")
    return lut


def normalize_mask(mask):
    # Normalize the mask to range from 0 to 1
    mask_min = np.min(mask)
    mask_max = np.max(mask)
    normalized_mask = (mask - mask_min) / (mask_max - mask_min)
    return normalized_mask


def adjust_tone_curve(
    image, curve_points_red, curve_points_green, curve_points_blue, mask=None
):
    # Create lookup tables for each color channel
    full_range = np.arange(256)
    lut_red = get_lut(full_range, curve_points_red)
    lut_green = get_lut(full_range, curve_points_green)
    lut_blue = get_lut(full_range, curve_points_blue)

    # Split the image into its color channels
    b, g, r = cv2.split(image)

    # Apply the lookup table to each channel
    r_adjusted = cv2.LUT(r, lut_red)
    g_adjusted = cv2.LUT(g, lut_green)
    b_adjusted = cv2.LUT(b, lut_blue)

    if mask is not None:
        # Resize mask to match the image dimensions
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

        # Ensure the mask is in float format and normalized
        mask_resized = normalize_mask(mask_resized)

        # Expand the mask to three channels
        mask_resized = cv2.merge([mask_resized] * 3)

        # Blend the original and adjusted channels using the mask
        r_adjusted = (1 - mask_resized[:, :, 0]) * r + mask_resized[
            :, :, 0
        ] * r_adjusted
        g_adjusted = (1 - mask_resized[:, :, 1]) * g + mask_resized[
            :, :, 1
        ] * g_adjusted
        b_adjusted = (1 - mask_resized[:, :, 2]) * b + mask_resized[
            :, :, 2
        ] * b_adjusted

        # Convert back to uint8
        r_adjusted = r_adjusted.astype(np.uint8)
        g_adjusted = g_adjusted.astype(np.uint8)
        b_adjusted = b_adjusted.astype(np.uint8)

    # Merge the channels back into an image
    adjusted_image = cv2.merge((b_adjusted, g_adjusted, r_adjusted))

    return adjusted_image


def adjust_exposure(image, exposure_factor):
    return np.clip(image * exposure_factor, 0, 255).astype("uint8")


def get_mask(name: str, folder="."):
    image = cv2.imread(f"{folder}/{name}")
    return image


def adjust_images(
    red: list[tuple[int, int]],
    green: list[tuple[int, int]],
    blue: list[tuple[int, int]],
    frames: int,
    dir: str,
):
    raw = rawpy.imread("tree.NEF")
    image = raw.postprocess()

    final_exposure_adjustment = 4
    for i in range(frames):
        # Slightly increase the exposure
        exposure_factor = round(final_exposure_adjustment * (i / frames), 4)

        # exposure **must** be adjusted first
        # adjusted_image = adjust_exposure(image, exposure_factor)
        adjusted_image = image

        # flat tone curve: [(0, 0), (64, 80), (128, 128), (192, 200), (255, 255)]
        curve_points_red = red
        curve_points_green = green
        curve_points_blue = blue

        mask = get_mask(f"frame_{i:03d}.png", "julia_cropped_split_1")
        # Adjust the tone curves of the image
        adjusted_image = adjust_tone_curve(
            adjusted_image,
            curve_points_red,
            curve_points_green,
            curve_points_blue,
            mask,
        )
        cv2.imwrite(f"{dir}/{i+1}.png", adjusted_image)
