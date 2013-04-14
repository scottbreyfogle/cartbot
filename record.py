#!/usr/bin/env python2
from time import time, sleep
from threading import Thread, Event
from subprocess import check_call
import os.path
import sys
import re
import json

from evdev import InputDevice, ecodes, list_devices

input_dict = {}
events = set([]) # A set that will contain all keys currently being held down
complete = Event()
running = Event()
running.set()
started = Event()

def stop_threads():
    started.set() 
    running.set()
    complete.set()

def read_input(dev):
    while not complete.is_set():
        for event in dev.read():
            if event.type == ecodes.EV_KEY: # Key press
                (key,state) = event.code, event.value
                if state == 1: # Key is pressed down
                    events.add((key, 1))
                elif state == 0: # Key is released
                    events.discard((key, 1))
                    if key == ecodes.KEY_F9: # Start
                        print("Recording started.")
                        started.set()
                    elif key == ecodes.KEY_F10: # Pause
                        print("Recording paused.")
                        running.clear()
                    elif key == ecodes.KEY_F11: # Unpause
                        print("Recording resumed.")
                        running.set()
                    elif key == ecodes.KEY_F12: # Stop
                        print("Recording stopped. exiting.")
                        stop_threads()
            if event.type == ecodes.EV_ABS: # Absolute event, gamepad analog stick
                events.add((event.code, event.value))
 
def store(json_file, image_dir, sleep_duration=.1):
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    
    started.wait()
    while not complete.is_set():
        current_time = time()
        img_file = "{}/{:.4f}.png".format(image_dir, current_time) 
        check_call(["./scrot", "-u", img_file])
        input_dict[current_time] = (img_file,list(events))
        sleep(sleep_duration)
        running.wait()

    with open(json_file, 'w') as f:
        json.dump(input_dict, f)

def main():
    print("Press F9 to start recording")
    threads = []
    
    for dev in map(InputDevice, list_devices()):
        if re.search("razer|x-?box", dev.name, flags=re.IGNORECASE):
            print "Redording events on {} ({})".format(dev.name, dev.fn)
            recorder = Thread(target=read_input, args=(dev,))
            recorder.start()
            threads.append(recorder)

    store_thread = Thread(target=store, args=(sys.argv[1], sys.argv[2]))
    store_thread.start()
    threads.append(store_thread)

    # Wait and kill on ctrl-c if it comes
    try:
        while 1:
            if complete.is_set():
                return
            sleep(.1)
    except KeyboardInterrupt: # Make all the threads exit
        stop_threads()

    # Join all children
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main()
    else:
        print "Usage: ./input_store.py training_file.json image_directory"
