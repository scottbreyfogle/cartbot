import os
import Image

def getActiveWindow():
    os.system("scrot -u /tmp/vision.png")
    return Image.open("/tmp/vision.png")
