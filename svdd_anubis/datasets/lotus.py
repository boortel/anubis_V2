#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:02:48 2022

@author: kratochvila
"""
from PIL import Image
import os
import os.path
import json
import sys
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle
import torch.utils.data as data
from torchvision.datasets.utils import check_integrity

from base.torchvision_dataset import TorchvisionDataset
from .preprocessing import get_target_label_idx, global_contrast_normalization
import torchvision.transforms as transforms
from torch.utils.data import Subset

import numpy as np
import torch

class LOTUS_Dataset(TorchvisionDataset):

    def __init__(self, root: str, normal_class: int, version: str="both", res: int = 32,
                 validation: bool = False, autoaugment: bool = False):
        super().__init__(root)

        self.n_classes = 9 # 0: normal, 1: outlier
        self.normal_classes = tuple([normal_class])
        self.outlier_classes = list(range(1, 9))
        self.outlier_classes.remove(normal_class)

        # Pre-computed min and max values (after applying GCN) from train data per class
        min_max = [(-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597),
                   (-1.6091, 10.7597)]
        
        # For 1225 Industry biscuits base for one class
        
        # dataset=load_dataset_imgs()
        # test=list(dataset.test_set)
        # train=list(dataset.train_set)
        # s=[x[0] for x in train if x[1]==1]
        # n=[s.append(x[0]) for x in test if x[1]==1]
        # ma=max([torch.max(torch.concat(x)) for x in s])
        # mi=min([torch.min(torch.concat(x)) for x in s])

        # CIFAR-10 preprocessing: GCN (with L1 norm) and min-max feature scaling to [0,1]
        trans=[transforms.Resize((res,res)),#160,120
               transforms.ToTensor(),
               transforms.Lambda(lambda x: global_contrast_normalization(x, scale='l1')),#, ]
               transforms.Normalize([min_max[normal_class][0]] * 3,
                                    [min_max[normal_class][1] - min_max[normal_class][0]] * 3)]
        trans=trans[1:] if res == 0 else trans
        transform = transforms.Compose(trans)

        target_transform = transforms.Lambda(lambda x: int(x in self.outlier_classes))

        train_set = LOTUS(root=self.root, train=True, version=version,
                              transform=transform, target_transform=target_transform)
        # Subset train set to normal class
        train_idx_normal = get_target_label_idx(train_set.train_labels, self.normal_classes)
        self.train_set = Subset(train_set, train_idx_normal)

        self.test_set = LOTUS(root=self.root, train=False, version=version,
                                  transform=transform, target_transform=target_transform)
        if validation:
            self.validation_set = LOTUS(root=self.root, train=False, version=version,
                                         transform=transform, target_transform=target_transform,validation=True)
 
class LOTUS(data.Dataset):
    """`MyData Dataset.

    Args:
        root (string): Root directory of dataset where directory
            ``mydata-batches-py`` exists or will be saved to if download is set to True.
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        version (int, optional): Version of dataset, Possible ``100`` or ``300``, default 100.

    """
    base_folder_list = ['lotus-batches-py']#'300-batches-py'
    version_list = ["top","side","both"]
    base_folder = None
    train_list = None
    test_list = None

    def __init__(self, root, train=True, version="both",
                 transform=None, target_transform=None, validation=False):
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set
        
        self._load_hashes(version)

        if not self._check_integrity():
            raise RuntimeError('Dataset not found or corrupted.' +
                               ' You can use download=True to download it')

        # now load the picked numpy arrays
        if self.train:
            # self.train_data = []
            # self.train_labels = []
            for fentry in self.train_list:
                f = fentry[0]
                file = os.path.join(self.root, self.base_folder, f)
                fo = open(file, 'rb')
                if sys.version_info[0] == 2:
                    entry = pickle.load(fo)
                else:
                    entry = pickle.load(fo, encoding='latin1')
                # self.train_data.append(entry['data'])
                # if 'labels' in entry:
                #     self.train_labels.append(entry['labels'])
                # else:
                #     self.train_labels.append(entry['fine_labels'])
                fo.close()
                self.train_data = entry['data']
                self.train_labels = entry['labels']
            # self.train_data = np.concatenate(self.train_data)
            # self.train_data = self.train_data.reshape((100, 640, 480, 3))
        else:
            f = self.test_list[0][0]
            file = os.path.join(self.root, self.base_folder, f)
            fo = open(file, 'rb')
            if sys.version_info[0] == 2:
                entry = pickle.load(fo)
            else:
                entry = pickle.load(fo, encoding='latin1')
            self.test_data = entry['data']
            if 'labels' in entry:
                self.test_labels = entry['labels']
            else:
                self.test_labels = entry['fine_labels']
            fo.close()
            if validation:
                self.test_data = np.concatenate((self.test_data[self.test_labels == 1][:10],
                self.test_data[self.test_labels == 2][:],
                self.test_data[self.test_labels == 3][:],
                self.test_data[self.test_labels == 4][:],
                self.test_data[self.test_labels == 5][:],
                self.test_data[self.test_labels == 6][:100]),axis=0)
                self.test_labels = np.concatenate((self.test_labels[self.test_labels == 1][:10],
                self.test_labels[self.test_labels == 2][:],
                self.test_labels[self.test_labels == 3][:],
                self.test_labels[self.test_labels == 4][:],
                self.test_labels[self.test_labels == 5][:],
                self.test_labels[self.test_labels == 6][:100]),axis=0)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        if self.train:
            (img1, img2), target = self.train_data[index], self.train_labels[index]
        else:
            (img1, img2), target = self.test_data[index], self.test_labels[index]

        
        #if self.train:
        #    (img1), target = self.train_data[index], self.train_labels[index]
        #else:
        #    (img1), target = self.test_data[index], self.test_labels[index]

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img1 = Image.fromarray(img1)
        img2 = Image.fromarray(img2)

        if self.transform is not None:
            img1 = self.transform(img1)
            img2 = self.transform(img2)

        if self.target_transform is not None:
            target = self.target_transform(target)
        if self.version == "side":
            return img1, target, index
        elif self.version == "top":
            return img2, target, index
        else:
            img = torch.stack((img1,img2), dim=-1)
            return img, target, index

    def __len__(self):
        if self.train:
            return len(self.train_data)
        else:
            return len(self.test_data)

    def _check_integrity(self):
        root = self.root
        for fentry in (self.train_list + self.test_list):
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    def _load_hashes(self, version):
        assert version in self.version_list, "Wrong version of dataset (top, side or both)"
        self.version = version
        self.base_folder = self.base_folder_list[0] #[self.version_list.index(version)]
        root = self.root
        if self.train_list == None:
            hashes_file=os.path.join(root, self.base_folder, 'hashes.json')
            assert os.path.exists(hashes_file), 'The hashes.json doesnt exist'
            with open(hashes_file) as hashes_buffer:    
                hashes = json.loads(hashes_buffer.read())
            keys = list(hashes.keys())
            self.train_list = list()
            self.test_list = list()
            for key in keys:
                if 'train' in key:
                    self.train_list.append(list((key,hashes[key])))
                elif 'test' in key:
                    self.test_list.append(list((key,hashes[key])))
            
