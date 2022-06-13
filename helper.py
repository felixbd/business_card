# #!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""=====================================================================================================================

BUSINESS CARD CREATOR
This project contains a simple graphical user interface that
you can use to create a digital business card for Apple Wallet.
Copyright (C) 2021  Felix Drees

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

====================================================================================================================="""

import os
from typing import Union, Any
import tkinter as tk

from PIL import Image as pil_img


class ResizeImageForApplePass:
    """
    background.png  180 x 220 points
    footer.png      286 x 15 points
    icon.png        29 x 29 points
    logo.png        160 x 50 points
    strip.png       ... to complicated ^^
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
        original_img = pil_img.open(self._img_file_name)
        # resize imgs
        small_resized_img = original_img.resize(self._IMAGE_SIZE[self._img_type][0])
        big_resized_img = original_img.resize(self._IMAGE_SIZE[self._img_type][1])
        # save imgs
        small_resized_img.save(os.path.join("BusinessCard.pass", f"{self._img_type}.png"))
        big_resized_img.save(os.path.join("BusinessCard.pass", f"{self._img_type}@2x.png"))

        return os.path.join("BusinessCard.pass", f"{self._img_type}.png"), \
               os.path.join("BusinessCard.pass", f"{self._img_type}@2x.png")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type == FileExistsError:
            return True
        if exc_type == FileNotFoundError:
            return False


def me_card_formatter(first_middle_name: str, last_name: str, email: str, tel: str, b_day: Union[int, str]) -> str:
    """
    MeCard (QR code) - for a quick and easy sharing of a contact

    MeCard is a data file similar to vCard but used by NTT DoCoMo in Japan in QR code format for use with Cellular Phones.
    It is largely compatible with most QR-readers for smartphones. It is an easy way to share a contact with the most used fields.
    Usually, devices can recognize it and treat it like a contact ready to import.
    The QR Code image in the README.md is an example.

    Args:
        first_middle_name: the first and middle names of the contact
        last_name: the last name of the contact
        email: the email of the contact
        tel: the tel of the contact
        b_day: the date of birth of the contact

    Returns:    the MeCard values in teh MeCard format
    Note:       the email tel and b-day are not checked for valid formatting
    Example:    MECARD:N:Doe,John;EMAIL:john.doe@example.com;TEL:13035551212;BDAY:19700310;;
    """
    rv_string = f"MECARD:N:{last_name},{first_middle_name};"

    # Empty strings are considered false in a Boolean context
    if email: rv_string += f"EMAIL:{email};"
    if tel: rv_string += f"TEL:{tel};"
    if b_day: rv_string += f"BDAY:{b_day};"

    return rv_string + ';'


def place_label_and_entry_fields(frame_name: tk.Frame, bg_color: str, keys_and_default_text: dict, distance: Union[int, float], height: Union[int, float]) -> dict[Any, Union[str, tk.Entry]]:
    """ TODO ... """
    label_names = dict([(key, f"{key.replace(' ', '_')}_label") for key in keys_and_default_text])
    entry_names = dict([(key, f"{key.replace(' ', '_')}_entry") for key in keys_and_default_text])

    rel_y_loop = distance
    for label, default_text in keys_and_default_text.items():
        # LABELS
        label_names[label] = tk.Label(frame_name, text=f"{label}: ", bg=bg_color)
        label_names[label].place(relx=0.05, rely=rel_y_loop, relheight=height, relwidth=0.35)
        # ENTRYS
        entry_names[label] = tk.Entry(frame_name, bg=bg_color)
        entry_names[label].insert(tk.END, f'{default_text}')
        entry_names[label].place(relx=0.45, rely=rel_y_loop, relheight=height, relwidth=0.45)

        rel_y_loop += distance
    return entry_names
