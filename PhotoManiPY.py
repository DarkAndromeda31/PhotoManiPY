"""
Module: PhotoManiPY for Photo ManiPY
Description:

Made by: Maximilian Rose
Created on 13/02/2020
IDE: PyCharm
"""

import pathlib as pl
import tkinter as tk
from tkinter import filedialog, ttk

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
            subpixel = f"({subpixel_activated.get()})"

            outpath = path.replace(pl.Path(path).suffix, "") + hsl + crop + resize + subpixel + str(
                file_io_output_ext_dropdown.get())

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
            Function that opens a folder browse dialogue then changes output path accordingly
            TODO: Make this a functioning system not whatever it is now
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

            # Apply effects
            if subpixel_activated.get():
                cur_image = ei.subpixel_conversion(cur_image)

            # Save image
            if ".maxpg" in output:
                codec.save_as_codec(cur_image, output)
            else:
                mi.save_image(cur_image, output)

        def execute_temp():
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
            path = file_io_output_path.get()

            # Apply changes
            cur_image = ei.crop(cur_image, crop_point1, crop_point2)
            cur_image = ei.shift_hsl(cur_image, hue_shift, sat_shift, lum_shift)
            cur_image = ei.resize(cur_image, (resize_x, resize_y))

            # Apply effects
            if subpixel_activated.get():
                cur_image = ei.subpixel_conversion(cur_image)

            path = "./temp/" + pl.Path(path).name
            mi.save_image(cur_image, path)

            file_io_input_path.delete(0, tk.END)
            file_io_input_path.insert(0, path)

        def open_preview():
            """
            Function to open a preview window of the image indicated from the filepath
            """

            filepath = pl.Path(file_io_input_path.get())
            prev_win = tk.Toplevel()
            prev_win.wm_title(filepath.name)
            prev_win.resizable(False, False)

            # Find changes
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

            # Apply effects
            if subpixel_activated.get():
                cur_image = ei.subpixel_conversion(cur_image)

            pic = ImageTk.PhotoImage(cur_image)

            img = ttk.Label(prev_win, image=pic)
            img.image = pic

            img.grid(row=0, column=0)

        def open_GUI():
            def getorigin(eventorigin):
                global x0, y0
                x0 = eventorigin.x
                y0 = eventorigin.y
                print("Point 1:", x0, y0)

                gui_win.bind("<Button 1>", getendpoint)

            def getendpoint(eventorigin):
                global x1, y1
                x1 = eventorigin.x
                y1 = eventorigin.y
                print("Point 2:", x1, y1)
                gui_win.unbind("<Button 1>")
                img.configure(cursor="")

                # Do the crop thing
                point_1 = (x0, y0)
                point_2 = (x1, y1)
                print("P1:", point_1, "P2:", point_2)

                temp_image = mi.open_image(file_io_input_path.get())
                temp_image = ei.crop(temp_image, point_1, point_2)

                path = "./temp/" + pl.Path(file_io_input_path.get()).name
                mi.save_image(temp_image, path)

                file_io_input_path.delete(0, tk.END)
                file_io_input_path.insert(0, path)

                new_image = mi.open_image("./temp/" + pl.Path(file_io_input_path.get()).name)
                new_image = ImageTk.PhotoImage(new_image)
                img.configure(image=new_image)
                img.image = new_image

            def visual_crop():
                img.configure(cursor="crosshair")
                gui_win.bind("<Button 1>", getorigin)

            # ----- WINDOW -----
            # Setup window
            filepath = pl.Path(file_io_input_path.get())
            gui_win = tk.Toplevel()
            gui_win.wm_title(filepath.name)
            gui_win.resizable(False, False)
            gui_win.iconbitmap("./images/favicon.ico")

            # ----- FRAMES -----
            # Define the Frames for each section
            toolbar = ttk.Frame(gui_win, relief="raised")
            toolbar.grid(row=0, column=0)

            # ----- WIDGETS -----
            # Define toolbar buttons
            crop_icon = mi.open_image("./images/crop_icon.png")
            crop_image = ImageTk.PhotoImage(crop_icon)

            gui_tool_crop_button = ttk.Button(toolbar, image=crop_image, command=visual_crop)
            gui_tool_crop_button.image = crop_image

            gui_tool_crop_button.grid(row=0, column=0)

            # Define image display
            cur_image = mi.open_image(file_io_input_path.get())

            main_pic = ImageTk.PhotoImage(cur_image)

            img = ttk.Label(gui_win, image=main_pic)
            img.image = main_pic

            img.grid(row=1, column=0)

        # ----- WINDOW -----
        # Setup window
        self.master.title("Photo ManiPy")
        self.master.iconbitmap("./images/favicon.ico")
        self.grid(row=0, column=0)

        # ----- FRAMES -----
        # Define the Frames for each section
        file_io = ttk.LabelFrame(self, text='File I/O')  # remove dimensions when filled
        tool = ttk.LabelFrame(self, text='Tools')
        image = ttk.LabelFrame(self, text='Image')

        file_io.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)
        tool.grid(row=1, column=0, columnspan=3, rowspan=6, sticky="NSEW", padx=5, pady=5)
        image.grid(row=0, column=2, columnspan=2, sticky="NSEW", padx=5, pady=5)

        # Define sub-frames for file IO
        file_io_input_ext = ttk.LabelFrame(file_io, text='Input file extensions')
        file_io_output_ext = ttk.LabelFrame(file_io, text='Output extension')

        file_io_input_ext.grid(row=2, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)
        file_io_input_ext.grid_columnconfigure(0, weight=1)
        file_io_output_ext.grid(row=2, column=2, columnspan=1, sticky="NSW", padx=5, pady=5)

        # Define sub-frames for tools
        tool_hue_shift = ttk.LabelFrame(tool, text='Shift Hue')
        tool_crop = ttk.LabelFrame(tool, text='Crop')
        tool_resize = ttk.LabelFrame(tool, text='Resize')
        tool_effects = ttk.LabelFrame(tool, text='Effects')

        tool_hue_shift.grid(row=0, column=0, rowspan=2, sticky="NSEW", padx=5, pady=5)
        tool_crop.grid(row=0, column=1, rowspan=2, sticky="NSEW", padx=5, pady=5)
        tool_resize.grid(row=0, column=2, rowspan=2, sticky="NSEW", padx=5, pady=5)
        tool_effects.grid(row=0, column=3, rowspan=2, sticky="NSEW", padx=5, pady=5)

        # ----- WIDGETS -----
        # Define widgets for file IO main
        file_io_input_path_text = ttk.Label(file_io, text="Input Path:\n(File or Folder)")
        file_io_input_path = ttk.Entry(file_io, width=75)
        file_io_browse_in = ttk.Button(file_io, text='Browse', command=browse_file_in)
        file_io_output_path_text = ttk.Label(file_io, text="Output Path:")
        file_io_output_path = ttk.Entry(file_io, width=75)
        file_io_browse_out = ttk.Button(file_io, text='Browse', command=browse_file_out)

        file_io_input_path_text.grid(row=0, column=0, padx=5, pady=5)
        file_io_input_path.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        file_io_browse_in.grid(row=0, column=4, padx=5, pady=5)
        file_io_output_path_text.grid(row=1, column=0, padx=5, pady=5)
        file_io_output_path.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        file_io_browse_out.grid(row=1, column=4, padx=5, pady=5)

        # Define widgets for file IO input extensions
        file_io_input_ext_entry = ttk.Entry(file_io_input_ext)
        file_io_input_ext_entry.insert(0, "*.png:*.jpg:*.jpeg")

        file_io_input_ext_entry.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # Define widgets for file IO output extension
        dropdown_options = [".png", ".jpg", ".bmp", ".maxpg"]

        file_io_output_ext_dropdown = ttk.Combobox(file_io_output_ext, values=dropdown_options)
        file_io_output_ext_dropdown.current(0)

        file_io_output_ext_dropdown.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # Define widgets for image preview
        image_preview_test = ttk.Label(image, text="Preview")
        file_io_preview_open = ttk.Button(image, text="Open", command=open_preview)

        image_preview_test.grid(row=0, column=0, padx=5, pady=5)
        file_io_preview_open.grid(row=0, column=1, padx=5, pady=5)

        # Define widgets for image GUI button
        image_gui_test = ttk.Label(image, text="Graphical Editor")
        image_gui_open = ttk.Button(image, text="Open", command=open_GUI)

        image_gui_test.grid(row=1, column=0, padx=5, pady=5)
        image_gui_open.grid(row=1, column=1, padx=5, pady=5)

        # Define widgets for hue_shift
        tool_hue_shift_hue_text = ttk.Label(tool_hue_shift, text="Hue:")
        tool_hue_shift_hue = ttk.Spinbox(tool_hue_shift, from_=0, to=360, style="TSpinbox")
        tool_hue_shift_sat_text = ttk.Label(tool_hue_shift, text="Saturation:")
        tool_hue_shift_sat = ttk.Spinbox(tool_hue_shift, from_=-100, to=100, style="TSpinbox")
        tool_hue_shift_lum_text = ttk.Label(tool_hue_shift, text="Luminance:")
        tool_hue_shift_lum = ttk.Spinbox(tool_hue_shift, from_=-100, to=100, style="TSpinbox")

        tool_hue_shift_hue_text.grid(row=0, column=0, padx=5, pady=3)
        tool_hue_shift_hue.grid(row=0, column=1, padx=5, pady=3)
        tool_hue_shift_sat_text.grid(row=1, column=0, padx=5, pady=3)
        tool_hue_shift_sat.grid(row=1, column=1, padx=5, pady=3)
        tool_hue_shift_lum_text.grid(row=2, column=0, padx=5, pady=3)
        tool_hue_shift_lum.grid(row=2, column=1, padx=5, pady=3)

        tool_hue_shift_hue.delete(0, tk.END)
        tool_hue_shift_hue.insert(0, "0")
        tool_hue_shift_sat.delete(0, tk.END)
        tool_hue_shift_sat.insert(0, "0")
        tool_hue_shift_lum.delete(0, tk.END)
        tool_hue_shift_lum.insert(0, "0")

        # Define widgets for crop
        tool_crop_top_text = ttk.Label(tool_crop, text="Point 1 x:")
        tool_crop_top = ttk.Spinbox(tool_crop, from_=0, to=9999999999999, style="TSpinbox")
        tool_crop_bottom_text = ttk.Label(tool_crop, text="Point 2 x:")
        tool_crop_bottom = ttk.Spinbox(tool_crop, from_=0, to=9999999999999, style="TSpinbox")
        tool_crop_top_text2 = ttk.Label(tool_crop, text="Point 1 y:")
        tool_crop_top2 = ttk.Spinbox(tool_crop, from_=0, to=9999999999999, style="TSpinbox")
        tool_crop_bottom_text2 = ttk.Label(tool_crop, text="Point 2 y:")
        tool_crop_bottom2 = ttk.Spinbox(tool_crop, from_=0, to=9999999999999, style="TSpinbox")

        tool_crop_top_text.grid(row=0, column=0, padx=5, pady=3)
        tool_crop_top.grid(row=0, column=1, padx=5, pady=3)
        tool_crop_bottom_text.grid(row=1, column=0, padx=5, pady=3)
        tool_crop_bottom.grid(row=1, column=1, padx=5, pady=3)
        tool_crop_top_text2.grid(row=0, column=2, padx=5, pady=3)
        tool_crop_top2.grid(row=0, column=3, padx=5, pady=3)
        tool_crop_bottom_text2.grid(row=1, column=2, padx=5, pady=3)
        tool_crop_bottom2.grid(row=1, column=3, padx=5, pady=3)

        tool_crop_top.delete(0, tk.END)
        tool_crop_top.insert(0, "0")
        tool_crop_bottom.delete(0, tk.END)
        tool_crop_bottom.insert(0, "0")
        tool_crop_top2.delete(0, tk.END)
        tool_crop_top2.insert(0, "0")
        tool_crop_bottom2.delete(0, tk.END)
        tool_crop_bottom2.insert(0, "0")

        # Define widgets for resize
        tool_resize_vertical_text = ttk.Label(tool_resize, text="Vertical Scale:")
        tool_resize_vertical = ttk.Spinbox(tool_resize, from_=0, to=9999999999999, increment=0.1, style="TSpinbox")
        tool_resize_horizontal_text = ttk.Label(tool_resize, text="Horizontal Scale:")
        tool_resize_horizontal = ttk.Spinbox(tool_resize, from_=0, to=9999999999999, increment=0.1, style="TSpinbox")

        tool_resize_vertical_text.grid(row=0, column=0, padx=5, pady=3)
        tool_resize_vertical.grid(row=0, column=1, padx=5, pady=3)
        tool_resize_horizontal_text.grid(row=1, column=0, padx=5, pady=3)
        tool_resize_horizontal.grid(row=1, column=1, padx=5, pady=3)

        tool_resize_vertical.delete(0, tk.END)
        tool_resize_vertical.insert(0, "1.0")
        tool_resize_horizontal.delete(0, tk.END)
        tool_resize_horizontal.insert(0, "1.0")

        # Define widgets for effects
        subpixel_activated = tk.IntVar()
        subpixel_activated.set(0)
        tool_effects_subpixel = ttk.Checkbutton(tool_effects, text="Subpixel Rendering", variable=subpixel_activated)

        tool_effects_subpixel.grid(row=0, column=0, padx=5, pady=3)

        # Other buttons
        tool_apply_button = ttk.Button(tool, text="Apply Changes", command=execute_temp)
        tool_apply_save_button = ttk.Button(tool, text="Apply and Save", command=execute_file)
        tool_apply_button.grid(row=0, column=4, padx=5, pady=5)
        tool_apply_save_button.grid(row=1, column=4, padx=5, pady=5)


def main():
    root = tk.Tk()

    # make it
    Window(root)
    root.resizable(False, False)

    root.mainloop()


if __name__ == '__main__':
    main()
