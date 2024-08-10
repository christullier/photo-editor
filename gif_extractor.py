import os

from PIL import Image


def extract_frames_from_gif(gif_path, output_folder):
    # Open the GIF file
    gif = Image.open(gif_path)

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each frame of the GIF
    for frame_number in range(gif.n_frames):
        # Set the current frame
        gif.seek(frame_number)

        # Save the current frame as an image
        frame_path = os.path.join(output_folder, f"frame_{frame_number:03d}.png")
        gif.save(frame_path, "PNG")
        print(f"Saved frame {frame_number} to {frame_path}")


# Usage example
gif_file_path = "sample-julia.gif"
output_directory = "gif_output"
extract_frames_from_gif(gif_file_path, output_directory)
