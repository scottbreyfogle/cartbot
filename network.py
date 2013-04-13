from evdev import ecodes
import ImageOps
import ImageEnhance
import Image
import array

# Output nodes
num_outputs = 7

# How far to down sample the input image
sample_width = 256
sample_height = 12

key_mapping = {
        ecodes.KEY_UP: 0,
        ecodes.KEY_DOWN: 1,
        ecodes.KEY_LEFT: 2,
        ecodes.KEY_RIGHT: 3,
        ecodes.KEY_LEFTSHIFT: 4,
        ecodes.KEY_Z: 5,
        ecodes.KEY_C: 6
}
net_mapping = [ecodes.KEY_UP, ecodes.KEY_DOWN, ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_LEFTSHIFT, ecodes.KEY_Z, ecodes.KEY_C]

input_nodes = sample_width*sample_height*3
output_nodes = len(key_mapping)


def down_sample(image):
    """Takes and image and down scales and grayscales it so that each pixel
    corresponds to one input node."""
    image = ImageEnhance.Contrast(image).enhance(2)
    image = ImageEnhance.Sharpness(image).enhance(2)
    image = image.resize((sample_width,sample_height))
    #image = ImageOps.grayscale(image)
    return image

def image_to_input(image):
    """Takes an image and turns it into a sequence of node input values"""
    image = down_sample(image)
    result = []
    for pixel in image.getdata():
        for p in pixel:
            result += [float(p)]
    output_array = array.array('d')
    output_array.fromlist(result)
    return output_array

def keys_to_output(keys):
    """Takes a list of keys and returns a tuple which corresponds to output
    of the neural net"""
    output = [0 for i in xrange(output_nodes)]
    for key in keys:
        if key in key_mapping:
            output[key_mapping[key]] = 1
    #return array.fromlist(output)
    output_array = array.array('d')
    output_array.fromlist(output)
    return output_array

def net_to_keys(weights):
    return [net_mapping[w] for w in xrange(len(weights)) if weights[w] > .5]
