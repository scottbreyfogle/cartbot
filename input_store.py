#!/usr/bin/env python2
from evdev import InputDevice, categorize, ecodes
from re import search
from time import time, sleep
import thread
import pickle
import os
import sys
import Image
import json

dev = InputDevice('/dev/input/event4')

events = set([]) #A set that will contain all keys currently being held down

def read_input():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            (key,state) = event.code, event.value
            if state == 1: #Key is pressed down
                if key not in events:
                    events.add(key) #Adds a pressed key to events
            elif state == 0: #Key is released
                if key in events:
                    events.remove(key) #Removes a released key from events
 
def store(filename):
    thread.start_new_thread(read_input, ())
    input_dict = {}
    previous_time = time()
    current_time = 0
    #try:
    while (time() - previous_time) < 5:
        current_time = time() - previous_time
        os.system("scrot -u %ds.png" % current_time)
        #current_img = Image.open("%ds.png" % current_time)
        input_dict[current_time] = ("%ds.png" % current_time,list(events))
        sleep(0.1)
    #except KeyboardInterrupt:
    f = open(filename,"w")
    json.dump(input_dict,f)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        store(sys.argv[1])
    else:
        print "Usage: ./input_store.py file"
