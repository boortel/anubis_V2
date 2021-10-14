import cv2
import numpy as np

def processImage_main(image_in):
    # Create output image
    image_out = image_in

    # Blur the image
    image_blur = cv2.GaussianBlur(image_in[0], (3,3), 0)
    # Canny Edge Detection
    image_out[0] = cv2.Canny(image=image_blur, threshold1=100, threshold2=200)

    return image_out