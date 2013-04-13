import os
import Image

def get_active_window():
    os.system("./scrot -u /tmp/vision.png")
    return Image.open("/tmp/vision.png")
