import cv2
import numpy as np
import rawpy

from movie import make_video


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
        adjusted_image = adjust_exposure(image, exposure_factor)

        # Define tone curve points for each channel (example)
        # flat: [(0, 0), (64, 80), (128, 128), (192, 200), (255, 255)]
        curve_points_red = red
        curve_points_green = green
        curve_points_blue = blue

        # Adjust the tone curves of the image
        adjusted_image = adjust_tone_curve(
            adjusted_image, curve_points_red, curve_points_green, curve_points_blue
        )
        cv2.imwrite(f"{dir}/{i+1}.png", adjusted_image)


if __name__ == "__main__":
    vid_name = "8"

    TEST = True
    curve_adjustments = {
        "red": [(30, 0), (130, 255), (200, 0)],
        "green": [(0, 0), (89, 255), (255, 0)],
        "blue": [(80, 0), (100, 255), (150, 0)],
    }
    if TEST:
        frames = 24
        dir = "test"
    else:
        frames = 24 * 8  # 8 seconds of video
        dir = "output"

    if TEST:
        adjust_images(**curve_adjustments, frames=frames, dir=dir)
        make_video(vid_name, "test", 24)
    else:
        adjust_images(**curve_adjustments, frames=frames, dir=dir)
        make_video(vid_name, "output", 24)
