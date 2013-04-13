import ImageOps
import Image

# How far to down sample the input image
sampleWidth = 32
sampleHeight = 24

def down_sample(image):
    """Takes and image and down scales and grayscales it so that each pixel
    corresponds to one input node."""
    return ImageOps.grayscale(image.thumbnail((sampleWidth,sampleHeight), Image.ANTIALIAS))

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
        output[key_to_output(key)] = 1
    return tuple(output)
