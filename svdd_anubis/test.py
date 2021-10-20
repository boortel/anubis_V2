#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 21:26:47 2020

@author: kratochvila
"""
import torch
import numpy as np
import os
import random
import json

from utils.config import Config
from utils.visualization.plot_images_grid import plot_images_grid
from deepSVDD import DeepSVDD
from datasets.main import load_dataset

from sklearn.metrics import confusion_matrix
from tabulate import tabulate

from sklearn.metrics.ranking import roc_curve
import matplotlib.pyplot as plt

xp_path="../log/varroa" # "../log/v3/mydata_300_HRes_480_one_val_fine"
dataset_name = 'bee' # 'mydata100HRes_480'

load_config=os.path.join(xp_path,"config.json")
load_model="/model.tar"

cfg = Config(locals().copy())
# Load experiment config from JSON-file
cfg.load_config(import_json=load_config)
print('Loaded configuration from %s.' % load_config)

print('Dataset: %s' % dataset_name)
# Set seed
if cfg.settings['seed'] != -1:
    random.seed(cfg.settings['seed'])
    np.random.seed(cfg.settings['seed'])
    torch.manual_seed(cfg.settings['seed'])
    print('Set seed to %d.' % cfg.settings['seed'])

print('Computation device: %s' % cfg.settings['device'])
print('Number of dataloader workers: %d' % cfg.settings['n_jobs_dataloader'])
    
deep_SVDD = DeepSVDD(cfg.settings['objective'], cfg.settings['nu'])
deep_SVDD.set_network(cfg.settings['net_name'])
# If specified, load Deep SVDD model (radius R, center c, network weights, and possibly autoencoder weights)
deep_SVDD.load_model(model_path=xp_path+load_model, load_ae=False)

dataset = load_dataset(dataset_name, cfg.settings['data_path'], cfg.settings['normal_class'])
deep_SVDD.test(dataset,cfg.settings['device'],cfg.settings['n_jobs_dataloader'], cfg.settings['batch_size'])

# Plot most anomalous and most normal (within-class) test samples
indices, labels, scores = zip(*deep_SVDD.results['test_scores'])
indices, labels, scores = np.array(indices), np.array(labels), np.array(scores)
idx_sorted = indices[labels == 0][np.argsort(scores[labels == 0])]  # sorted from lowest to highest anomaly score
idx_sorted_wrong = indices[labels == 1][np.argsort(scores[labels == 1])]
if dataset_name in ('mnist', 'cifar10', 'mydata100', 'mydata300', 'mydata100HRes', 'mydata300HRes','bee'):

    if dataset_name == 'mnist':
        X_normals = dataset.test_set.test_data[idx_sorted[:32], ...].unsqueeze(1)
        X_outliers = dataset.test_set.test_data[idx_sorted[-32:], ...].unsqueeze(1)

    if dataset_name == 'cifar10':
        X_normals = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted[:32], ...], (0, 3, 1, 2)))
        X_outliers = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted[-32:], ...], (0, 3, 1, 2)))
    
    if dataset_name in ('mydata100', 'mydata300', 'mydata100HRes', 'mydata300HRes','bee'):
        X_normals = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted[:32], ...], (0, 3, 1, 2)))
        X_outliers = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted[-32:], ...], (0, 3, 1, 2)))
        X_wrong_normals = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted_wrong[:32], ...], (0, 3, 1, 2)))
        X_wrong_outliers = torch.tensor(np.transpose(dataset.test_set.test_data[idx_sorted_wrong[-32:], ...], (0, 3, 1, 2)))

    plot_images_grid(X_normals,title='Most normal examples', padding=2, nrow=4) # export_img=xp_path + '/normals', 
    plot_images_grid(X_outliers, title='Most anomalous examples', padding=2, nrow=4) # export_img=xp_path + '/outliers',
    if dataset_name in ('mydata100', 'mydata300', 'mydata100HRes', 'mydata300HRes','bee'):
        plot_images_grid(X_wrong_normals, title='Most normal examples', padding=2, nrow=4) # export_img=xp_path + '/wrong_normals',
        plot_images_grid(X_wrong_outliers, title='Most anomalous examples', padding=2, nrow=4) # export_img=xp_path + '/wrong_outliers',

# Open results on training dataset
with open(xp_path + '/results.json') as f_r:
    results = json.loads(f_r.read())

# Plot ROC curves
fpr_1,tpr_1, thresholds_1 = roc_curve([x[1] for x in deep_SVDD.results['test_scores']],
                                [x[2] for x in deep_SVDD.results['test_scores']])

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(fpr_1,tpr_1)
ax.set_title("ROC curve for experiment: {0} on {1} dataset".format(xp_path.split('/')[-1],dataset_name))
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
plt.savefig(xp_path + '/' +'roc_{0}_{1}'.format(xp_path.split('/')[-1],dataset_name), bbox_inches='tight', pad_inches=0.1)
# plt.clf()

thresh_1 = thresholds_1[tpr_1 >=0.9][0]

fpr_2,tpr_2, thresholds_2 = roc_curve([x[1] for x in results['test_scores']],
                                [x[2] for x in results['test_scores']])

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(fpr_2,tpr_2)
ax.set_title("ROC curve for experiment: {0} on {1} dataset".format(xp_path.split('/')[-1],cfg.settings['dataset_name']))
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
plt.savefig(xp_path + '/'  + 'roc_{0}_{1}'.format(xp_path.split('/')[-1],cfg.settings['dataset_name']), bbox_inches='tight', pad_inches=0.1)
# plt.clf()

thresh_2 = thresholds_2[tpr_2 >=0.9][0]

# Print Confusion matrix for tpr > 0.9

print('Dataset: %s' % dataset_name)
print("Test AUC: {0:.3f}%".format(100. * deep_SVDD.results['test_auc']))
print("The first threshold after tpr == 0.9 is: {} ".format(thresh_1))
[[TP,FN],[FP,TN]] = confusion_matrix([x[1] for x in deep_SVDD.results['test_scores']],
                                     [x[2] >= thresh_1 for x in deep_SVDD.results['test_scores']])
table = [["Label OK",str(TP),str(FN)],["Label NOK",str(FP),str(TN)]]
headers = ["Prediction\nOK","Prediction\nNOK"]
print(tabulate(table, headers, tablefmt="presto"))

# dataset_cfg = load_dataset(cfg.settings['dataset_name'], cfg.settings['data_path'], cfg.settings['normal_class'])

print('Dataset: %s' % cfg.settings['dataset_name'])    
print("Test AUC: {0:.3f}%".format(100. * results['test_auc']))
print("The first threshold after tpr == 0.9 is: {} ".format(thresh_2))
[[TP,FN],[FP,TN]] = confusion_matrix([x[1] for x in results['test_scores']],
                                     [x[2] >= thresh_2 for x in results['test_scores']])
table = [["Label OK",str(TP),str(FN)],["Label NOK",str(FP),str(TN)]]
headers = ["Prediction\nOK","Prediction\nNOK"]
print(tabulate(table, headers, tablefmt="presto"))

with open(xp_path + '/' + 'compare.text', 'w') as file:
    print('Dataset: %s' % dataset_name, file=file)
    print("Test AUC: {0:.3f}%".format(100. * deep_SVDD.results['test_auc']), file=file)
    print("The first threshold after tpr == 0.9 is: {} ".format(thresh_1), file=file)
    [[TP,FN],[FP,TN]] = confusion_matrix([x[1] for x in deep_SVDD.results['test_scores']],
                                         [x[2] >= thresh_1 for x in deep_SVDD.results['test_scores']])
    table = [["Label OK",str(TP),str(FN)],["Label NOK",str(FP),str(TN)]]
    headers = ["Prediction\nOK","Prediction\nNOK"]
    print(tabulate(table, headers, tablefmt="presto"), file=file)
    
    print('Dataset: %s' % cfg.settings['dataset_name'], file=file)    
    print("Test AUC: {0:.3f}%".format(100. * results['test_auc']), file=file)
    print("The first threshold after tpr == 0.9 is: {} ".format(thresh_2), file=file)
    [[TP,FN],[FP,TN]] = confusion_matrix([x[1] for x in results['test_scores']],
                                         [x[2] >= thresh_2 for x in results['test_scores']])
    table = [["Label OK",str(TP),str(FN)],["Label NOK",str(FP),str(TN)]]
    print(tabulate(table, headers, tablefmt="presto"), file=file)

# print("Confusion matrix\n\t\tPrediction\n\t{0}\t\t{1}\nLabel\n\t{2}\t\t{3}".format(TP,FN,FP,TN))
# plot_images_grid(torch.tensor(np.transpose(dataset.test_set.test_data[0],(2,0,1))),nrow=1)
# plt.imshow(np.transpose(dataset.test_set[14][0].cpu().numpy(),(1,2,0)))

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(fpr_1,tpr_1,label=dataset_name)
ax.plot(fpr_2,tpr_2,label=cfg.settings['dataset_name'])
ax.legend()
ax.set_title("ROC curves compare for experiment: {0}".format(xp_path.split('/')[-1]))
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
# plt.savefig(xp_path + '/' +'roc_{0}_{1}'.format(xp_path.split('/')[-1],dataset_name), bbox_inches='tight', pad_inches=0.1)
# plt.clf()

dataset_cfg = load_dataset(cfg.settings['dataset_name'], cfg.settings['data_path'], cfg.settings['normal_class'])
idx=[x[1] for x in results['test_scores']],[x[2] >= thresh_2 for x in results['test_scores']]
ix=[i for i in range(len(idx[0])) if not idx[0][i]==idx[1][i]]
if len(ix) > 0:
    X= torch.tensor(np.transpose(dataset_cfg.test_set.test_data[ix, ...], (0, 3, 1, 2)))
    plot_images_grid(X, title='Wrong classified', padding=2, nrow=10)