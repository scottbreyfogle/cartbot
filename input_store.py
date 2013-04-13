from evdev import InputDevice, categorize, ecodes
from re import search
from time import time
import os
import Image

dev = InputDevice('/dev/input/event4')

events = {} #A set that will contain all keys currently being held down

def read_input():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            (key,state) = search(".+\(KEY_(\w+)\), (up|down|hold)",str(categorize(event))).groups()
            if state == 'down':
                if key not in events:
                    events.add(key) #Adds a pressed key to events
            else if state == 'up':
                if key in events:
                    events.remove(key) #Removes a released key from events
 
def store():
    input_dict = {}
    previous_time = time.time()
    current_time = 0
    while True:
        current_time = time.time() - previous_time
        os.system("scrot -u %ds.png" % current_time)
        current_img = Image.open("%ds.png" % current_time)
        input_dict[(current_img,events)] = current_time
        time.sleep(0.1)
