#!/usr/bin/python2

import network

import sys
import json
import pickle
import Image
import evdev.ecodes
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

################################################################################
# Handle command line args
################################################################################

if len(sys.argv) < 4:
    print("Usage: hidden_nodes neural_net.pickle train_data.json[+]")
    exit(1)

neural_net_file = open(sys.argv[2], "w")
hidden_nodes = int(sys.argv[1])

################################################################################
# Main
################################################################################

net = buildNetwork(network.input_nodes, hidden_nodes, network.output_nodes)
data_set = SupervisedDataSet(network.input_nodes, network.output_nodes)

print("Creating data set...")

for train_file in sys.argv[3:]:
    train_file = open(train_file,'r')
    training_data = json.load(train_file)
    train_file.close()
    for time in training_data:
        image_file, keys = training_data[time]
        input_values = network.image_to_input(Image.open(image_file))
        output_values = network.keys_to_output(keys)
        data_set.addSample(input_values, output_values)

print(len(data_set))

print("Training the network...")

trainer = BackpropTrainer(net, data_set)
#trainer.trainUntilConvergence() # We want it to be verbose
for i in xrange(250):
    print("\t" + str(trainer.train()))

print("Saving to disk...")

pickle.dump(net,neural_net_file)

