from collections import Counter
from subprocess import check_call
import json
import pickle
import array

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import Image

class Network:
    def __init__(self, image_transform, input_nodes, hidden_nodes=5, output_nodes=None, temp_file="/tmp/screen.png"):
        self.input_transform = image_transform
        self.output_nodes = output_nodes
        self.hidden_nodes = hidden_nodes
        self.input_nodes = input_nodes
        self.temp_file = temp_file

    def train(self, files, min_delta = .0001, max_iterations=20):
        event_counter = Counter()
        
        for file in files:
            print("Counting events in {}".format(file))
            with open(file ,'r') as train_file:
                training_data = json.load(train_file)

            for (time, (image_file, events)) in training_data.items():
                for (code, value) in events:
                    event_counter[tuple(code)] += 1

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
        events = {tuple(x[0]): x[1] for x in events}
        output_list = [] 
        for code in self.event_codes:
            if code in events:
                output_list.append(events[code])
            else:
                output_list.append(0)
        output_array = array.array('d')
        output_array.fromlist(output_list)
        return output_array

    def predict(self):
        check_call(["./scrot", "-u", self.temp_file])
        input = self.input_transform(self.temp_file)
        
        weights = self.net.activate(input)
        return weights

    def save(self, file):
        with open(file, 'w') as f:
            pickle.dump(self, f)

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
