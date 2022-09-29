#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:56:39 2022

@author: lagerprocessor
"""

from PIL import Image


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

    pix = []
    for i in range(width):
        for j in range(height):
            r, g, b, p = img.getpixel((i, j))
            pix.append((r,g,b, p))

            if p != 0:
                pixel_map[i, j] = req_rgb
            elif not r == g == b:
                pixel_map[i, j] = req_rgb
            else:
                pass
    # img.save(save_name)
    img.show()
    return pix

# Example to test a new icon.
all_pix = prepare_icon("circle2.png", (0, 240, 0), "dummy_one.png")
