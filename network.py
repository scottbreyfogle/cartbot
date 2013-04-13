from evdev import ecodes
import Image

# Output nodes
num_outputs = 7

# How far to down sample the input image
sampleWidth = 32
sampleHeight = 24

def down_sample(img):
    img.thumbnail((sampleWidth,sampleHeight), Image.ANTIALIAS)
    return img

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


def net_to_key(weights):
    return [net_mapping[w] for w in weights if w > .5]

def key_to_output(key):
    return key_mapping[key]
