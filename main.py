#!/usr/bin/env python3

import os, re, subprocess
from func.print_logo import print_logo
from func.colors import green, cyan, yellow

print_logo()

print(f"Extracting {cyan('GNOME Shell Theme')}...")
os.system("./extractgst.sh")

wallpaper_filename = subprocess.check_output(
  "ls -l | grep '.jpg\|.png' | awk '{print $9}'",
  shell=True, stderr=subprocess.STDOUT).decode().rstrip()

print(f"{green(wallpaper_filename)} found in current folder.")

print(f"Copying {green(wallpaper_filename)} to theme folder...")
os.system(f"cp {wallpaper_filename} theme")


print(f"Writing {green('gnome-shell-theme.gresource.xml')} file...")

os.system(f"""echo '<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <gresource prefix="/org/gnome/shell/theme">
    <file>calendar-today.svg</file>
    <file>checkbox-focused.svg</file>
    <file>checkbox-off-focused.svg</file>
    <file>checkbox-off.svg</file>
    <file>checkbox.svg</file>
    <file>dash-placeholder.svg</file>
    <file>gnome-shell.css</file>
    <file>gnome-shell-high-contrast.css</file>
    <file>icons/message-indicator-symbolic.svg</file>
    <file>key-enter.svg</file>
    <file>key-hide.svg</file>
    <file>key-layout.svg</file>
    <file>key-shift-latched-uppercase.svg</file>
    <file>key-shift.svg</file>
    <file>key-shift-uppercase.svg</file>
    <file>noise-texture.png</file>
    <file>{wallpaper_filename}</file>
    <file>no-events.svg</file>
    <file>no-notifications.svg</file>
    <file>pad-osd.css</file>
    <file>process-working.svg</file>
    <file>toggle-off-hc.svg</file>
    <file>toggle-off-intl.svg</file>
    <file>toggle-on-hc.svg</file>
    <file>toggle-on-intl.svg</file>
  </gresource>
</gresources>' > theme/gnome-shell-theme.gresource.xml
""")


with open("theme/gnome-shell.css", "r") as file:
  filedata = file.read()

print(f'Editing {green("gnome-shell.css")} file...')
# Replace the definition of #lockDialogGroup with an empty string
new_file = re.sub(r'(?s)(#lockDialogGroup {(?<={)(.*?)(?=})})', "", filedata)

# TODO: Revemo direct reference to "wallpaper.jpg", file might have another name
new_file += """#lockDialogGroup \{
  background: #2e3436 url(%s) !important;
  background-size: cover !important;
  background-repeat: no-repeat !important;
}""" % wallpaper_filename

with open("theme/gnome-shell.css", "w") as file:
  file.write(new_file)

xrandr_output = subprocess.check_output(
    "xrandr | grep '*\| connected'",
    shell=True, stderr=subprocess.STDOUT).decode()

# xrandr_output = xrandr_output.splitlines()

# if len(xrandr_output) % 2: # output is pair, so we have both display name and resolution for each display

# for line in xrandr_output:
  
print("Processing wallpaper for setup with two displays...")
os.system(f"convert -background none \
\( {wallpaper_filename} -resize 1920x1080! \) \
\( {wallpaper_filename} -resize 1440x900! \) +append theme/wallpaper.jpg")

os.system("cd theme && glib-compile-resources gnome-shell-theme.gresource.xml")

print("Super user privileges are required to install the modified theme.\n")
os.system("sudo mv theme/gnome-shell-theme.gresource /usr/share/gnome-shell/")
print(f"\nModified theme installed. {yellow(':)')}\n")