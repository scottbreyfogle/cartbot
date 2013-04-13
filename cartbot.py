#!/usr/bin/env python2
import time
import sys
from network import net_to_keys,image_to_input
from evdev import uinput, EV_KEY

def run(network):
    running = True
    while running:
        vals = network.activate(image_to_input())
        for (index, weight) in enumerate(vals):
            if weight > .5:
                ui.write(EV_KEY, net_mapping[index], 1)
            else:
                ui.write(EV_KEY, net_mapping[index], 0)
        time.sleep(.1)

if __name__ == '__name__':
    if len(sys.argv) == 2:
        network = pickle.load() 
        run(network)
    else:
        print "Usage: ./cartbot.py neural-net-file"
