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

    def __init__(self, camera_tabs = []):
        super(Tab_dataset, self).__init__()
        self.camera_tabs = camera_tabs

        self.add_widgets()
        self.connect_actions()
        self.set_texts()
        self.setup_validators()

        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(True)

        self.doubleSpinBox_fps.setDisabled(True)
        self.doubleSpinBox_recording_time.setDisabled(True)
        self.spinBox_num_imgs.setDisabled(True)

        for cam in self.checkBox_cameras:
            cam.setDisabled(True)

    def add_widgets(self):
        self.tab_dataset = QtWidgets.QWidget()
        self.tab_dataset.setObjectName("tab_dataset")
        self.gridLayout_4 = QtWidgets.QGridLayout(self)
        self.gridLayout_4.setObjectName("gridLayout_4")
       
        self.radioButton_group0_3 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_3.setObjectName("radioButton_group0_3")
        self.gridLayout_4.addWidget(self.radioButton_group0_3, 11, 0, 1, 1)
        self.lineEdit_save_location = QtWidgets.QLineEdit(self)
        self.lineEdit_save_location.setObjectName("lineEdit_save_location")
        self.gridLayout_4.addWidget(self.lineEdit_save_location, 3, 2, 1, 2)
        self.lineEdit_naming_scheme = QtWidgets.QLineEdit(self)
        self.lineEdit_naming_scheme.setObjectName("lineEdit_naming_scheme")
        self.gridLayout_4.addWidget(self.lineEdit_naming_scheme, 2, 2, 1, 2)
        
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
       
        self.radioButton_group0_2 = QtWidgets.QRadioButton(self)
        self.radioButton_group0_2.setObjectName("radioButton_group0_2")
        self.gridLayout_4.addWidget(self.radioButton_group0_2, 10, 0, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_4.addWidget(self.btn_start, 14, 0, 1, 1)
        self.label_prompt_recording_time = QtWidgets.QLabel(self)
        self.label_prompt_recording_time.setObjectName("label_prompt_recording_time")
        self.gridLayout_4.addWidget(self.label_prompt_recording_time, 10, 2, 1, 1)

        self.checkBox_cameras = [None,None,None,None]

        self.checkBox_cameras[3] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[3].setObjectName("checkBox_camera4")
        self.gridLayout_4.addWidget(self.checkBox_cameras[3], 7, 2, 1, 1)

        self.checkBox_cameras[0] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[0].setObjectName("checkBox_camera1")
        self.gridLayout_4.addWidget(self.checkBox_cameras[0], 4, 2, 1, 1)

        self.checkBox_cameras[2] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[2].setObjectName("checkBox_camera3")
        self.gridLayout_4.addWidget(self.checkBox_cameras[2], 6, 2, 1, 1)

        self.checkBox_cameras[1] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[1].setObjectName("checkBox_camera2")
        self.gridLayout_4.addWidget(self.checkBox_cameras[1], 5, 2, 1, 1)

        self.doubleSpinBox_fps = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_fps.setObjectName("doubleSpinBox_fps")
        self.gridLayout_4.addWidget(self.doubleSpinBox_fps, 9, 3, 1, 1)

        self.label_fps = QtWidgets.QLabel(self)
        self.label_fps.setObjectName("label_fps")
        self.gridLayout_4.addWidget(self.label_fps, 9, 2, 1, 1)

        self.label_fps.setAlignment(QtCore.Qt.AlignRight)
        self.label_prompt_num_images.setAlignment(QtCore.Qt.AlignRight)
        self.label_prompt_recording_time.setAlignment(QtCore.Qt.AlignRight)
        
    def connect_actions(self):
        self.checkBox_cameras[0].clicked.connect(self.start_enabler)
        self.checkBox_cameras[1].clicked.connect(self.start_enabler)
        self.checkBox_cameras[2].clicked.connect(self.start_enabler)
        self.checkBox_cameras[3].clicked.connect(self.start_enabler)

        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)

        self.radioButton_group0_0.clicked.connect(self.radio_clicked)
        self.radioButton_group0_1.clicked.connect(self.radio_clicked)
        self.radioButton_group0_2.clicked.connect(self.radio_clicked)
        self.radioButton_group0_3.clicked.connect(self.radio_clicked)

        self.camera_tabs[0].recording_update.connect(self.recording_callback)
        self.camera_tabs[1].recording_update.connect(self.recording_callback)
        self.camera_tabs[2].recording_update.connect(self.recording_callback)
        self.camera_tabs[3].recording_update.connect(self.recording_callback)

        self.lineEdit_naming_scheme.textChanged.connect(self.start_enabler)
        self.lineEdit_save_location.textChanged.connect(self.start_enabler)

        self.btn_save_location.clicked.connect(lambda: self.get_directory(self.lineEdit_save_location))

    def set_texts(self):
        self.checkBox_cameras[1].setText("Camera 2")
        self.radioButton_group0_3.setText("Fixed images mode")
        self.checkBox_cameras[2].setText("Camera 3")
        self.btn_save_location.setText("Save location")
        self.label_prompt_naming_scheme.setText("Naming scheme")
        self.checkBox_cameras[0].setText("Camera 1")
        self.radioButton_group0_0.setText("Manual mode")
        self.radioButton_group0_1.setText("Triggered mode")
        self.label_prompt_num_images.setText("Number of images per camera")
        self.label_fps.setText("FPS")
        self.btn_stop.setText("Stop")
        self.checkBox_cameras[3].setText("Camera 4")
        self.radioButton_group0_2.setText("Timed mode")
        self.btn_start.setText("Start")
        self.label_prompt_recording_time.setText("Recording time")

    def start_enabler(self):
        if ((self.checkBox_cameras[0].isChecked() or
           self.checkBox_cameras[1].isChecked() or 
           self.checkBox_cameras[2].isChecked() or 
           self.checkBox_cameras[3].isChecked()) and
           (self.radioButton_group0_0.isChecked() or
           self.radioButton_group0_1.isChecked() or
           self.radioButton_group0_2.isChecked() or
           self.radioButton_group0_3.isChecked()) and
           self.lineEdit_naming_scheme.text() != "" and
           self.lineEdit_save_location.text() != ""):
            self.btn_start.setDisabled(False)
        else:
            self.btn_start.setDisabled(True)

    def start(self):
        # Prepare to start recording - variables and such
        for index, cam in enumerate(self.camera_tabs):
            if cam.connected and self.checkBox_cameras[index].isChecked():
                # If preview or recording running -> stop it first
                if cam.recording:
                    cam.record()
                if cam.preview_live:
                    cam.preview(1)

                # set naming scheme on given tab
                cam.line_edit_sequence_name.setText(self.lineEdit_naming_scheme.text())
                cam.line_edit_save_location.setText(f"{self.lineEdit_save_location.text()}/Cam{index + 1}")

                # Set up acquisition mode
                if self.radioButton_group0_0.isChecked():
                    cam.line_edit_sequence_duration.setValue(0)
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("AcquisitionMode",1)
                elif self.radioButton_group0_1.isChecked():
                    cam.line_edit_sequence_duration.setValue(0)
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("AcquisitionMode",1)
                    #Trigger source is line1
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("TriggerSource",2)
    #TODO check if this setting is enough to trigger correctly
                if self.radioButton_group0_2.isChecked():
                    cam.line_edit_sequence_duration.setValue(self.doubleSpinBox_recording_time.value())
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("AcquisitionMode",1)
                if self.radioButton_group0_3.isChecked():
                    cam.line_edit_sequence_duration.setValue(0)
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("AcquisitionMode",3)
                    global_camera.cams.active_devices[global_camera.active_cam[cam.camIndex]].set_parameter("AcquisitionFrameCount",self.spinBox_num_imgs.value())
                
        # Run recording on all cameras
        for cam in self.camera_tabs:
            if self.checkBox_cameras[cam.camIndex].isChecked() and cam.connected:
                if self.radioButton_group0_0.isChecked() or self.radioButton_group0_2.isChecked():
                    cam.record(self.doubleSpinBox_fps.value())
                else:
                    cam.record()

        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)

    def stop(self):
        for cam in self.camera_tabs:
            if self.checkBox_cameras[cam.camIndex].isChecked() and cam.connected:
                # If preview or recording running -> stop it first
                if cam.preview_live:
                    cam.preview(1)
                if cam.recording:
                    cam.record()
        
        self.btn_stop.setDisabled(True)
        self.start_enabler()

    def setup_validators(self):
        """!@brief create input constrains for various widgets
        @details if a text widget needs certain input type, the validators are
        set up here. For example setting prohibited characters of the file saved. Not used yet!
        """
        self.doubleSpinBox_fps.setMinimum(0.1)
        self.doubleSpinBox_fps.setMaximum(16777216)
        self.doubleSpinBox_recording_time.setMinimum(0.1)
        self.doubleSpinBox_recording_time.setMaximum(16777216)
        self.spinBox_num_imgs.setMaximum(16777216)
        self.spinBox_num_imgs.setMinimum(1)
        expression = QtCore.QRegExp("^[^\\\\/:*?\"<>|]*$")
        self.lineEdit_naming_scheme.setValidator(QtGui.QRegExpValidator(expression))

    def radio_clicked(self):
        if self.radioButton_group0_0.isChecked():
            self.doubleSpinBox_fps.setDisabled(False)
            self.doubleSpinBox_recording_time.setDisabled(True)
            self.spinBox_num_imgs.setDisabled(True)
        elif self.radioButton_group0_1.isChecked():  
            self.doubleSpinBox_fps.setDisabled(True)
            self.doubleSpinBox_recording_time.setDisabled(True)
            self.spinBox_num_imgs.setDisabled(True)
        elif self.radioButton_group0_2.isChecked():
            self.doubleSpinBox_fps.setDisabled(False)
            self.doubleSpinBox_recording_time.setDisabled(False)
            self.spinBox_num_imgs.setDisabled(True)
        elif self.radioButton_group0_3.isChecked():
            self.doubleSpinBox_fps.setDisabled(True)
            self.doubleSpinBox_recording_time.setDisabled(True)
            self.spinBox_num_imgs.setDisabled(False)

        self.start_enabler()

    def recording_callback(self, state, cam_index):
        print("In recording callback")
        if self.checkBox_cameras[cam_index].isChecked():
            if state == False:
                print("stopping")
                self.stop()

    def get_directory(self, line_output = None):
        """!@brief Opens file dialog for user to set path to save frames.
        @details Method is called by Save Location button. Path is written to 
        the label next to the button and can be further modified.
        """
        #Open file dialog for choosing a folder
        name = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                     "Select Folder",
                                                     )
        
        #Set label text to chosen folder path
        if(line_output):
            line_output.setText(name)
        return name

    def checkbox_enabler(self):
        for index, cam in enumerate(self.camera_tabs):
            self.checkBox_cameras[index].setDisabled(not cam.connected)
            if not cam.connected:
                self.checkBox_cameras[index].setChecked(False)
        
        self.start_enabler()