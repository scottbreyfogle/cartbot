#!/usr/bin/env python2
from argparse import ArgumentParser
from threading import Thread, Event
from functools import partial
from time import sleep
import pickle

from record import record
from predict import predict
from network import Network,downsample_transform

if __name__ == '__main__':
    parser = ArgumentParser(description="Neural Network for playing simple video games")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-r", "--record", help="Record a game session to train the neural net", metavar=("json_save_file", "image_subdirectory"), nargs=2)
    action.add_argument("-t", "--train", help="Train a neural net", metavar=("neural_net_save_file", "training_files"), nargs="+")
    action.add_argument("-p", "--predict", help="Have the neural net predict and emulate user input", metavar="neural_net_save_file", nargs=1)
    
    args = parser.parse_args()
    if args.record:
        record(*args.record)
    elif args.train:
        n = Network(partial(downsample_transform, 20, 20), 3*20*20)
        n.train(args.train[1:])
        n.save(args.train[0])
    elif args.predict:
        with open(args.predict[0]) as f:
            network = pickle.load(f) 
            stop = Event()
            t = Thread(target=predict, args=(network,stop))
            t.start()
            
            try:
                print("Cartbot is injecting user input. Ctrl-c to stop")
                while True:
                    sleep(.1)
            except KeyboardInterrupt: # Make all the threads exit
                stop.set()
            t.join()
