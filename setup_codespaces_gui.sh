#!/bin/bash

echo "Updating..."
sudo apt update

echo "Installing packages..."

sudo apt-get install libgl1-mesa-glx libgles2-mesa libegl1-mesa libmtdev1
sudo apt install xterm fluxbox novnc tigervnc-standalone-server

python -m pip install "kivy[full]" kivy_examples

# echo "Starting NoVNC"

# websockify --web /usr/share/novnc/ --wrap-mode=ignore 6080 localhost:5900 &

# echo "Starting VNC server..."

# vncserver :1 -geometry 2560x1440 -depth 24 -localhost -nolisten tcp -rfbport 5900

# echo "Done! Port 6080 and 5900 should now be forwarded. Simply open https://localhost:6080 to access the NoVNC client."