import cv2
import numpy as np
import time
# For anomally detect
import sys
import os
sys.path.append("./svdd_anubis/")
from PIL import Image, ImageDraw
from svdd_anubis.deepSVDD import DeepSVDD
from svdd_anubis.utils.config import Config
from svdd_anubis.datasets.preprocessing import global_contrast_normalization
import torchvision.transforms as transforms
import torch



class Image_processing():
    def __init__(self):
        self.trans = None
        self.deep_SVDD = None
        self.dev = None
        self.score_threshold = 1000

    def setup_image_process(self, model_dir_path):
        load_config=os.path.join(model_dir_path,"config.json")
        load_model=os.path.join(model_dir_path,"model.tar")

        useCUDA = torch.cuda.is_available()

        if useCUDA:
            self.dev = torch.device('cuda')
        else:
            self.dev = torch.device('cpu')
        
        # Get configuration
        cfg = Config(locals().copy())
        cfg.load_config(import_json=load_config)
        
        # Data transform information
        min_max = [(-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597)]
        trans=[transforms.Resize((cfg.settings['net_res'],cfg.settings['net_res'])),#160,120
               transforms.ToTensor(),
               transforms.Lambda(lambda x: global_contrast_normalization(x, scale='l1')),#, ]
               transforms.Normalize([min_max[cfg.settings['normal_class']][0]] * 3,
                                    [min_max[cfg.settings['normal_class']][1] - min_max[cfg.settings['normal_class']][0]] * 3)]
        self.trans = transforms.Compose(trans)

        self.deep_SVDD = DeepSVDD(cfg.settings['objective'], cfg.settings['nu'])
        self.deep_SVDD.set_network(cfg.settings['net_name'], cfg.settings['net_res'], cfg.settings['net_rep_dim'])
        self.deep_SVDD.load_model(model_path=load_model, load_ae=False, map_location = self.dev)

    def change_threshold(self, threshold):
        self.score_threshold = threshold

    def processImage_main(self, image_in):
        """!@brief Function is used to process the input image and for 
        its return to the processing queue.
        @param[image_in] Input image
        """

        # Create output image
        image_out = image_in
        
        #image_out = edge_detect(image_in)
        image_out, scores = self.anomally_detect(image_in)

        return image_out, scores[0]
        
    def edge_detect(self, image):
        
        # Blur the image
        image_blur = cv2.GaussianBlur(image[0], (3,3), 0)
        # Canny Edge Detection
        image[0] = cv2.Canny(image=image_blur, threshold1=100, threshold2=200)
        
        return image


    def anomally_detect(self, image):        
        #img = np.repeat(image[0],3, axis=-1)
        
        if "BGR" in image[1]:
            img_test = cv2.cvtColor(image[0], cv2.COLOR_BGR2RGB)
        else:
            img_test = image[0]

        im = Image.fromarray(img_test,'RGB')
        im_draw = Image.fromarray(image[0],'RGB')
        img = self.trans(im) #np.squeeze(image[0], axis=-1)
        scores = self.deep_SVDD.test_image(img, self.dev)
        
        draw = ImageDraw.Draw(im_draw)
        draw.rectangle([(0,0), im_draw.size], outline='#0000ff' if scores[0]> self.score_threshold else '#00ff00', width=10) #'#ff0000' if scores[0]> 1 else '#00ff00'
        
        image[0] = np.array(im_draw)
        return image, scores
