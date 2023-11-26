# Only for DEV purposes.

# To add more color icons
# 1. add color in COLORS
# 2. add the rgb for that color in RGB.

from PIL import Image
import os


COLORS = ["red", "blue", "green", "yellow", "orange", "gray", "brown"]
RGB = [
    (255, 0, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 150, 50),
    (130, 130, 130),
    (100, 50, 0),
]
FILES = ["home", "pos", "spos", "rtl_pos", "waypoint"]


def prepare_icon(file, req_rgb, save_name):
    """
    Prepares map icons for each vehicle

    Parameters
    ----------
    file : .png file
        One of the input icon files.
    req_rgb : tuple
        (r, g, b) of the required color for icon.
    save_name : .png file
        Name to save the file.

    Returns
    -------
    None.

    """

    img = Image.open(file)
    pixel_map = img.load()
    width, height = img.size

    # pix = []
    for i in range(width):
        for j in range(height):
            r, g, b, p = img.getpixel((i, j))
            # pix.append((r,g,b, p))

            if p != 0:
                pixel_map[i, j] = req_rgb
            elif not r == g == b:
                pixel_map[i, j] = req_rgb
            else:
                pass
    img.save(save_name)
    # img.show()
    # return pix


# Example to test a new icon.
# all_pix = prepare_icon("circle2.png", (0, 240, 0), "dummy_one.png")

if __name__ == "__main__":
    sep_path = os.getcwd().split("/gust/")
    path = "{}/gust/src/main/resources/base/map_widget/".format(sep_path[0])

    for color, rgb in zip(COLORS, RGB):
        for file in FILES:
            # location of the files from FILES
            filename = "{}{}.png".format(path, file)
            # location of where to save the colored files
            savename = "{}colored_icons/{}_{}.png".format(path, color, file)
            prepare_icon(filename, rgb, savename)
