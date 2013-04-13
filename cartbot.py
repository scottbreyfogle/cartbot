#!/usr/bin/env python2
import time
import sys
import pickle
from subprocess import Popen
from window import get_active_window
from network import net_to_keys,image_to_input, net_mapping
from evdev import uinput, ecodes

def run(network):
    running = True
    ui = uinput.UInput()
    while running:
        vals = network.activate(image_to_input(get_active_window()))
        for (index, weight) in enumerate(vals):
            if weight > .5:
                ui.write(ecodes.EV_KEY, net_mapping[index], 1)
#                if(net_mapping[index] == ecodes.KEY_LEFT or net_mapping[index] == ecodes.KEY_RIGHT):
#                    ui.write(ecodes.EV_KEY, net_mapping[index], 0)
                ui.syn()

            else:
                #print("POPPING: " + str(net_mapping[index]))
                ui.write(ecodes.EV_KEY, net_mapping[index], 0)
                #ui.write(ecodes.EV_KEY, ecodes.KEY_ENTER, 0)
                ui.syn()

        time.sleep(.01)
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 0)
        ui.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        network = pickle.load(open(sys.argv[1],"r")) 
        run(network)
    else:
        print "Usage: ./cartbot.py neural-net-file"
