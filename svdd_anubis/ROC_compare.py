#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 12:27:34 2020

@author: pc-neuron
"""
import json
from sklearn.metrics.ranking import roc_curve
import matplotlib.pyplot as plt

xp_path = '../log/v'#'../log/v2/'
exs = [#'2/mydata_100_LRes_soft_01','2/mydata_100_LRes_soft_05','2/mydata_100_LRes_soft_1'
       #'2/mydata_100_LRes_one','2/mydata_100_LRes_one_pre', '2/mydata_300_LRes_one','2/mydata_300_LRes_one_pre'
       #'3/mydata_300_HRes_480_one_pre','3/mydata_300_HRes_480_one_pre_best','3/mydata_300_HRes_480_one',
       #'mydata_100_LRes_one', 'mydata_300_LRes_one', 'mydata_100_HRes_one',
       #'mydata_100_HRes_480_one_pre', 'mydata_100_HRes_480_soft_05',
       #'2/mydata_100_HRes_480_soft_05_pre','2/mydata_100_HRes_480_one_test',
       #'2/mydata_300_HRes_480_one_pre','2/mydata_300_HRes_480_one_test',
       '2/mydata_300_LRes_one_pre','3/mydata_100_HRes_480_one_val_fine','3/mydata_300_HRes_480_one_val_fine','2/../autoaugment/best'
       ]
xp_paths = [xp_path + ex for ex in exs]
fpr,tpr = list(), list()
for path in xp_paths:
    with open(path + '/results.json') as f_r:
        results = json.loads(f_r.read())   
    f,t, thresholds = roc_curve([x[1] for x in results['test_scores']],
                                [x[2] for x in results['test_scores']])
    fpr.append(f)
    tpr.append(t)

fig, ax = plt.subplots(figsize=(6, 6))
for x,y,name in zip(fpr,tpr,exs):
    ax.plot(x,y,label=name.split('/')[1])
ax.legend()
ax.set_title("Comparision of ROC curves")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
plt.savefig(xp_path[:-1] + 'ROC_comparision'+' g-i+AA' , bbox_inches='tight', pad_inches=0.1)
# plt.clf()
