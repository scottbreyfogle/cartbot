from collections import Counter
from functools import partial
import sys
import json

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from evdev import ecodes
import ImageOps
import ImageEnhance
import ImageFilter
import Image
import array

class Network:
    def __init__(self, image_transform, input_nodes, hidden_nodes=5, output_nodes=None):
        self.input_transform = image_transform
        self.output_nodes = output_nodes
        self.hidden_nodes = hidden_nodes
        self.input_nodes = input_nodes

    def train(self, files, min_delta = .0001, max_iterations=20):
        event_counter = Counter()
        
        for file in files:
            print("Counting events in {}".format(file))
            with open(file ,'r') as train_file:
                training_data = json.load(train_file)

            for (time, (image_file, events)) in training_data.items():
                for (code, value) in events:
                    event_counter[code] += 1

        if self.output_nodes == None:
            self.output_nodes = self.determine_output_nodes(event_counter)
        self.event_codes = [t[0] for t in event_counter.most_common(self.output_nodes)]

        self.net = buildNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        data_set = SupervisedDataSet(self.input_nodes, self.output_nodes)

        for file in files:
            print("Adding training data from {} to dataset".format(file))
            with open(file,'r') as train_file:
                training_data = json.load(train_file)

            for (time, (image_file, events)) in training_data.items():
                input_values = self.input_transform(image_file)
                output_values = self.output_transform(events)
                data_set.addSample(input_values, output_values)

        print("Training the network...")

        last_error = min_delta + 1
        trainer = BackpropTrainer(self.net, data_set)
        if not min_delta and not max_iterations: # Max iterations and min delta are 0 or None
            trainer.trainUntilConvergence()
            print("Neural net trained until convergence")
        elif not max_iterations:
            while last_error > min_delta:
                error = trainer.train()
                print("\t{}".format(error))
            print("Reached target min_delta")
        else:
            for i in xrange(max_iterations):
                error = trainer.train()
                print("\t{}".format(error))
                if min_delta and abs(last_error - error) <= min_delta:
                    print("Reached target min_delta")
                    break
                last_error = error
            else: # Happens when there was no break
                print("Completed max iterations")

    def determine_output_nodes(self, event_counter, min_difference_factor=.1):
        common = event_counter.most_common()

        last_count = common[0][1]
        for (i, (key, count)) in enumerate(common[0:]):
            if count < last_count * min_difference_factor:
                return i
        return len(event_counter)

    def output_transform(self, events):
        events = dict(events)
        output_array = array.array('d')
        output_array.fromlist([events[code] for code in self.event_codes])
        return output_array

def downsample_transform(width, height, image):
    '''Simple image transform that returns a downsampled version of the image'''
    image = Image.open(image).resize((width, height))

    result = []
    for pixel in image.getdata():
        for val in pixel:
            result.append(val)

    output_array = array.array('d')
    output_array.fromlist(result)
    return output_array

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        n = Network(partial(downsample_transform, 20, 20), 3*20*20)
        n.train(sys.argv[1:])
    else:
        print "Usage: ./network.py training_file.json..."
