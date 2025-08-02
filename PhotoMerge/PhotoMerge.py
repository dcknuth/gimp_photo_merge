#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gimp, GimpUi, GObject, Gtk, Gio

import sys, os, getpass, subprocess
DEBUG = 4
tmp_base = r"C:\\Users\\"
user_name = getpass.getuser()
tmp_file_end = r"\\AppData\\Roaming\\GIMP\\3.0\\tmp\\photo_merge_tmp.png"
tmp_file = ''.join([tmp_base, user_name, tmp_file_end])
exe_loc = r"\\AppData\\Roaming\\GIMP\\3.0\\scripts\\do_photo_merge\\"
exe_name = "do_photo_merge.exe"
EXE_PATH = ''.join([tmp_base, user_name, exe_loc, exe_name])

class PhotoMerge(Gimp.PlugIn):
    # Plugin properties
    __gproperties__ = {
        "name": (str, "Name", "The name of the plugin", "Photo Merge", GObject.ParamFlags.READWRITE),
    }

    def __init__(self):
        super().__init__()

    def do_query_procedures(self):
        # Register the procedure
        return ["plug-in-photo-merge"]

    def do_create_procedure(self, name):
        if name == "plug-in-photo-merge":
            procedure = Gimp.ImageProcedure.new(
                self, name, 
                Gimp.PDBProcType.PLUGIN,
                self.run, None
            )
            
            # Always available, even without open images
            procedure.set_image_types("*")
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
            procedure.set_menu_label("Photo Merge...")
            # Place in main File menu, accessible without open images
            procedure.add_menu_path('<Image>/File/[Open]')
            
            procedure.set_documentation(
                "Opens images to create a photo merge",
                "This plugin opens a file selection dialog to choose images to merge",
                name
            )
            
            procedure.set_attribution("David Knuth", "David Knuth", "2025")
            if (DEBUG > 4):
                Gimp.message("Finished creating procedure")
            return procedure
        
        return None

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if (DEBUG > 4):
            Gimp.message("Running plugin now...")
        # Create and show the file selection dialog
        if run_mode == Gimp.RunMode.INTERACTIVE:
            if (DEBUG > 4):
                Gimp.message("Running in interactive mode")
            
            selected_files = self.show_file_dialog()
            if (DEBUG > 4):
                Gimp.message("We have a file list")
            
            if selected_files:
                if (DEBUG > 4):
                    Gimp.message("We can now combine the images")
                self.process_selected_images(selected_files)
                return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
            else:
                # User cancelled or no files selected
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def show_file_dialog(self):
        """Shows a file selection dialog and returns selected file paths"""
        
        # Create file chooser dialog
        dialog = Gtk.FileChooserDialog(
            title="Select Images",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        
        # Add buttons
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        # Allow multiple selection
        dialog.set_select_multiple(True)
        
        # Set up file filters for images
        filter_images = Gtk.FileFilter()
        filter_images.set_name("Image files")
        filter_images.add_mime_type("image/jpeg")
        filter_images.add_mime_type("image/png")
        filter_images.add_mime_type("image/gif")
        filter_images.add_mime_type("image/bmp")
        filter_images.add_mime_type("image/tiff")
        filter_images.add_pattern("*.jpg")
        filter_images.add_pattern("*.jpeg")
        filter_images.add_pattern("*.png")
        filter_images.add_pattern("*.gif")
        filter_images.add_pattern("*.bmp")
        filter_images.add_pattern("*.tif")
        filter_images.add_pattern("*.tiff")
        dialog.add_filter(filter_images)
        
        # All files filter
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)
        
        home_dir = os.path.expanduser("~")
        dialog.set_current_folder(home_dir)
        
        selected_files = []
        
        # Run the dialog
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            selected_files = dialog.get_filenames()
            
        dialog.destroy()
        return selected_files

    def process_selected_images(self, file_paths):
        """Process the selected image files"""
        
        print(f"Selected {len(file_paths)} files:")
        for file_path in file_paths:
            print(f"  - {file_path}")
        
        # Do the actual merge with an external call
        args = [EXE_PATH, '--output', tmp_file] + file_paths
        result = subprocess.run(args)
        if result.returncode < 0:
            Gimp.message(f"Error running the merge command: {result.returncode}")
        else:
            # Open the merged image in GIMP
            try:
                # Load the image
                image = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, 
                                     Gio.File.new_for_path(tmp_file))
                
                # Display the image
                display = Gimp.Display.new(image)
                
                # delete the temporary file
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
                
            except Exception as e:
                print(f"Error opening {tmp_file}: {str(e)}")
        if (DEBUG > 4):
            Gimp.message("Processing done")

# Register the plugin
Gimp.main(PhotoMerge.__gtype__, sys.argv)