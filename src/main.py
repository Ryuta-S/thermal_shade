import numpy as np
import cv2
import sys, os
from PIL import Image
import utils.tiff_utils as tu
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

image_path = os.path.join('data', '0001_0829/0000.tiff')
image = tu.open_multipage_tiff(image_path)

img = image[:,:,388]

cv2.imwrite(os.path.join('data', '0001_0829/3ch.tiff'),tu.convert_1ch_to_3ch(img))