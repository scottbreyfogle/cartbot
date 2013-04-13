#!/usr/bin/python2

import network

import sys
import cpickle
import Image
import evdev.ecodes
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

hidden_nodes = 5

################################################################################
# Handle command line args
################################################################################

if len(sys.argv) != 3:
    print("Usage: train_data.pickle neural_net.pickle")

training_file = sys.argv[1]
neural_net_file = sys.argv[2]

################################################################################
# Main
################################################################################

net = buildNetwork(sampleWidth*sampleHeight, hidden_nodes, output_nodes)
data_set = SupervisedDataSet(sampleWidth*sampleHeight, output_nodes)
training_data = pickle.load(training_file)

print("Creating data set...")

for time in training_data:
    image_file, keys = training_data[time]
    input_values = image_to_input(Image.load(image_file))
    output_values = key_to_output(keys)
    data_set.addSample(input_values, output_values)

print("Training the network...")

trainer = BackpropTrainer(net, data_set)
trainer.trainUntilConvergence(None,None,True) # We want it to be verbose

print("Saving to disk...")

pickle.dump(net,neural_net_file)

