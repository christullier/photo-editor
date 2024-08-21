import os

from movie import make_video
from tonecurve import adjust_images


def get_new_vid_name(base_name, directory="."):
    # Get the file extension
    base, extension = os.path.splitext(base_name)

    # Initialize a counter
    counter = 1

    # Construct the initial file path
    new_name = f"{base}{extension}"
    file_path = os.path.join(directory, new_name)

    # Check if the file exists and iterate the name if it does
    while os.path.exists(file_path):
        # Increment the counter and create a new name
        new_name = f"{base}_{counter}{extension}"
        file_path = os.path.join(directory, new_name)
        counter += 1

    return new_name


if __name__ == "__main__":

    TEST = False
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
        frames = 100
        dir = "output"

    vid_name = "fractal"
    vid_name = get_new_vid_name(f"{vid_name}.mp4", "vids")

    if TEST:
        adjust_images(**curve_adjustments, frames=frames, dir=dir)
        make_video(vid_name, "test", 24)
    else:
        adjust_images(**curve_adjustments, frames=frames, dir=dir)
        make_video(vid_name, "output", 24)
