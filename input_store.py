#!/usr/bin/env python2
from evdev import InputDevice, categorize, ecodes
from re import search
from datetime import datetime
import thread
import pickle
import time
import os
import sys
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
            elif state == 'up':
                if key in events:
                    events.remove(key) #Removes a released key from events
 
def store(filename):
    thread.start_new_thread(read_input, ())
    input_dict = {}
    previous_time = datetime.now()
    current_time = 0
    try:
        while True:
            current_time = datetime.now() - previous_time
            os.system("scrot -u %(current_time)s.png", current_time)
            current_img = Image.open("%(current_time)s.png", current_time)
            input_dict[(current_img,events)] = current_time
            time.sleep(0.1)
    except KeyboardInterrupt:
        json.dump(f, input_dict)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        store(sys.argv[1])
    else:
        print "Usage: ./input_store.py file"
