#!/usr/bin/python2

import network

import sys
from cPickle import (dump,load)
import Image
import evdev.ecodes
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

################################################################################
# Handle command line args
################################################################################

if len(sys.argv) < 3:
    print("Usage: train_data.pickle neural_net.pickle [hidden_nodes]")
    exit(1)

training_file = open(sys.argv[1], "r")
neural_net_file = open(sys.argv[2], "w")
hidden_nodes = 5
if len(sys.argv) > 3 and int(sys.argv[3]) > 0:
    hidden_nodes =  int(sys.argv[3])

################################################################################
# Main
################################################################################

net = buildNetwork(network.input_nodes, hidden_nodes, network.output_nodes)
data_set = SupervisedDataSet(network.input_nodes, network.output_nodes)
training_data = load(training_file)
training_file.close()

print("Creating data set...")

for time in training_data:
    image_file, keys = training_data[time]
    input_values = network.image_to_input(Image.load(image_file))
    output_values = network.key_to_output(keys)
    data_set.addSample(input_values, output_values)

print("Training the network...")

trainer = BackpropTrainer(net, data_set)
trainer.trainUntilConvergence(None,None,True) # We want it to be verbose

print("Saving to disk...")

dump(net,neural_net_file)

