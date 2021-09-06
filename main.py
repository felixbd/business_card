#!/usr/bin/env python3.9
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
import json

import helper

import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor

__version__: str = "1.1.0"

TK_HEIGHT: float = 800
TK_WIDTH: float = 1200

icon_img_file_name: str = ''
thumbnail_img_file_name: str = ''
foreground_color: str = ''
background_color: str = ''


def select_icon_img() -> None:
    global icon_img_file_name
    icon_img_file_name = askopenfilename()
    with helper.ResizeImageForApplePass(icon_img_file_name, 'logo') as saved_img_file_names:
        pass
    return


def select_thumbnail_img() -> None:
    global thumbnail_img_file_name
    thumbnail_img_file_name = askopenfilename()
    with helper.ResizeImageForApplePass(thumbnail_img_file_name, 'thumbnail') as saved_img_file_names:
        pass
    return


def select_foreground_color() -> None:
    global foreground_color
    foreground_color = f"rgb{askcolor(title='Foreground Color Chooser')[0]}"
    return


def select_background_color() -> None:
    global background_color
    background_color = f"rgb{askcolor(title='Background Color Chooser')[0]}"
    return


def license_copyright() -> None:
    try:
        with open("LICENSE", 'r') as license_file:
            messagebox.showinfo('License and Copyright', license_file.read())
    except Exception as err:
        messagebox.showerror("Error", f"LICENSE and Copyright notice not found.\n\nError:\n{err}")
    finally:
        return


def exit_dialog(root_window: tk.Tk) -> None:
    if messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                              icon='warning') == 'yes':
        root_window.destroy()
    else:
        messagebox.showinfo('Return', 'You will now return to the application screen')
    return


def create_pass_json(left_entry_dict: dict, middle_entry_dict: dict, right_entry_dict: dict,
                     root_window: tk.Tk) -> None:
    """ TODO ... """
    global foreground_color, background_color, icon_img_file_name, thumbnail_img_file_name

    if not foreground_color or not background_color:
        messagebox.showerror('COLOR ERROR', "you haven't selected any foreground or background color", icon='warning')
        return

    # ask whether the user wants to continue despite unselected images (icon, thumbnail, logo etc..)
    if not icon_img_file_name:
        if messagebox.askquestion('MISSING IMG', 'du you like to continue without a icon', icon='warning') != 'yes':
            messagebox.showinfo('Return', 'You will now return to the application screen')
            return

    if not thumbnail_img_file_name:
        if messagebox.askquestion('MISSING IMG', 'du you like to continue without a thumbnail',
                                  icon='warning') != 'yes':
            messagebox.showinfo('Return', 'You will now return to the application screen')
            return

    # GET THE VALUES THE USER ENTERED IN THE GUI
    # left entry
    org_name, desc, logo_t, f_name, m_name, l_name, email, tel_p, tel_m,\
    b_day = [val.get() for val in left_entry_dict.values()]
    # middle emtry
    address, post_code, f_state, country, pref_lang, t_z, git_acc, insta, snap, twitter, telegram, discord, linkedin, \
    lichess, paypal = [val.get() for val in middle_entry_dict.values()]
    # right entry
    f_version, pass_type_id, team_id, auth_token, serial_num,\
    web_service_url = [val.get() for val in right_entry_dict.values()]

    # OPEN THE JSON FILE FOR UPDATING THE USER INPUT
    with open(os.path.join("BusinessCard.pass", "pass.json"), 'r') as pass_json_file:
        pass_json: json = json.load(pass_json_file)

    # CHARACTERISTICS OF THE BUSINESS CARD
    pass_json['formatVersion'] = int(f_version)
    pass_json['passTypeIdentifier'] = pass_type_id
    pass_json['teamIdentifier'] = team_id
    pass_json['authenticationToken'] = auth_token
    pass_json['serialNumber'] = serial_num
    pass_json['webServiceURL'] = web_service_url
    # VISUAL CHARACTERISTICS
    pass_json['foregroundColor'] = foreground_color
    pass_json['backgroundColor'] = background_color
    pass_json['organizationName'] = org_name
    pass_json['description'] = desc
    pass_json['logoText'] = logo_t
    # FRONT OF THE BUSINESS CARD
    pass_json['barcode']['message'] = helper.me_card_formatter(f"{f_name} {m_name}", l_name, email, tel_m, b_day)
    pass_json['generic']['primaryFields'][0]['value'] = f"{f_name} {m_name} {l_name}"
    pass_json['generic']['secondaryFields'][0]['value'] = email
    pass_json['generic']['secondaryFields'][1]['value'] = tel_p
    pass_json['generic']['secondaryFields'][2]['value'] = tel_m
    # BACK OF THE BUSINESS CARD
    for index, val in zip(range(15), [address, post_code, f_state, country, pref_lang, b_day, t_z, paypal, git_acc,
                                      insta, snap, twitter, telegram, discord, linkedin, lichess]):
        pass_json['generic']['backFields'][index]['value'] = val

    # WRITE THE UPDATED JSON TO THE BusinessCard.pass/pass.json FILE
    with open(os.path.join("BusinessCard.pass", "pass.json"), "w") as pass_json_file:
        pass_json_file.write(json.dumps(pass_json, indent=4))

    # finally after creating the business card destroy the gui
    root_window.destroy()
    return


