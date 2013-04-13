#!/usr/bin/env python2
from evdev import InputDevice, categorize, ecodes, list_devices
from re import search
from time import time, sleep
from threading import Thread
from subprocess import Popen
import pickle
import os
import sys
import Image
import json

input_dict = {}
events = set([]) #A set that will contain all keys currently being held down
global running
running = True
global threads
threads = []

def read_input():
    dev = None
    for dev in map(InputDevice, list_devices()):
        if dev.name.lower().find('keyboard') > 0:
            break
    print dev.name
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            (key,state) = event.code, event.value
            if state == 1: #Key is pressed down
                if key not in events:
                    events.add(key) #Adds a pressed key to events
            elif state == 0: #Key is released
                if key in events:
                    events.remove(key) #Removes a released key from events
        if not running:
            break
 
def store(image_dir):
    previous_time = time()
    current_time = 0
    while running:
        current_time = time() - previous_time
        img_file = "%s/%.4fs.png" % (image_dir,current_time) 
        fail = os.system("scrot -u {}".format(img_file))
        if fail:
            break
        print(result)
        input_dict[current_time] = (img_file,list(events))
        sleep(.1)

def main():
    thread = Thread(target=read_input)
    thread.start()
    threads.append(thread)

    emulator = Popen(["mupen64plus", "roms/Mario Kart 64 (USA).n64"])

    while ecodes.KEY_LEFTSHIFT not in events:
        sleep(.01)
    
    thread = Thread(target=store, args=(sys.argv[2],))
    thread.start()
    threads.append(thread)

    while True:
        if emulator.poll() == None:
            sleep(.1)
        else:
            return

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            emulator = main()
        except:
            running = False
            for thread in threads:
                "Joining.."
                thread.join()
            f = open(sys.argv[1], "w")
            json.dump(input_dict,f)
            raise
        else:
            running = False
            for thread in threads:
                "Joining.."
                thread.join()
            f = open(sys.argv[1], "w")
            json.dump(input_dict,f)

    else:
        print "Usage: ./input_store.py training_file.json image_directory"
