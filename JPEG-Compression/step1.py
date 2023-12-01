from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
input_image = Image.open('images.jpg')
image_array = np.array(input_image)
def rgb_to_ycbcr(pixel):
    y= 16 + 65.738*pixel[0]/256 + 129.057*pixel[1]/256 + 25.064*pixel[2]/256
    cb = 128-37.945*pixel[0]/256 - 74.494*pixel[1]/256 + 112.439*pixel[2]/256
    cr = 128+112.439*pixel[0] - 94.154*pixel[1]/256 - 18.285*pixel[2]/256
    return y, cb, cr
ycbcr_image = np.apply_along_axis(rgb_to_ycbcr, 2, image_array)
y_channel = ycbcr_image[:, :, 0]
cb_channel = ycbcr_image[:, :, 1]
cr_channel = ycbcr_image[:, :, 2]
plt.figure(figsize=(10, 5))
plt.subplot(1, 4, 1)
plt.title("Original Image")
plt.imshow(input_image)
plt.subplot(1, 4, 2)
plt.title("Y Component")
plt.imshow(y_channel, cmap='gray')
plt.subplot(1, 4, 3)
plt.title("Cb Component")
plt.imshow(cb_channel, cmap='gray')
plt.subplot(1, 4, 4)
plt.title("Cr Component")
plt.imshow(cr_channel, cmap='gray')
print(y_channel,y_channel.shape)
print(cb_channel,cb_channel.shape)
print(cr_channel,cr_channel.shape)
plt.show()


