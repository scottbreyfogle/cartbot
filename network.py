import Image

# How far to down sample the input image
sampleWidth = 32
sampleHeight = 24

def down_sample(img):
    img.thumbnail((sampleWidth,sampleHeight), Image.ANTIALIAS)
    return img
