import click
import torch
import logging
import random
import os
import numpy as np
from PIL import Image, ImageDraw

from utils.config import Config
from deepSVDD import DeepSVDD
from datasets.preprocessing import global_contrast_normalization
import torchvision.transforms as transforms

################################################################################
# Settings
################################################################################
@click.command()
@click.argument('model_dir_path', type=click.Path(exists=True))
@click.argument('image_path', type=click.Path(exists=True))

################################################################################
# main
################################################################################
def main(model_dir_path,image_path):

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
    
    with Image.open(image_path) as im:
         image = trans(im)
         scores = deep_SVDD.test_image(image, cfg.settings['device'])
         
         print(scores)
         draw = ImageDraw.Draw(im)
         draw.rectangle([(0,0), im.size], outline='#ff0000' if scores[0]> 1 else '#00ff00', width=10)
         im.show()
         
if __name__ == '__main__':
    main()
