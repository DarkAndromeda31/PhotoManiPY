"""
Module: PhotoManiPY for Photo ManiPY
Description:

Made by: Maximilian Rose
Created on 13/02/2020
IDE: PyCharm
"""

import pathlib as pl
import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk

import codec
import edit_image as ei
import manage_image as mi


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):
        def update_outpath(path):
            """
            Function that adds the changes to the filename then sets the output to this, this is that any changes in
            what edits are going to be done are reflected if those changes are made after the filename was last loaded.

            :param path: The path of the file that will be used
            """
            hsl = f"({tool_hue_shift_hue.get()},{tool_hue_shift_sat.get()},{tool_hue_shift_lum.get()})"
            crop = f"({tool_crop_top.get()},{tool_crop_bottom.get()})"
            resize = f"(x{tool_resize_vertical.get()},x{tool_resize_horizontal.get()})"

            outpath = path.replace(pl.Path(path).suffix, "") + hsl + crop + resize + current_dropdown.get()

            file_io_output_path.delete(0, tk.END)
            file_io_output_path.insert(0, outpath)

        def browse_file_in():
            """
            Function that opens a file browse dialogue then changes the input entry box and output entry box accordingly
            """
            # File dialogue
            filetypes = file_io_input_ext_entry.get().replace(":", " ")
            path = filedialog.askopenfilename(
                filetypes=(("Image Files", filetypes), ("All files", "*")))  # Add the readout from the other entry

            # Change the input boxes to reflect loaded path
            file_io_input_path.delete(0, tk.END)
            file_io_input_path.insert(0, path)

            # Change to default values of crop
            cur_image = mi.open_image(file_io_input_path.get())
            width, height = cur_image.size

            tool_crop_bottom.delete(0, tk.END)
            tool_crop_bottom.insert(0, width)

            tool_crop_bottom2.delete(0, tk.END)
            tool_crop_bottom2.insert(0, height)

            update_outpath(path)

        def browse_file_out():
            """
            Function that opens a folder browse dialouge then changes output path accordingly
            TODO: Make this a functining system not whatever it is now
            """
            file_io_output_path.delete(0, tk.END)
            path = filedialog.askopenfilename(
                filetypes=(("Image Files", "*.jpg"), ("All files", "*")))  # Add the readout from the other entry
            file_io_output_path.insert(0, path)

        def execute_file():
            """
            Function that applies the changes to the file indicated by the filepath, It first finds the values used
            for the changes, then applies them in the order:
            1. Crop the image
            2. Shift the hue of the image
            3. Resize the image
            4. Any other post-processing effects
            5. Save the image
            """

            # Update filename
            update_outpath(file_io_input_path.get())

            # Find changes
            cur_image = mi.open_image(file_io_input_path.get())
            crop_point1 = (int(tool_crop_top.get()), int(tool_crop_top2.get()))
            crop_point2 = (int(tool_crop_bottom.get()), int(tool_crop_bottom2.get()))
            hue_shift = int(tool_hue_shift_hue.get())
            sat_shift = int(tool_hue_shift_sat.get())
            lum_shift = int(tool_hue_shift_lum.get())
            resize_x = float(tool_resize_horizontal.get())
            resize_y = float(tool_resize_vertical.get())
            output = file_io_output_path.get()

            # Apply changes
            cur_image = ei.crop(cur_image, crop_point1, crop_point2)
            cur_image = ei.shift_hsl(cur_image, hue_shift, sat_shift, lum_shift)
            cur_image = ei.resize(cur_image, (resize_x, resize_y))

            # Save image
            if ".maxpg" in output:
                codec.save_as_codec(cur_image, output)
            else:
                mi.save_image(cur_image, output)

        def open_preview():
            """
            Function to open a preview window of the image indicated from the filepath
            """

            filepath = pl.Path(file_io_input_path.get())
            prev_win = tk.Toplevel()
            prev_win.wm_title(filepath.name)

            # Find changes
            cur_image = mi.open_image(file_io_input_path.get())
            crop_point1 = (int(tool_crop_top.get()), int(tool_crop_top2.get()))
            crop_point2 = (int(tool_crop_bottom.get()), int(tool_crop_bottom2.get()))
            hue_shift = int(tool_hue_shift_hue.get())
            sat_shift = int(tool_hue_shift_sat.get())
            lum_shift = int(tool_hue_shift_lum.get())
            resize_x = float(tool_resize_horizontal.get())
            resize_y = float(tool_resize_vertical.get())
            # output = file_io_output_path.get()

            # Apply changes
            cur_image = ei.crop(cur_image, crop_point1, crop_point2)
            cur_image = ei.shift_hsl(cur_image, hue_shift, sat_shift, lum_shift)
            cur_image = ei.resize(cur_image, (resize_x, resize_y))

            pic = ImageTk.PhotoImage(cur_image)

            img = tk.Label(prev_win, image=pic)
            img.image = pic

            img.grid(row=0, column=0)

        def open_GUI():
            filepath = pl.Path(file_io_input_path.get())
            gui_win = tk.Toplevel()
            gui_win.wm_title(filepath.name)

            toolbar = tk.Frame(gui_win, bd=1, relief="raised")
            toolbar.grid(row=0, column=0)

            crop_icon = mi.open_image("crop_icon.png")
            crop_image = ImageTk.PhotoImage(crop_icon)

            gui_tool_crop_button = tk.Button(toolbar, image=crop_image)

            gui_tool_crop_button.grid(row=0, column=0)

            # Find changes
            print(file_io_input_path.get())
            cur_image = mi.open_image(file_io_input_path.get())
            crop_point1 = (int(tool_crop_top.get()), int(tool_crop_top2.get()))
            crop_point2 = (int(tool_crop_bottom.get()), int(tool_crop_bottom2.get()))
            hue_shift = int(tool_hue_shift_hue.get())
            sat_shift = int(tool_hue_shift_sat.get())
            lum_shift = int(tool_hue_shift_lum.get())
            resize_x = float(tool_resize_horizontal.get())
            resize_y = float(tool_resize_vertical.get())

            # Apply changes
            cur_image = ei.crop(cur_image, crop_point1, crop_point2)
            cur_image = ei.shift_hsl(cur_image, hue_shift, sat_shift, lum_shift)
            cur_image = ei.resize(cur_image, (resize_x, resize_y))

            main_pic = ImageTk.PhotoImage(cur_image)

            img = tk.Label(gui_win, image=main_pic)

            img.grid(row=1, column=0)

        # ----- WINDOW -----
        # Setup window
        self.master.title("Photo ManiPy")
        self.grid(row=0, column=0)

        # ----- FRAMES -----
        # Define the Frames for each section
        file_io = tk.LabelFrame(self, text='File I/O')  # remove dimensions when filled
        tool = tk.LabelFrame(self, text='Tools')
        image = tk.LabelFrame(self, text='Image')

        file_io.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)
        tool.grid(row=1, column=0, columnspan=3, rowspan=6, sticky="NSEW", padx=5, pady=5)
        image.grid(row=0, column=2, columnspan=2, sticky="NSEW", padx=5, pady=5)

        # Define sub-frames for file IO
        file_io_input_ext = tk.LabelFrame(file_io, text='Input file extensions')
        file_io_output_ext = tk.LabelFrame(file_io, text='Output extension')

        file_io_input_ext.grid(row=2, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)
        file_io_input_ext.grid_columnconfigure(0, weight=1)
        file_io_output_ext.grid(row=2, column=2, columnspan=1, sticky="NSW", padx=5, pady=5)

        # Define sub-frames for tools
        tool_hue_shift = tk.LabelFrame(tool, text='Shift Hue')
        tool_crop = tk.LabelFrame(tool, text='Crop')
        tool_resize = tk.LabelFrame(tool, text='Resize')

        tool_hue_shift.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
        tool_crop.grid(row=0, column=1, sticky="NSEW", padx=5, pady=5)
        tool_resize.grid(row=0, column=2, sticky="NSEW", padx=5, pady=5)

        # ----- WIDGETS -----
        # Define widgets for file IO main
        file_io_input_path_text = tk.Label(file_io, text="Input Path:\n(File or Folder)")
        file_io_input_path = tk.Entry(file_io, width=75)
        file_io_browse_in = tk.Button(file_io, text='Browse', command=browse_file_in)
        file_io_output_path_text = tk.Label(file_io, text="Output Path:")
        file_io_output_path = tk.Entry(file_io, width=75)
        file_io_browse_out = tk.Button(file_io, text='Browse', command=browse_file_out)

        file_io_input_path_text.grid(row=0, column=0, padx=5, pady=5)
        file_io_input_path.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        file_io_browse_in.grid(row=0, column=4, padx=5, pady=5)
        file_io_output_path_text.grid(row=1, column=0, padx=5, pady=5)
        file_io_output_path.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        file_io_browse_out.grid(row=1, column=4, padx=5, pady=5)

        # Define widgets for file IO input extensions
        file_io_input_ext_entry = tk.Entry(file_io_input_ext)
        file_io_input_ext_entry.insert(0, "*.png:*.jpg:*.jpeg")

        file_io_input_ext_entry.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # Define widgets for file IO output extension
        dropdown_options = [".png", ".jpg", ".bmp", ".maxpg"]
        current_dropdown = tk.StringVar(self)
        current_dropdown.set(dropdown_options[0])

        file_io_output_ext_dropdown = tk.OptionMenu(file_io_output_ext, current_dropdown, *dropdown_options)
        file_io_output_ext_dropdown.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # Define widgets for image preview
        image_preview_test = tk.Label(image, text="Test")
        file_io_preview_open = tk.Button(image, text="Open Preview", command=open_preview)

        image_preview_test.grid(row=0, column=0, padx=5, pady=5)
        file_io_preview_open.grid(row=1, column=0, padx=5, pady=5)

        # Define widgets for image GUI button
        image_gui_test = tk.Label(image, text="Test")
        image_gui_open = tk.Button(image, text="Open Graphical Editor", command=open_GUI)

        image_gui_test.grid(row=0, column=1, padx=5, pady=5)
        image_gui_open.grid(row=1, column=1, padx=5, pady=5)

        # Define widgets for hue_shift
        tool_hue_shift_hue_text = tk.Label(tool_hue_shift, text="Hue:")
        tool_hue_shift_hue = tk.Spinbox(tool_hue_shift, from_=0, to=360, justify='right')
        tool_hue_shift_sat_text = tk.Label(tool_hue_shift, text="Saturation:")
        tool_hue_shift_sat = tk.Spinbox(tool_hue_shift, from_=-100, to=100, justify='right')
        tool_hue_shift_lum_text = tk.Label(tool_hue_shift, text="Luminance:")
        tool_hue_shift_lum = tk.Spinbox(tool_hue_shift, from_=-100, to=100, justify='right')

        tool_hue_shift_hue_text.grid(row=0, column=0, padx=5, pady=3)
        tool_hue_shift_hue.grid(row=0, column=1, padx=5, pady=3)
        tool_hue_shift_sat_text.grid(row=1, column=0, padx=5, pady=3)
        tool_hue_shift_sat.grid(row=1, column=1, padx=5, pady=3)
        tool_hue_shift_lum_text.grid(row=2, column=0, padx=5, pady=3)
        tool_hue_shift_lum.grid(row=2, column=1, padx=5, pady=3)

        tool_hue_shift_sat.delete(0, tk.END)
        tool_hue_shift_sat.insert(0, "0")
        tool_hue_shift_lum.delete(0, tk.END)
        tool_hue_shift_lum.insert(0, "0")

        # Define widgets for crop
        tool_crop_top_text = tk.Label(tool_crop, text="Point 1 x:")
        tool_crop_top = tk.Spinbox(tool_crop, from_=0, to=9999999999999, justify='right')
        tool_crop_bottom_text = tk.Label(tool_crop, text="Point 2 x:")
        tool_crop_bottom = tk.Spinbox(tool_crop, from_=0, to=9999999999999, justify='right')
        tool_crop_top_text2 = tk.Label(tool_crop, text="Point 1 y:")
        tool_crop_top2 = tk.Spinbox(tool_crop, from_=0, to=9999999999999, justify='right')
        tool_crop_bottom_text2 = tk.Label(tool_crop, text="Point 2 y:")
        tool_crop_bottom2 = tk.Spinbox(tool_crop, from_=0, to=9999999999999, justify='right')

        tool_crop_top_text.grid(row=0, column=0, padx=5, pady=3)
        tool_crop_top.grid(row=0, column=1, padx=5, pady=3)
        tool_crop_bottom_text.grid(row=1, column=0, padx=5, pady=3)
        tool_crop_bottom.grid(row=1, column=1, padx=5, pady=3)
        tool_crop_top_text2.grid(row=0, column=2, padx=5, pady=3)
        tool_crop_top2.grid(row=0, column=3, padx=5, pady=3)
        tool_crop_bottom_text2.grid(row=1, column=2, padx=5, pady=3)
        tool_crop_bottom2.grid(row=1, column=3, padx=5, pady=3)

        # Define widgets for resize
        tool_resize_vertical_text = tk.Label(tool_resize, text="Vertical Scale:")
        tool_resize_vertical = tk.Spinbox(tool_resize, from_=0, to=9999999999999, increment=0.1, justify='right')
        tool_resize_horizontal_text = tk.Label(tool_resize, text="Horizontal Scale:")
        tool_resize_horizontal = tk.Spinbox(tool_resize, from_=0, to=9999999999999, increment=0.1, justify='right')

        tool_resize_vertical_text.grid(row=0, column=0, padx=5, pady=3)
        tool_resize_vertical.grid(row=0, column=1, padx=5, pady=3)
        tool_resize_horizontal_text.grid(row=1, column=0, padx=5, pady=3)
        tool_resize_horizontal.grid(row=1, column=1, padx=5, pady=3)

        tool_resize_vertical.delete(0, tk.END)
        tool_resize_vertical.insert(0, "1.0")
        tool_resize_horizontal.delete(0, tk.END)
        tool_resize_horizontal.insert(0, "1.0")

        # Other buttons
        tool_apply_button = tk.Button(tool, text="Apply", command=execute_file)
        tool_apply_button.grid(row=0, column=3, padx=5, pady=5)


def main():
    root = tk.Tk()

    # make it
    Window(root)
    root.resizable(False, False)

    root.mainloop()


if __name__ == '__main__':
    main()