def main() -> None:
    root = tk.Tk()
    root.title(f'business card creator - by Felix Drees - v{__version__}')
    root.configure(bg='black')
    canvas = tk.Canvas(root, height=TK_HEIGHT, width=TK_WIDTH, bg='gray')
    canvas.pack()

    # SPLIT THE CANVAS IN A LEFT MIDDLE AND RIGHT FRAME
    # left
    left_frame = tk.Frame(canvas, bg='black')
    left_frame.place(relx=0, rely=0.1, relheight=0.8, relwidth=0.33)
    # middle
    middle_frame = tk.Frame(canvas, bg='black')
    middle_frame.place(relx=0.33, rely=0.1, relheight=0.8, relwidth=0.33)
    # right
    right_frame = tk.Frame(canvas, bg='black')
    right_frame.place(relx=0.66, rely=0.1, relheight=0.8, relwidth=0.34)

    # HEADING
    heading_text = "BUSINESS CARD CREATOR \n\nFor mor information read the projects README.md\nThere you will be " \
                   "instructed how you can / should fill out the fields "
    heading = tk.Label(root, text=heading_text, bg='gray')
    heading.place(relx=0.15, rely=0.01, relheight=0.08, relwidth=0.65)

    # LEFT FRAME
    left_frame_keys_and_default_texts = {
        'organisation name': 'Example GmbH & Co. KG', "description": "business card", "logo text": '',
        'first name': 'Max', 'middle names': '', 'last name': 'Mustermann',
        'email': '', 'tel privat': '', 'tel mobile': '',
        'date of birth': '19990526'
    }
    left_entry_dict = helper.place_label_and_entry_fields(left_frame, 'snow', left_frame_keys_and_default_texts,
                                                          distance=.06, height=0.05)
    # select a icon img
    select_icon_img_button = tk.Button(left_frame, text="select icon img", bg="snow", command=select_icon_img)
    select_icon_img_button.place(relx=0.05, rely=0.66, relheight=0.05, relwidth=0.85)
    # select a thumbnail img
    select_thumbnail_img_button = tk.Button(left_frame, text="select thumbnail img", bg="snow",
                                            command=select_thumbnail_img)
    select_thumbnail_img_button.place(relx=0.05, rely=0.72, relheight=0.05, relwidth=0.85)

    # MIDDLE FRAME
    middle_frame_keys_and_default_texts = {
        "street + house num": "Example str. 1", "post code": "28205", "federal state": "HB", "country": "DE",
        "preferred language": "german, english", "time zone": "+0100", "github account": '', "instagram account": '',
        "snapchat account": '', "twitter account": '', "telegram account": '', "discord account": '',
        "Linkedin account": '', "Lichess account": '', "PayPal": "@..."
    }
    middle_entry_dict = helper.place_label_and_entry_fields(middle_frame, 'snow', middle_frame_keys_and_default_texts,
                                                            distance=0.059, height=0.05)

    # RIGHT FRAME
    right_frame_keys_and_default_texts = {
        "format version": "1", "* pass type identifier": '', "* team identifier": '',
        "authentication token": '', "serial number": "123456", "web service url": ''
    }
    right_entry_dict = helper.place_label_and_entry_fields(right_frame, 'snow', right_frame_keys_and_default_texts,
                                                           distance=0.06, height=0.05)

    # select foreground-color
    select_foreground_color_button = tk.Button(right_frame, text="select foreground color", bg="snow",
                                               command=select_foreground_color)
    select_foreground_color_button.place(relx=0.05, rely=0.425, relheight=0.05, relwidth=0.85)

    # select background-color
    select_background_color_button = tk.Button(right_frame, text="select background color", bg="snow",
                                               command=select_background_color)
    select_background_color_button.place(relx=0.05, rely=0.5, relheight=0.05, relwidth=0.85)

    # SUBMIT, EXIT AND LICENSE BUTTON
    submit_button = tk.Button(root, text="SUBMIT", bg="gray",
                              command=lambda: create_pass_json(left_entry_dict, middle_entry_dict, right_entry_dict,
                                                               root_window=root))
    submit_button.place(relx=0.35, rely=0.925, relheight=0.05, relwidth=0.1)

    exit_button = tk.Button(root, text="EXIT", bg="gray", command=lambda: exit_dialog(root_window=root))
    exit_button.place(relx=0.55, rely=0.925, relheight=0.05, relwidth=0.1)

    license_copyright_button = tk.Button(root, text="LICENSE (c)", bg="gray", command=license_copyright)
    license_copyright_button.place(relx=0.85, rely=0.925, relheight=0.05, relwidth=0.1)

    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        messagebox.showerror('ERROR', f'Error message:\n{err}')
        raise SystemExit(err)
