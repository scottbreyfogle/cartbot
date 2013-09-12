#!/usr/bin/env python2
from time import time, sleep
from threading import Thread, Event
from subprocess import check_call
import os.path
import sys
import re
import json

from evdev import InputDevice, ecodes, list_devices

class Recorder:
    def __init__(self, json_file, image_dir, sleep_duration=.1):
        self.json_file = json_file
        self.image_dir = image_dir
        self.sleep_duration = sleep_duration

        self.threads = []
        self.input_dict = {}
        self.events = set([]) # A set that will contain all keys currently being held down
        self.complete = Event()
        self.started = Event()
        self.running = Event()

    def stop_threads(self):
        self.started.set() 
        self.running.set()
        self.complete.set()

    def process_key(self, state, key):
        if state == 1: # Key is pressed down
            self.events.add(((ecodes.EV_KEY, key), 1))
        elif state == 0: # Key is released
            self.events.discard(((ecodes.EV_KEY, key), 1))
            if key == ecodes.KEY_F9: # Start
                print("Recording started.")
                self.started.set()
            elif key == ecodes.KEY_F10: # Pause
                print("Recording paused.")
                self.running.clear()
            elif key == ecodes.KEY_F11: # Unpause
                print("Recording resumed.")
                self.running.set()
            elif key == ecodes.KEY_F12: # Stop
                print("Recording stopped. exiting.")
                self.stop_threads()

    def process_abs(self, event):
        self.events.add(((event.type, event.code), event.value))

    def read_input(self, dev):
        while not self.complete.is_set():
            for event in dev.read():
                if event.type == ecodes.EV_KEY: # Key press
                    self.process_key(event.code, event.value)
                if event.type == ecodes.EV_ABS: # Absolute event, gamepad analog stick
                    self.process_abs(event)
     
    def save_image(self):
        current_time = time()
        img_file = "{}/{:.4f}.png".format(self.image_dir, current_time) 
        check_call(["./scrot", "-u", img_file])
        return img_file

    def store(self):
        self.running.set()
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        
        started.wait()
        while not self.complete.is_set():
            img_file = self.record_image()
            self.input_dict[current_time] = (img_file, list(self.events))
            sleep(self.sleep_duration)
            self.running.wait()

        with open(json_file, 'w') as f:
            json.dump(input_dict, f)

    def await_keyboard_interrupt(self):
        try:
            while True:
                if complete.is_set():
                    return
                sleep(.1)
        except KeyboardInterrupt: # Make all the threads exit
            return

    def record(self):
        for dev in map(InputDevice, list_devices()):
            if re.search("razer|x-?box", dev.name, flags=re.IGNORECASE): # TODO: better input device filtering
                print("Recording events on {} ({})".format(dev.name, dev.fn))
                recorder = Thread(target=read_input, args=(dev,))
                recorder.start()
                self.threads.append(recorder)
        print("Press F9 to start recording")

        store_thread = Thread(target=self.store)
        store_thread.start()
        self.threads.append(store_thread)

        # Wait and kill on ctrl-c if it comes
        self.await_keyboard_interrupt()
        self.stop_threads()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        r = Recorder(sys.argv[1], sys.argv[2])
        r.record()
    else:
        print("Usage: ./input_store.py training_file.json image_directory")
