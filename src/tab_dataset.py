from PyQt5 import QtCore, QtWidgets, QtGui
import src.global_camera as global_camera
from PyQt5.QtCore import pyqtSignal as Signal
import os
import threading
from queue import Queue
from src.config_level import Config_level

import numpy as np
import src.image_processing as imp
import time
#import win32api
import src.global_queue as global_queue

class Tab_dataset(QtWidgets.QWidget):
    #signals

    def __init__(self):
        super(Tab_dataset, self).__init__()
        
        self.add_widgets()
        self.connect_actions()
        self.set_texts()

    def add_widgets(self):
        self.tab_dataset = QtWidgets.QWidget()
        self.tab_dataset.setObjectName("tab_dataset")
        self.gridLayout_4 = QtWidgets.QGridLayout(self)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.checkBox_camera2 = QtWidgets.QCheckBox(self)
        self.checkBox_camera2.setObjectName("checkBox_camera2")
        self.gridLayout_4.addWidget(self.checkBox_camera2, 5, 2, 1, 1)
        self.radioButton_group0_3 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_3.setObjectName("radioButton_group0_3")
        self.gridLayout_4.addWidget(self.radioButton_group0_3, 11, 0, 1, 1)
        self.lineEdit_save_location = QtWidgets.QLineEdit(self)
        self.lineEdit_save_location.setObjectName("lineEdit_save_location")
        self.gridLayout_4.addWidget(self.lineEdit_save_location, 3, 2, 1, 2)
        self.lineEdit_naming_cheme = QtWidgets.QLineEdit(self)
        self.lineEdit_naming_cheme.setObjectName("lineEdit_naming_cheme")
        self.gridLayout_4.addWidget(self.lineEdit_naming_cheme, 2, 2, 1, 2)
        self.checkBox_camera3 = QtWidgets.QCheckBox(self)
        self.checkBox_camera3.setObjectName("checkBox_camera3")
        self.gridLayout_4.addWidget(self.checkBox_camera3, 6, 2, 1, 1)
        self.spinBox_num_imgs = QtWidgets.QSpinBox(self)
        self.spinBox_num_imgs.setObjectName("spinBox_num_imgs")
        self.gridLayout_4.addWidget(self.spinBox_num_imgs, 11, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 12, 0, 1, 1)
        self.btn_save_location = QtWidgets.QPushButton(self)
        self.btn_save_location.setObjectName("btn_save_location")
        self.gridLayout_4.addWidget(self.btn_save_location, 3, 0, 1, 1)
        self.label_prompt_naming_scheme = QtWidgets.QLabel(self)
        self.label_prompt_naming_scheme.setObjectName("label_prompt_naming_scheme")
        self.gridLayout_4.addWidget(self.label_prompt_naming_scheme, 2, 0, 1, 1)
        self.checkBox_camera1 = QtWidgets.QCheckBox(self)
        self.checkBox_camera1.setObjectName("checkBox_camera1")
        self.gridLayout_4.addWidget(self.checkBox_camera1, 4, 2, 1, 1)
        self.radioButton_group0_0 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_0.setObjectName("radioButton_group0_0")
        self.gridLayout_4.addWidget(self.radioButton_group0_0, 8, 0, 1, 1)
        self.radioButton_group0_1 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_1.setObjectName("radioButton_group0_1")
        self.gridLayout_4.addWidget(self.radioButton_group0_1, 9, 0, 1, 1)
        self.label_prompt_num_images = QtWidgets.QLabel(self)
        self.label_prompt_num_images.setObjectName("label_prompt_num_images")
        self.gridLayout_4.addWidget(self.label_prompt_num_images, 11, 2, 1, 1)
        self.doubleSpinBox_recording_time = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_recording_time.setObjectName("doubleSpinBox_recording_time")
        self.gridLayout_4.addWidget(self.doubleSpinBox_recording_time, 10, 3, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout_4.addWidget(self.btn_stop, 14, 2, 1, 1)
        self.checkBox_camera4 = QtWidgets.QCheckBox(self)
        self.checkBox_camera4.setObjectName("checkBox_camera4")
        self.gridLayout_4.addWidget(self.checkBox_camera4, 7, 2, 1, 1)
        self.radioButton_group0_2 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_2.setObjectName("radioButton_group0_2")
        self.gridLayout_4.addWidget(self.radioButton_group0_2, 10, 0, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_4.addWidget(self.btn_start, 14, 0, 1, 1)
        self.label_prompt_recording_time = QtWidgets.QLabel(self)
        self.label_prompt_recording_time.setObjectName("label_prompt_recording_time")
        self.gridLayout_4.addWidget(self.label_prompt_recording_time, 10, 2, 1, 1)
        
    def connect_actions(self):
        pass

    def set_texts(self):
        self.checkBox_camera2.setText("Camera 2")
        self.radioButton_group0_3.setText("Fixed images mode")
        self.checkBox_camera3.setText("Camera 3")
        self.btn_save_location.setText("Save location")
        self.label_prompt_naming_scheme.setText("Naming scheme")
        self.checkBox_camera1.setText("Camera 1")
        self.radioButton_group0_0.setText("Manual mode")
        self.radioButton_group0_1.setText("Manual mode with trigger")
        self.label_prompt_num_images.setText("Number of images per camera")
        self.btn_stop.setText("Stop")
        self.checkBox_camera4.setText("Camera 4")
        self.radioButton_group0_2.setText("Timed mode")
        self.btn_start.setText("Start")
        self.label_prompt_recording_time.setText("Recording time")