from evdev import ecodes
import ImageOps
import Image

# Output nodes
num_outputs = 7

# How far to down sample the input image
sample_width = 32
sample_height = 24

input_nodes = sample_width*sample_height
output_nodes = 10

key_mapping = {
        ecodes.KEY_UP: 0,
        ecodes.KEY_DOWN: 1,
        ecodes.KEY_LEFT: 2,
        ecodes.KEY.RIGHT: 3,
        ecodes.KEY_LSHIFT: 4,
        ecodes.KEY_Z: 5,
        ecodes.KEY_C: 6
}
net_mapping = [ecodes.KEY_UP, ecodes.KEY_DOWN, ecodes.KEY_LEFT, ecodes.KEY.RIGHT, ecodes.KEY_LSHIFT, ecodes.KEY_Z, ecodes.KEY_C]


def down_sample(img):
    img.thumbnail((sampleWidth,sampleHeight), Image.ANTIALIAS)
    return img
def down_sample(image):
    """Takes and image and down scales and grayscales it so that each pixel
    corresponds to one input node."""
    return ImageOps.grayscale(image.thumbnail((sample_width,sample_height), Image.ANTIALIAS))

def image_to_input(image):
    """Takes an image and turns it into a sequence of node input values"""
    image = down_sample(image)
    result = (0,)[1:]
    for pixel in img.get_data():
        result += (pixel,)
    return result

def keys_to_output(keys):
    """Takes a list of keys and returns a tuple which corresponds to output
    of the neural net"""
    output = [0 for i in xrange(output_nodes)]
    for key in keys:
        output[key_mapping[key]] = 1
    return tuple(output)

def net_to_key(weights):
    return [net_mapping[w] for w in weights if w > .5]
