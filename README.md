# GIMP Photo Merge Plugin
A GIMP 3.0+ plugin to photomerge the selected files and then open the merged one up in GIMP

## Installation
This will be for Windows under a protected installation, so there are some extra hurdles. I will list out the steps, but I may also try to supply a script to set everything up
1. Ensure there is a *plug-ins* directory at `C:\Users\YOUR_USER_NAME\AppData\Roaming\GIMP\3.0\`
1. Copy the *PhotoMerge* directory and *PhotoMerge.py* Python script from the repo into the *plug-ins* directory
1. Ensure there is a *scripts* directory in the same location
1. Download the *do_photo_merge.zip* file and expand into the *scripts* directory
1. There should now be a *do_photo_merge* directory inside the *scripts* directory. It should contain a *do_poto_merge.exe* and an *_internal* directory with all the dependencies
1. Launch GIMP and you should see a new menu selection in the File menu called *Photo Merge...* which will let you select files to merge and merge them

## Things Learned
* It was hard to find how to get the menu into the place I wanted it.
The base example puts the new menu in Filters -> Tutorial with `procedure.add_menu_path('<Image>/Filters/Tutorial/')`, but you will need something like `procedure.add_menu_path('<Image>/File/[Open]')` to put your menu item in the file related area. The part in square brackets is called a 'named section' of the menu and an LLM or search can tell you about them after you know the name
* You might think you can copy modules from a local Python installation. Then add to the path with `sys.path.append(r"C:\Users\YOUR_USER_NAME\AppData\Roaming\GIMP\3.0\lib")` or a similar directory. However, this does not seem to work
* Since there seemed to be no way to get the modules needed into the Python installation that comes with the normally packaged GIMP for Windows, I decided to call an outside instance of Python with numpy and cv2 installed
* I used PyInstaller to make this work and be easy to distribute. The drawback is that it is big, somewhat convoluted and may trigger Windows Defender
* I did not include the venv that I used or the build directory that PyInstaller created in the repo