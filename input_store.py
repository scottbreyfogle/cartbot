from evdev import InputDevice, categorize, ecodes
from re import search
import time
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
    current_time = 0
    while True:
        os.system("scrot -u %(current_time)s.png", current_time)
        current_img = Image.open("%(current_time)s.png", current_time)
        input_dict[(current_img,REPLACE_ME_WITH_NAME_OF_SET)] = current_time #replace REPLACE_ME-WITH_NAME_OF_SET with the name of the set of keyboard actions
        current_time += 0.5
        time.sleep(0.5)
