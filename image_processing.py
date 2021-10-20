import cv2
import numpy as np

# For anomally detect
import sys
import os
sys.path.append("./svdd_anubis/")
from PIL import Image, ImageDraw
from utils.config import Config
from deepSVDD import DeepSVDD
from datasets.preprocessing import global_contrast_normalization
import torchvision.transforms as transforms

def processImage_main(image_in):
    """!@brief Function is used to process the input image and for 
    its return to the processing queue.
    @param[image_in] Input image
    """

    # Create output image
    image_out = image_in
    
    #image_out = edge_detect(image_in)
    image_out = anomally_detect(image_in)

    return image_out
    
def edge_detect(image):
    
    # Blur the image
    image_blur = cv2.GaussianBlur(image[0], (3,3), 0)
    # Canny Edge Detection
    image[0] = cv2.Canny(image=image_blur, threshold1=100, threshold2=200)
    
    return image
    
def anomally_detect(image):
    
    model_dir_path="./svdd_anubis/model"
    load_config=os.path.join(model_dir_path,"config.json")
    load_model=os.path.join(model_dir_path,"model.tar")
    
    # Get configuration
    cfg = Config(locals().copy())
    cfg.load_config(import_json=load_config)
    
    # Data transform information
    min_max = [(-1.3942, 6.5378),
               (-1.9069, 18.5352),
               (-2.6035, 29.8313),
               (-2.3845, 12.4581)]
    trans=transforms.Compose([transforms.Resize((480,480)),
                              transforms.ToTensor(),
                              transforms.Lambda(lambda x: global_contrast_normalization(x, scale='l1')),
                              transforms.Normalize([min_max[cfg.settings['normal_class']][0]] * 3,
                                    [min_max[cfg.settings['normal_class']][1] - min_max[cfg.settings['normal_class']][0]] * 3)])    
    
    deep_SVDD = DeepSVDD(cfg.settings['objective'], cfg.settings['nu'])
    deep_SVDD.set_network(cfg.settings['net_name'])
    deep_SVDD.load_model(model_path=load_model, load_ae=False)
    
    img = np.repeat(image[0],3, axis=-1)
    im = Image.fromarray(img,'RGB')
    img = trans(im) #np.squeeze(image[0], axis=-1)
    scores = deep_SVDD.test_image(img, cfg.settings['device'])
         
    #print(scores)
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0,0), im.size], outline='#ffffff' if scores[0]> 1000 else '#000000', width=10) #'#ff0000' if scores[0]> 1 else '#00ff00'
    
    image[0] = np.array(im.convert('L'))
    return image
