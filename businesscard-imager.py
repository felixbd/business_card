# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################################################################
#   GNU AGPLv3 | Copyright (C) 2021  Felix Drees | BUSINESS CARD CREATOR                                               #
########################################################################################################################

import os
import argparse
from typing import Union, Any

from PIL import Image


class ResizeImageForApplePass:
    """
    background.png  180 x 220 points
    footer.png      286 x 15 points
    icon.png        29 x 29 points
    logo.png        160 x 50 points
    strip.png       TODO ... to complicated ^^
    thumbnail.png   90 x 90 points. aspect ratio should be in range 2:3 to 3:2, otherwise the image is cropped

    Note:
    non-Retina display -> 1 point ==  1 pixel
    Retina display -> 2 or 3 pixels per point
    To support all screen sizes and resolutions, provide the original, @2x, and @3x versions of your art.
    """

    _IMAGE_TYPES = ["logo", "thumbnail"]
    _IMAGE_SIZE = {"logo": [(66, 54), (69, 58)], "thumbnail": [(45, 45), (388, 429)]}

    def __init__(self, img_file_name: str, img_type: str) -> None:
        if not isinstance(img_file_name and img_type, str) or img_type not in self._IMAGE_TYPES:
            raise TypeError("UNABLE TO RESIZE IMG, invalid img file name or img type")

        self._img_file_name = img_file_name
        self._img_type = img_type

    def __enter__(self) -> tuple:
        original_img = Image.open(self._img_file_name)
        # resize images
        small_resized_img = original_img.resize(self._IMAGE_SIZE[self._img_type][0])
        big_resized_img = original_img.resize(self._IMAGE_SIZE[self._img_type][1])
        # save images
        small_resized_img.save(os.path.join("BusinessCard.pass", f"{self._img_type}.png"))
        big_resized_img.save(os.path.join("BusinessCard.pass", f"{self._img_type}@2x.png"))

        return os.path.join("BusinessCard.pass", f"{self._img_type}.png"), \
               os.path.join("BusinessCard.pass", f"{self._img_type}@2x.png")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type == FileExistsError:
            return True
        if exc_type == FileNotFoundError:
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description='REFORMATTING IMAGES FOR BUSINESS CARD')

    parser.add_argument('-t', '--thumbnail', help='paste path to thumbnail image file', default=None)
    parser.add_argument('-l', '--logo', help='paste path to logo image file', default=None)

    args = parser.parse_args()

    try:
        with ResizeImageForApplePass(args.thumbnail, 'thumbnail') as saved_thumbnail_img_file_names:
            pass

        with ResizeImageForApplePass(args.logo, 'logo') as saved_logo_img_file_names:
            pass
    except Exception as error:
        raise SystemError(error)


if __name__ == '__main__':
    main()

