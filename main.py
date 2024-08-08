from movie import make_video
from tonecurve import adjust_images

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
