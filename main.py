#!/usr/bin/env python3

import os, subprocess

os.system("./extractgst.sh")
os.system("cp wallpaper.* theme")

wallpaper_filename = subprocess.check_output(
  "ls -l | grep wallpaper | awk '{print $9}'",
  shell=True, stderr=subprocess.STDOUT).decode().rstrip()


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