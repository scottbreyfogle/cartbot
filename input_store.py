from evdev import InputDevice, categorize, ecodes
from re import search
from datetime import datetime
import time
import os
import Image

dev = InputDevice('/dev/input/event4')

events = {} #A set that will contain all keys currently being held down

def read_input():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            (key,state) = search(".+\(KEY_(\w+)\), (up|down)",str(event)).groups()
            if state == 'down':
                if key not in events:
                    events.add(key) #Adds a pressed key to events
            else:
                if key in events:
 
def store():
    input_dict = {}
    previous_time = datetime.now()
    current_time = 0
    while True:
        current_time = datetime.now() - previous_time
        os.system("scrot -u %(current_time)s.png", current_time)
        current_img = Image.open("%(current_time)s.png", current_time)
        input_dict[(current_img,events)] = current_time
        time.sleep(0.1)
