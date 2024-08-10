import os
import re

import cv2


def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.
    "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split("([0-9]+)", s)]


def sort_nicely(l):
    """Sort the given list in the way that humans expect."""
    l.sort(key=alphanum_key)


def images_to_video(image_folder, output_video, frame_rate):
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith(".png") or img.endswith(".jpg")
    ]
    # images.sort()  # Ensure the images are sorted in the correct order
    sort_nicely(images)

    # Read the first image to get the dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4 files
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
        print(f"wrote: {image}")

    video.release()
    print(f"Video saved as {output_video}")


def make_video(video_file_name: str, image_folder: str, frame_rate: int):

    video_file_name = "vids/" + video_file_name

    images_to_video(image_folder, video_file_name, frame_rate)
    os.system("say completo")


if __name__ == "__main__":
    make_video()
