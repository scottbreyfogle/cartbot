from evdev import ecodes
import ImageOps
import ImageEnhance
import ImageFilter
import Image
import array
import pygame

# Output nodes
num_outputs = 7

# How far to down sample the input image
sample_width = 40
sample_height = 30

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

input_nodes = 4260
output_nodes = len(key_mapping)

def pil_to_pygame(image):
    return pygame.image.fromstring( image.convert("RGB").tostring(), image.size, "RGB")

def down_sample(image, screen):
    """Takes and image and down scales and grayscales it so that each pixel
    corresponds to one input node."""
    greyImage = ImageOps.grayscale(image)
    #image = ImageEnhance.Contrast(image).enhance(2)
    #image = ImageEnhance.Sharpness(image).enhance(1)
    smallImage = image.resize((sample_width,sample_height))#.filter(ImageFilter.FIND_EDGES)
    #mapImage = greyImage.crop((640,320,720,530)).resize((40,105))
    mapImage = ImageOps.grayscale(ImageEnhance.Contrast(image.crop((640,320,720,530))).enhance(4)).resize((20,33))

    if(screen):
        smallImageGame = pil_to_pygame(smallImage.resize((320,240)))
        screen.blit(smallImageGame,smallImageGame.get_rect())
        #mapImageGame = pil_to_pygame(mapImage.resize((160,240)))
        #mapImageGameRect = mapImageGame.get_rect()
        #mapImageGameRect.left = 160
        #screen.blit(mapImageGame,mapImageGameRect)

    #return [smallImage,mapImage]
    return [smallImage,mapImage]
    #return [image]
    #return [image.crop((0,0,2,600)), image.crop((797,0,799,600))] 

def image_to_input(image, screen):
    """Takes an image and turns it into a sequence of node input values"""
    images = down_sample(image, screen)
    result = []
    for image in images:
        for pixel in image.getdata():
            if type(pixel) == int:
                result += [float(pixel)]
            else:
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
