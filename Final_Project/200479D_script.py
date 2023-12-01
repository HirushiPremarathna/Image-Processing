import numpy as np
from PIL import Image

def convert_to_grayscale(image_path):

    # Load the image
    image = Image.open(image_path)

    # Convert the image to RGB mode if it is not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get the image data as a NumPy array
    image_data = np.array(image)

    # Convert the RGB values to grayscale using the luminosity method
    grayscale_image = np.dot(image_data[:, :, :3], [0.299, 0.587, 0.114])

    # Convert the grayscale image to 8-bit format and clip the values to [0, 255]
    grayscale_image = np.uint8(np.clip(grayscale_image, 0, 255))

    return grayscale_image

# Convert the sample image to grayscale
grayscale_image = convert_to_grayscale('/content/SampleImage.png')

# Save the grayscale image as a new PNG file
Image.fromarray(grayscale_image).save('/content/grayscale_image.png')
