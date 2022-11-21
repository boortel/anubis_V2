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

class Tab_camera(QtWidgets.QWidget):
    #signals

    ##Signal configuration change to the GUI
    configuration_update = Signal(str, str, float)#name, location, duration
    signal_update_parameters = Signal()
    signal_show_parameters = Signal()
    signal_clear_parameters = Signal()

    ##Camera Control signals
    send_status_msg = Signal(str, int, int)
    connection_update = Signal(bool, int, str, int)#connected, state - 0=disconnected 1=standby 2=busy, camera name, camera tab
    recording_update = Signal(bool, int)
    preview_update = Signal(bool, int)
    request_prediction = Signal(np.ndarray)
    received_info = Signal(int, int)
    fps_info = Signal(float, int)

    def __init__(self, camIndex, prevRef, prevWinRef):
        super(Tab_camera, self).__init__()
        self.preview_live = False
        self.recording = False
        ##Holds parameter category paths for tree widget
        self.top_items = {}
        ##Holds children widgets for tree widget
        self.children_items = {}

        ##Flag is not set while the application is getting parameters from the cam object
        self.param_flag = threading.Event()

        ##Flag used when running various parameter refreshing methods
        self.update_flag = threading.Event()
        ##Flag used when running various parameter refreshing methods
        self.update_completed_flag = threading.Event()
        self.update_completed_flag.set()


        ##Used to store values of parameters when automatically refreshing them
        self.parameter_values = {}
        
        ##Contains all dynamically created widgets for parameters
        self.feat_widgets = {}
        ##Contains all dynamically created labels of parameters
        self.feat_labels = {}
        ##Stores dictionaries of every parameter until they are processed to the GUI
        self.feat_queue = Queue()

        self.connected = False
        ##Widget used to transfer GUI changes from thread into the main thread while showing parameters
        self.parameters_signal = QtWidgets.QLineEdit()
        self.parameters_signal.textChanged.connect(self.show_parameters)

        ##Indexing variable
        self.camIndex = camIndex

        ##Reference to the preview area
        self.camera_preview = prevRef

        ##Reference to the preview window
        self.camera_preview_window = prevWinRef

        ##Camera control stuff
        ##Widget used to transfer GUI changes from thread into the main thread while updating preview
        self.resize_signal = QtWidgets.QLineEdit()
        self.resize_signal.textChanged.connect(self.update_img)


        ##Holds current frame displayed in the GUI
        self.image_pixmap = None
        ##Width of the preview area
        self.w_preview = 0
        ##Height of the preview area
        self.h_preview = 0

        self.image_pixmap_window = None
        ##Width of the preview area
        self.w_preview_window = 0
        ##Height of the preview area
        self.h_preview_window = 0

        ##Signals that a recording was stopped, either by timer or manually
        self.interrupt_flag = threading.Event()

        ##Current frames per second received from the camera
        self.fps = 0.0
        ##Total sum of received frames for active camera session
        self.received = 0

        ##Last value of the dragging in the preview area - x axis
        self.move_x_prev = 0
        ##Last value of the dragging in the preview area - y axis
        self.move_y_prev = 0

        ##Value of current preview zoom in %/100
        self.preview_zoom = 1
        ##Resizing image to preview area size instead of using zoom
        self.preview_fit = True

        ##True if the processing is enabled, False otherwise
        self.processing = False

        self.connected = False

        self.add_widgets()
        self.connect_actions()
        self.set_texts()
        self.setup_validators()

        self.thread_auto_refresh_params = threading.Thread(target=self.start_refresh_parameters)
        self.thread_auto_refresh_params.setDaemon(True)

        self.thread_reset = threading.Thread(target=self.reset)
        self.thread_reset.setDaemon(True)

        self.thread_reset_flag = threading.Event()
        self.thread_reset_flag.set()


    def add_widgets(self):

        self.setObjectName(u"tab_camera_1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        # Conf camera
        self.conf_camera = QtWidgets.QGroupBox(self)
        self.conf_camera.setObjectName(u"conf_camera")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.conf_camera)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_config_level = QtWidgets.QLabel(self.conf_camera)
        self.label_config_level.setObjectName(u"label_config_level")

        self.gridLayout_3.addWidget(self.label_config_level, 0, 0, 1, 1)

        self.tree_features = QtWidgets.QTreeWidget(self.conf_camera)
        self.tree_features.setObjectName(u"tree_features")

        self.gridLayout_3.addWidget(self.tree_features, 1, 0, 1, 3)

        self.btn_save_config = QtWidgets.QPushButton(self.conf_camera)
        self.btn_save_config.setObjectName(u"btn_save_config")

        self.gridLayout_3.addWidget(self.btn_save_config, 2, 0, 1, 2)

        self.btn_load_config = QtWidgets.QPushButton(self.conf_camera)
        self.btn_load_config.setObjectName(u"btn_load_config")

        self.gridLayout_3.addWidget(self.btn_load_config, 2, 2, 1, 1)

        self.combo_config_level = QtWidgets.QComboBox(self.conf_camera)
        self.combo_config_level.addItem("")
        self.combo_config_level.addItem("")
        self.combo_config_level.addItem("")
        self.combo_config_level.setObjectName(u"combo_config_level")

        self.gridLayout_3.addWidget(self.combo_config_level, 0, 1, 1, 2)

        self.verticalLayout_2.addWidget(self.conf_camera)


        # Conf recording
        self.conf_recording = QtWidgets.QGroupBox(self)
        self.conf_recording.setObjectName(u"conf_recording")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.conf_recording)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_sequence_name = QtWidgets.QLabel(self.conf_recording)
        self.label_sequence_name.setObjectName(u"label_sequence_name")

        self.gridLayout_5.addWidget(self.label_sequence_name, 0, 0, 1, 4)

        self.label_file_name_recording = QtWidgets.QLabel(self.conf_recording)
        self.label_file_name_recording.setObjectName(u"label_file_name_recording")

        self.gridLayout_5.addWidget(self.label_file_name_recording, 1, 0, 1, 1)

        self.line_edit_sequence_name = QtWidgets.QLineEdit(self.conf_recording)
        self.line_edit_sequence_name.setObjectName(u"line_edit_sequence_name")

        self.gridLayout_5.addWidget(self.line_edit_sequence_name, 1, 1, 1, 3)

        self.btn_file_manager_save_location = QtWidgets.QPushButton(self.conf_recording)
        self.btn_file_manager_save_location.setObjectName(u"btn_file_manager_save_location")

        self.gridLayout_5.addWidget(self.btn_file_manager_save_location, 2, 0, 1, 1)

        self.line_edit_save_location = QtWidgets.QLineEdit(self.conf_recording)
        self.line_edit_save_location.setObjectName(u"line_edit_save_location")

        self.gridLayout_5.addWidget(self.line_edit_save_location, 2, 1, 1, 3)

        self.label_sequence_duration = QtWidgets.QLabel(self.conf_recording)
        self.label_sequence_duration.setObjectName(u"label_sequence_duration")

        self.gridLayout_5.addWidget(self.label_sequence_duration, 3, 0, 1, 2)

        self.line_edit_sequence_duration = QtWidgets.QDoubleSpinBox(self.conf_recording)
        self.line_edit_sequence_duration.setObjectName(u"line_edit_sequence_duration")

        self.gridLayout_5.addWidget(self.line_edit_sequence_duration, 3, 2, 1, 2)

        self.label_sequence_duration_tip = QtWidgets.QLabel(self.conf_recording)
        self.label_sequence_duration_tip.setObjectName(u"label_sequence_duration_tip")

        self.gridLayout_5.addWidget(self.label_sequence_duration_tip, 4, 0, 1, 4)

        self.btn_save_sequence_settings = QtWidgets.QPushButton(self.conf_recording)
        self.btn_save_sequence_settings.setObjectName(u"btn_save_sequence_settings")

        self.gridLayout_5.addWidget(self.btn_save_sequence_settings, 5, 0, 1, 3)

        self.btn_reset_sequence_settings = QtWidgets.QPushButton(self.conf_recording)
        self.btn_reset_sequence_settings.setObjectName(u"btn_reset_sequence_settings")

        self.gridLayout_5.addWidget(self.btn_reset_sequence_settings, 5, 3, 1, 1)

        self.verticalLayout_2.addWidget(self.conf_recording)


        # Ctl image
        self.ctl_image = QtWidgets.QGroupBox(self)
        self.ctl_image.setObjectName(u"ctl_image")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.ctl_image)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.ctl_record = QtWidgets.QGroupBox(self.ctl_image)
        self.ctl_record.setObjectName(u"ctl_record")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.ctl_record)

        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.btn_single_frame = QtWidgets.QPushButton(self.ctl_record)
        self.btn_single_frame.setObjectName(u"btn_single_frame")
        self.gridLayout_8.addWidget(self.btn_single_frame, 0, 0, 1, 1)

        self.btn_start_recording = QtWidgets.QPushButton(self.ctl_record)
        self.btn_start_recording.setObjectName(u"btn_start_recording")
        self.gridLayout_8.addWidget(self.btn_start_recording, 0, 1, 1, 1)

        self.btn_start_preview = QtWidgets.QPushButton(self.ctl_record)
        self.btn_start_preview.setObjectName(u"btn_start_preview")
        self.gridLayout_8.addWidget(self.btn_start_preview, 1, 0, 1, 1)

        self.btn_start_process = QtWidgets.QPushButton(self.ctl_record)
        self.btn_start_process.setObjectName(u"btn_start_process")
        self.gridLayout_8.addWidget(self.btn_start_process, 1, 1, 1, 1)

        self.gridLayout_9.addWidget(self.ctl_record, 0, 0, 1, 1)

        self.ctl_zoom = QtWidgets.QGroupBox(self.ctl_image)
        self.ctl_zoom.setObjectName(u"ctl_zoom")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.ctl_zoom)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.btn_zoom_in = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_in.setObjectName(u"btn_zoom_in")

        self.gridLayout_6.addWidget(self.btn_zoom_in, 0, 0, 1, 1)

        self.btn_zoom_out = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_out.setObjectName(u"btn_zoom_out")

        self.gridLayout_6.addWidget(self.btn_zoom_out, 0, 1, 1, 1)

        self.btn_zoom_fit = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_fit.setObjectName(u"btn_zoom_fit")

        self.gridLayout_6.addWidget(self.btn_zoom_fit, 1, 0, 1, 1)

        self.btn_zoom_100 = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_100.setObjectName(u"btn_zoom_100")

        self.gridLayout_6.addWidget(self.btn_zoom_100, 1, 1, 1, 1)


        self.gridLayout_9.addWidget(self.ctl_zoom, 0, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.ctl_image)


    def connect_actions(self):
        # Params
        self.combo_config_level.currentIndexChanged.connect(self.load_parameters)
        self.btn_save_config.clicked.connect(self.save_cam_config)
        self.btn_load_config.clicked.connect(self.load_cam_config)

        # Recording
        self.line_edit_save_location.textChanged.connect(self.send_conf_update)
        self.line_edit_sequence_duration.valueChanged.connect(self.send_conf_update)
        self.line_edit_sequence_name.textChanged.connect(self.send_conf_update)
        self.btn_file_manager_save_location.clicked.connect(lambda: self.get_directory(self.line_edit_save_location))
        self.btn_save_sequence_settings.clicked.connect(self.save_seq_settings)
        self.btn_reset_sequence_settings.clicked.connect(self.reset_seq_settings)

        # Image ctl
        self.btn_zoom_out.clicked.connect(lambda: self.set_zoom(-1))
        self.btn_zoom_fit.clicked.connect(lambda: self.set_zoom(0))
        self.btn_zoom_in.clicked.connect(lambda: self.set_zoom(1))
        self.btn_zoom_100.clicked.connect(lambda: self.set_zoom(100))
        self.btn_single_frame.clicked.connect(self.single_frame)
        self.btn_start_preview.clicked.connect(self.preview)
        self.btn_start_recording.clicked.connect(self.record)
        self.btn_start_process.clicked.connect(self.toggle_processing)

    def set_texts(self):

        self.conf_camera.setTitle("Configure Camera")
        self.label_config_level.setText("Configuration level")
        self.tree_features.headerItem().setText(0, "Feature")
        self.tree_features.headerItem().setText(1, "Value")
        self.btn_save_config.setText("Save Configuration")
        self.btn_load_config.setText("Load Configuration")
        self.combo_config_level.setItemText(0, "Beginner")
        self.combo_config_level.setItemText(1, "Expert")
        self.combo_config_level.setItemText(2, "Guru")

        self.conf_recording.setTitle("Configure Recording")
        self.label_sequence_name.setText("Tip: Use %n for sequence number, %d for date and %t for time stamp ")
        self.label_file_name_recording.setText("File name")
        self.btn_file_manager_save_location.setText("Save Location")
        self.label_sequence_duration.setText("Sequence duration [s]")
        self.label_sequence_duration_tip.setText("Tip: Leave empty for manual control using Start/Stop recording buttons")
        self.btn_save_sequence_settings.setText("Save settings")
        self.btn_reset_sequence_settings.setText("Default settings")

        self.ctl_image.setTitle("Image Control")
        self.ctl_record.setTitle("")
        self.btn_single_frame.setText("Single frame")
        self.btn_start_recording.setText("Start/Stop recording")
        self.btn_start_preview.setText("Start/Stop preview")
        self.btn_start_process.setText("Start/Stop processing")
        self.ctl_zoom.setTitle("")
        self.btn_zoom_in.setText("Zoom In")
        self.btn_zoom_out.setText("Zoom Out")
        self.btn_zoom_fit.setText("Fit to window")
        self.btn_zoom_100.setText("Zoom to 100%")

    def start_auto_refresh(self):
        self.thread_reset_flag.wait()
        self.thread_auto_refresh_params.start()

    def reset(self):
        self.thread_reset_flag.clear()
        
        self.connected = False
        self.thread_auto_refresh_params.join()
        self.preview_live = False
        self.recording = False
        self.btn_load_config.setDisabled(False)
        self.btn_save_config.setDisabled(False)
        self.param_flag.clear()
        self.update_flag.clear()
        self.update_completed_flag.set()
        self.clear_parameters()
        self.image_pixmap = None
        self.w_preview = 0
        self.h_preview = 0
        self.image_pixmap_window = None
        self.w_preview_window = 0
        self.h_preview_window = 0
        self.interrupt_flag.clear()
        self.fps = 0.0
        self.received = 0
        self.move_x_prev = 0
        self.move_y_prev = 0
        self.preview_zoom = 1
        self.preview_fit = True
        self.connected = False

        self.thread_auto_refresh_params = threading.Thread(target=self.start_refresh_parameters)
        self.thread_auto_refresh_params.setDaemon(True)

        self.thread_reset = threading.Thread(target=self.reset)
        self.thread_reset.setDaemon(True)
        self.thread_reset_flag.set()

    # ==============================================
    # Camera control
    # ==============================================

    def toggle_processing(self):
        """just toggle processing of the preview image"""
        self.processing = not self.processing

    def record(self, fps = 0):
        """!@brief Starts and stops recording
        @details Is called by start/stop button. Recording is always started 
        manually. Recording ends with another button click or after time set 
        in self.line_edit_sequence_duration passes. Save location and name is 
        determined by the text in self.line_edit_save_location and 
        self.line_edit_sequence_name.
        """
        if self.connected:
            if(not self.recording):
                # clear parameters to prevent user from changing them
                self.signal_clear_parameters.emit()
#TODO Make showing params faster and remove line above 

                #Change status icon and print status message
                self.connection_update.emit(True, 2, "-1", self.camIndex)
                self.send_status_msg.emit("Starting recording", 0, self.camIndex)
                
                self.recording_update.emit(True, self.camIndex)
                self.recording = True
                self.btn_load_config.setDisabled(True)
                self.btn_save_config.setDisabled(True)
                
                #Start new recording with defined name and save path
                global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].start_recording(self.line_edit_save_location.text(),
                                    self.line_edit_sequence_name.text(),
                                    fps)
                
                
                #If automatic sequence duration is set, create thread that will
                #automatically terminate the recording
                if(self.line_edit_sequence_duration.value() > 0):
                    self.interrupt_flag.clear()
                    self.seq_duration_thread = threading.Thread(target=self.seq_duration_wait)
                    self.seq_duration_thread.daemon = True
                    self.seq_duration_thread.start()
                
                #Start live preview in a new thread
                self.show_preview_thread = threading.Thread(target=self.show_preview)
                self.show_preview_thread.daemon = True
                self.show_preview_thread.start()
                self.send_status_msg.emit("Recording",0, self.camIndex)
            else:
                #Set status message and standby icon
                self.connection_update.emit(True, 1, "-1", self.camIndex)
                self.send_status_msg.emit("Stopping recording", 0, self.camIndex)
                
                #Tell automatic sequence duration thread to end
                self.interrupt_flag.set()
                
                #End recording
                global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].stop_recording()
                self.recording = False
                self.preview_live = False
                self.recording_update.emit(False, self.camIndex)
                
                self.btn_load_config.setDisabled(False)
                self.btn_save_config.setDisabled(False)
                self.preview_update.emit(False, self.camIndex)
                self.send_status_msg.emit("Recording stopped", 3500, self.camIndex)

                self.signal_show_parameters.emit()
#TODO Make showing params faster and remove line above 
    
    def seq_duration_wait(self):
        """!@brief Automatic recording interrupt.
        @details Let camera record for defined time and if the recording is not
        manually terminated stop the recording.
        """
        #wait for the first frame to be received
        while global_queue.active_frame_queue[global_camera.active_cam[self.camIndex]].empty():
            time.sleep(0.001)
        
        #print status message
        self.send_status_msg.emit("Recording for "+self.line_edit_sequence_duration.text()+"s started", 0, self.camIndex)
        
        #wait either for manual recording stop or wait for defined time
        self.interrupt_flag.wait(self.line_edit_sequence_duration.value())
        
        #If the recording is still running (not terminated manually), stop 
        #the recording.
        if(self.recording):
            self.record()
    
    def preview(self):
        """!@brief Starts live preview
        @details Unlike recording method, this method does not save frames to a
        drive. Preview picture is rendered in separate thread.
        """
        #continue only if camera is connected
        if self.connected:
            if(not self.preview_live):
                #clears parameters to prevent user from changing them
                self.signal_clear_parameters.emit()
#TODO Make showing params faster and remove line above 

                #Set status message and icon
                self.connection_update.emit(True, 2, "-1", self.camIndex)             
                self.preview_update.emit(True, self.camIndex)
                
                #Start camera frame acquisition (not recording)
                global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].start_acquisition()
                
                #Create and run thread to draw frames to gui
                self.send_status_msg.emit("Starting preview", 1500, self.camIndex)
                self.show_preview_thread = threading.Thread(target=self.show_preview)
                self.preview_live = True

                self.show_preview_thread.daemon = True
                self.show_preview_thread.start()
            else:
                #Reset status icon and print message
                self.connection_update.emit(True, 1, "-1", self.camIndex)
                
                #Stop receiving frames
                global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].stop_acquisition()
                
                self.preview_live = False
                self.send_status_msg.emit("Stopping preview", 1500, self.camIndex)
                
                self.preview_update.emit(False, self.camIndex)
                self.signal_show_parameters.emit()
#TODO Make showing params faster and remove line above                
    
    def set_zoom(self, flag):
        """!@brief Set the zoom amount of the image previewed
        @details This method only sets the zooming variable, actual resizing
        is done in other methods.
        @param[in] flag Is used to define type of zoom. 
        1  - zoom in
        -1 - zoom out
        0  - zoom fit
        100- zoom reset
        """
        #flag 1 zoom in, -1 zoom out, 0 zoom fit, 100 zoom reset
        if(flag == -1 and self.preview_zoom > 0.1):
            self.preview_fit = False
            self.preview_zoom -= 0.1
        elif(flag == 1):
            self.preview_fit = False
            self.preview_zoom += 0.1
        elif(flag == 0):
            self.preview_fit = True
        elif(flag == 100):
            self.preview_fit = False
            self.preview_zoom = 1
    
    def single_frame(self):
        """!@brief Acquire and draw a single frame.
        @details Unlike the live preview, this method runs in the main thread 
        and therefore can modify frontend variables. The method may block whole
        application but its execution should be fast enough to not make a 
        difference.
        """
        #Method runs only if camera is connected
        if self.connected and not(self.preview_live or self.recording):
            #Set status icon and message
            self.send_status_msg.emit("Receiving single frame", 1500, self.camIndex)
            self.connection_update.emit(True, 2, "-1", self.camIndex)
            
            #Get image
            image, pixel_format = global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].get_single_frame()
            #Try to run prediction
            self.request_prediction.emit(image)
            
            #Set up a new value of received frames in the statusbar
            self.received = self.received + 1
            self.received_info.emit(self.received, self.camIndex)

            #Convert image to proper format fo PyQt
            h, w, ch = image.shape
            bytes_per_line = ch * w
            image = QtGui.QImage(image.data, w, h, bytes_per_line, self._get_QImage_format(pixel_format))

            
            #get size of preview window
            w_preview = self.camera_preview.size().width()
            h_preview = self.camera_preview.size().height()

            w_preview_window = self.camera_preview_window.size().width()
            h_preview_window = self.camera_preview_window.size().height()
            
            image_scaled = image.scaled(w_preview, 
                                        h_preview, 
                                        QtCore.Qt.KeepAspectRatio)

            image_scaled_window = image.scaled(w_preview_window, 
                                        h_preview_window, 
                                        QtCore.Qt.KeepAspectRatio)
            
            #Set image to gui
            self.camera_preview.resize(w_preview,
                                       h_preview)
            self.camera_preview.setPixmap(QtGui.QPixmap.fromImage(image_scaled))
            self.camera_preview.show()

             #Set image to gui
            self.camera_preview_window.resize(w_preview_window,
                                       h_preview_window)
            self.camera_preview_window.setPixmap(QtGui.QPixmap.fromImage(image_scaled_window))
            self.camera_preview_window.show()
            
            #Reset status icon
            self.connection_update.emit(True, 1, "-1", self.camIndex)
    
    def show_preview(self):
        """!@brief Draws image from camera in real time.
        @details Acquires images from camera and draws them in real time at 
        the same rate as is display refresh_rate. If the frames come too fast,
        only one at the most recent one is drawn and the rest is dumped.
        """
        #Determine refresh rate of used display. This way the method will not
        #run too slowly or redundantly fast.
        #device = win32api.EnumDisplayDevices()
        #refresh_rate = win32api.EnumDisplaySettings(device.DeviceName, -1).DisplayFrequency
        refresh_rate = 30
        
        #Auxiliary variables for fps calculation
        frames = 0
        cycles = 0
        
        color_format = QtGui.QImage.Format_Invalid
        str_color = None
        time_fps = time.monotonic_ns()
        #runs as long as the camera is recording or preview is active
        while (self.recording or self.preview_live) and (global_camera.active_cam[self.camIndex] in global_queue.active_frame_queue.keys()):
            cycles = cycles + 1
            
            #Draw only if there is at least 1 frame to draw
            if not global_queue.active_frame_queue[global_camera.active_cam[self.camIndex]].empty():
                image = global_queue.active_frame_queue[global_camera.active_cam[self.camIndex]].get_nowait()
                self.received = self.received + 1
                
                frames += 1
                
                #Dump all remaining frames (If frames are received faster than 
                #refresh_rate).
                while not global_queue.active_frame_queue[global_camera.active_cam[self.camIndex]].qsize() == 0:
                    frames += 1
                    self.received = self.received + 1
                    global_queue.active_frame_queue[global_camera.active_cam[self.camIndex]].get_nowait()
                
                if self.processing:
                    #Try to process the image
                    image = imp.processImage_main(image)
                    h, w, ch = image[0].shape
                    bytes_per_line = ch * w
                else:
                    #Convert image to proper format for PyQt
                    h, w, ch = image[0].shape
                    bytes_per_line = ch * w

                #Set up a new value of received frames in the statusbar
                self.received_info.emit(self.received, self.camIndex)
                
#Change to time dependency instead of cycle#More cycles -> more exact fps calculation (value is more stable in gui)
                
                if cycles > 30:
                    time_now = time.monotonic_ns()
                    time_passed = time_now - time_fps
                    time_fps = time_now
                    #[frames*Hz/c] -> [frames/s]
                    self.fps = round(frames/(time_passed/1_000_000_000),1)
                    self.fps_info.emit(self.fps, self.camIndex)
                    
                    cycles = 0
                    frames = 0
                
                if(str_color != image[1]):
                    str_color = image[1]
                    color_format = self._get_QImage_format(str_color)
                    
                if(color_format == QtGui.QImage.Format_Invalid):
                    self.send_status_msg.emit("Used image format is not supported", 0, self.camIndex)
                
                
                image = QtGui.QImage(image[0].data, w, h, bytes_per_line, color_format)
                
                #get size of preview window if zoom fit is selected
                if(self.preview_fit == True):
                    self.w_preview = self.camera_preview.size().width()
                    self.h_preview = self.camera_preview.size().height()
                    image_scaled = image.scaled(self.w_preview, 
                                                self.h_preview, 
                                                QtCore.Qt.KeepAspectRatio)

                    self.w_preview_window = self.camera_preview_window.size().width()
                    self.h_preview_window = self.camera_preview_window.size().height()
                    image_scaled_window = image.scaled(self.w_preview_window, 
                                                        self.h_preview_window, 
                                                        QtCore.Qt.KeepAspectRatio)
                else:#else use zoom percentage
                    self.w_preview = w*self.preview_zoom
                    self.h_preview = h*self.preview_zoom
                    image_scaled = image.scaled(self.w_preview,
                                         self.h_preview,
                                         QtCore.Qt.KeepAspectRatio)

                    self.w_preview_window = w*self.preview_zoom
                    self.h_preview_window = h*self.preview_zoom
                    image_scaled_window = image.scaled(self.w_preview_window,
                                                self.h_preview_window,
                                                QtCore.Qt.KeepAspectRatio)
                
                self.image_pixmap = QtGui.QPixmap.fromImage(image_scaled)
                self.image_pixmap_window = QtGui.QPixmap.fromImage(image_scaled_window)
                self.preview_callback()
                #Set image to gui
            #Wait for next display frame
            time.sleep(1/refresh_rate)
        
        #When recording stops, change fps to 0
        self.fps = 0.0
        self.fps_info.emit(self.fps, self.camIndex)
    
    def preview_callback(self):
        """!@brief Auxiliary method used to transfer thread state change into
        the main thread.
        """
        if(self.resize_signal.text() != "A"):
            self.resize_signal.setText("A")
        else:
            self.resize_signal.setText("B")

    def eventFilter(self, obj, event):
        """!@brief Implements dragging inside preview area
        @details whin user cliks and drags inside of a preview area, this 
        method is called and do the scrolling based on the distance dragged in
        each direction.
        """
        if (obj == self.camera_preview):
            if(event.type() == QtCore.QEvent.MouseMove ):
    
                if self.move_x_prev == 0:
                    self.move_x_prev = event.pos().x()
                if self.move_y_prev == 0:
                    self.move_y_prev = event.pos().y()
    
                dist_x = self.move_x_prev - event.pos().x()
                dist_y = self.move_y_prev - event.pos().y()
                self.camera_preview.verticalScrollBar().setValue(
                    self.camera_preview.verticalScrollBar().value() + dist_y)
                self.camera_preview.horizontalScrollBar().setValue(
                    self.camera_preview.horizontalScrollBar().value() + dist_x)
                #self.preview_area.scrollContentsBy(dist_x,dist_y)
                self.move_x_prev = event.pos().x()
                self.move_y_prev = event.pos().y()

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.last_time_move = 0
        return QtWidgets.QWidget.eventFilter(self, obj, event)
    
    def update_img(self):
        """!@brief update image in the live preview window.
        @details This method must run in the main thread as it modifies frontend
        data of the gui.
        """
        if type(self.image_pixmap) == type(None) or type(self.image_pixmap_window) == type(None):
            return

        #Resize preview label if preview window size changed
        if(self.w_preview != self.camera_preview.size().width() or
                   self.h_preview != self.camera_preview.size().height()):
            self.camera_preview.resize(self.w_preview,
                                       self.h_preview)
        
        #set a new image to the preview area
        self.camera_preview.setPixmap(self.image_pixmap)
        self.camera_preview.show()

        #Resize preview label if preview window size changed
        if(self.w_preview_window != self.camera_preview_window.size().width() or
                   self.h_preview_window != self.camera_preview_window.size().height()):
            self.camera_preview_window.resize(self.w_preview_window,
                                            self.h_preview_window)
        
        #set a new image to the preview area
        self.camera_preview_window.setPixmap(self.image_pixmap_window)
        self.camera_preview_window.show()

    # ==============================================
    # Recording 
    # ==============================================
    
    def setup_validators(self):
        """!@brief create input constrains for various widgets
        @details if a text widget needs certain input type, the validators are
        set up here. For example setting prohibited characters of the file saved. Not used yet!
        """
        self.line_edit_sequence_duration.setMinimum(0)
        self.line_edit_sequence_duration.setMaximum(16777216)
        expression = QtCore.QRegExp("^[^\\\\/:*?\"<>|]*$")
        self.line_edit_sequence_name.setValidator(QtGui.QRegExpValidator(expression))

    def reset_seq_settings(self):
        """!@brief Restores default recording settings
        @details Settings are saved to config.ini file. Defaults are hard-coded
        in this method.
        """
        file_contents = []
        
        #Open config file and load its contents
        with open("config.ini", 'r') as config:
            file_contents = config.readlines()
        
        end_of_rec_conf = None
        #Find end of Recording config part of the file
        #if no delimiter is found a new one is added
        try:
            end_of_rec_conf = file_contents.index("CTI_FILES_PATHS\n")
        except(ValueError):
            file_contents.append("CTI_FILES_PATHS\n")
            end_of_rec_conf = -1
            
        with open("config.ini", 'w') as config:
            #Write default states to the file
            config.write("RECORDING\n")
            config.write("filename=img(%n)\n")
            config.write("save_location=Recording\n")
            #maybe set to the documents folder
            config.write("sequence_duration=0\n")
            
            #When at the end of recording config part, just copy the rest of
            #the initial file.
            if(end_of_rec_conf):
                for line in file_contents[end_of_rec_conf:]:
                    config.write(line)

        #Fill the Recording tab with updated values
        self.load_config("img(%n)", "Recording", "0")
        
        #Print status msg
        self.send_status_msg.emit("Configuration restored", 2500, self.camIndex)
    
    def save_seq_settings(self):
        """!@brief Saves recording settings
        @details Settings are saved to config.ini file. Parameters saved are:
        file name, save, location and sequence duration.
        """
        file_contents = []
        
        #Open config file and load its contents
        with open("config.ini", 'r') as config:
            file_contents = config.readlines()
        
        #Open config file for writing
        with open("config.ini", 'w') as config:
            
            for line in file_contents:
                #Reading configuration for recording
                if(line.startswith("filename=")):
                    config.write("filename=" + self.line_edit_sequence_name.text() + "\n")
                elif(line.startswith("save_location=")):
                    config.write("save_location=" + self.line_edit_save_location.text() + "\n")
                elif(line.startswith("sequence_duration=")):
                    config.write("sequence_duration=" + self.line_edit_sequence_duration.text() + "\n")
                else:
                    #All content not concerning recording is written back without change
                    config.write(line)

        self.send_status_msg.emit("Configuration saved", 0, self.camIndex)
    

    def load_config(self, filename=None , save_location=None, sequence_duration=None):
        """!@brief Fills in saved values for recording configuration
        @param[in] filename Template for naming saved files
        @param[in] save_location Where should the images be saved
        @param[in] sequence_duration Length of a recording sequence
        """
        try:
            sequence_duration = float(sequence_duration)
        except ValueError:
            sequence_duration = 0
    
        if(filename):
            self.line_edit_sequence_name.setText(filename)
        if(save_location):
            self.line_edit_save_location.setText(save_location)
        if(sequence_duration):
            self.line_edit_sequence_duration.setValue(sequence_duration)

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
    
    def send_conf_update(self):
        """!@brief Used to emit configuration update signal based on current values of line edits"""
        self.configuration_update.emit(self.line_edit_sequence_name.text(), 
                                        self.line_edit_save_location.text(), 
                                        self.line_edit_sequence_duration.value())
    
    # ==============================================
    # Camera
    # ==============================================

    def clear_parameters(self):
        self.top_items = {}
        self.children_items = {}
        
        self.tree_features.clear()
        
        for name in self.feat_widgets:
            self.feat_widgets[name].deleteLater()
        
        for name in self.feat_labels:
            self.feat_labels[name].deleteLater()
        
        self.feat_widgets.clear()
        self.feat_labels.clear()

    def show_parameters(self):
        """!@brief Loads all camera's features and creates dynamic widgets for
        every feature.
        @details This method is called when user first enters parameters tab or
        when the configuration level changes. All the widgets are created dynamically
        and based on the type of the feature, proper widget type is selected. Also
        these widgets have method to change their value associated with them
        when created.
        """
        num = 0
        
        categories = []
        self.clear_parameters()
        if self.feat_queue.empty():
            self.load_parameters()
        
        while not self.feat_queue.empty():
            try:
                param = self.feat_queue.get()
                param['attr_cat'] = param['attr_cat'].lstrip('/')
                ctgs = param['attr_cat'].split('/')
                for i, ctg in enumerate(ctgs):
                    if(not(ctg in categories)):
                        if(i == 0):
                            self.top_items[ctg] = QtWidgets.QTreeWidgetItem([ctg])
                            self.tree_features.addTopLevelItem(self.top_items[ctg])
                        else:
                            self.top_items[ctg] = QtWidgets.QTreeWidgetItem([ctg])
                            self.top_items[ctgs[i-1]].addChild(self.top_items[ctg])
                        categories.append(ctg)
            #Create a new label with name of the feature
            
                self.feat_labels[param["name"]] = QtWidgets.QLabel(self)
                self.feat_labels[param["name"]].setObjectName(param["name"])
                self.feat_labels[param["name"]].setText(param["attr_name"])
                #If the feature has a tooltip, set it.
                try:
                    self.feat_labels[param["name"]].setToolTip(param["attr_tooltip"])
                except:
                    pass
                
                #Place the label on the num line of the layout
                #self.parameters_layout.setWidget(num, QtWidgets.QFormLayout.LabelRole, self.feat_labels[param["name"]])
                
                #If the feature does not have a value, set it to 0
                if param["attr_value"] == None:
                    param["attr_value"] = 0
                    
                #Based on the feature type, right widget is chosen to hold the
                #feature's value
                
                if param["attr_type"] == "IntFeature":
                    #For int feature a Line edit field is created, but only 
                    #integers can be written in.
                    self.feat_widgets[param["name"]] = QtWidgets.QSpinBox(self)
                    if(param["attr_range"]):
                        self.feat_widgets[param["name"]].setRange(
                                                param["attr_range"][0],
                                                param["attr_range"][1])
                    
                    #Set text to the current value of the feature
                    self.feat_widgets[param["name"]].setValue(param["attr_value"])
                    
                    #Call feature change for this feature when enter is pressed in this field.
                    #Text is the value that will be set to the feature.
                    self.feat_widgets[param["name"]].valueChanged.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],new_val))
                elif param["attr_type"] == "FloatFeature":
                    #For float feature a Line edit field is created, but only 
                    #real numbers can be written in.
                    self.feat_widgets[param["name"]] = QtWidgets.QDoubleSpinBox(self)
                    if(param["attr_range"]):
                        self.feat_widgets[param["name"]].setRange(
                                                param["attr_range"][0],
                                                param["attr_range"][1])
                    
                    #Set text to the current value of the feature
                    self.feat_widgets[param["name"]].setValue(param["attr_value"])
                    
                    #Call feature change for this feature when enter is pressed in this field.
                    #Text is the value that will be set to the feature.
                    self.feat_widgets[param["name"]].valueChanged.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],new_val))
                elif param["attr_type"] == "StringFeature":
                    #For string feature a Line edit field is created.
                    self.feat_widgets[param["name"]] = QtWidgets.QLineEdit(self)
                    
                    #Set text to the current value of the feature
                    self.feat_widgets[param["name"]].setText(param["attr_value"])
                    
                    #Call feature change for this feature when enter is pressed in this field.
                    #Text is the value that will be set to the feature.
                    self.feat_widgets[param["name"]].returnPressed.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],new_val))            
                elif param["attr_type"] == "BoolFeature":
                    #For bool feature a checkbox is created.
                    self.feat_widgets[param["name"]] = QtWidgets.QCheckBox(self)
                    
                    #If value is true the checkbox is ticked otherwise remains empty
                    self.feat_widgets[param["name"]].setChecked(param["attr_value"])
                    
                    #When state of the checkbox change, the feature is sent to 
                    #the camera and changed to the new state
                    self.feat_widgets[param["name"]].stateChanged.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],new_val))
                elif param["attr_type"] == "EnumFeature":
                    #For enum feature a combo box is created.
                    self.feat_widgets[param["name"]] = QtWidgets.QComboBox(self)
                    
                    #All available enum states are added as options to the
                    #combo box.
                    for enum in param["attr_enums"]:
                        self.feat_widgets[param["name"]].addItem(str(enum))
                    
                    #Search the options and find the index of the active value
                    index = self.feat_widgets[param["name"]].findText(str(param["attr_value"]), QtCore.Qt.MatchFixedString)
                    
                    #Set found index to be the active one
                    if index >= 0:
                        self.feat_widgets[param["name"]].setCurrentIndex(index)
                    
                    #When different option is selected change the given enum in
                    #the camera
                    self.feat_widgets[param["name"]].activated.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],self.feat_widgets[param["name"]].itemText(new_val)))
                elif param["attr_type"] == "CommandFeature":
                    #If the feature type is not recognized, create a label with 
                    #the text error
                    self.feat_widgets[param["name"]] = QtWidgets.QPushButton(self)
                    self.feat_widgets[param["name"]].setText("Execute command")
                    self.feat_widgets[param["name"]].clicked.connect(lambda val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].execute_command(param["name"]))
                else:
                    #If the feature type is not recognized, create a label with 
                    #the text error
                    self.feat_widgets[param["name"]] = QtWidgets.QLabel(self)
                    self.feat_widgets[param["name"]].setText("Unknown feature type")
                
                self.feat_widgets[param["name"]].setEnabled(param["attr_enabled"])
                
                #Add newly created widget to the layout on the num line
                new_item = QtWidgets.QTreeWidgetItem(self.top_items[ctgs[-1]] ,['', ''])
                #add new item to the last subcategory of its category tree
                self.tree_features.setItemWidget(new_item, 0,self.feat_labels[param["name"]])
                self.tree_features.setItemWidget(new_item, 1,self.feat_widgets[param["name"]])
                #new_item = QtWidgets.QTreeWidgetItem(self.top_items[param['attr_cat']] ,[self.feat_labels[param["name"]], self.feat_widgets[param["name"]]])
                self.children_items[param["name"]] = new_item
                #self.parameters_layout.setWidget(num, QtWidgets.QFormLayout.FieldRole, self.feat_widgets[param["name"]])
                num += 1
            except:
                pass
                #we'll get here when queue is empty
        self.param_flag.clear()
    
    def start_refresh_parameters(self):
        """!@brief Called automatically when feat_refresh_timer runs out
        @details used to start a thread to refresh parameters values. Not
        called by user but automatically.
        """
        #called every 2 seconds
        while(self.connected):
            time.sleep(2)
            if (self.feat_widgets and self.connected and
                not(self.preview_live or self.recording) and                 
#TODO Make showing params faster and remove line above 
                not self.param_flag.is_set() and self.update_completed_flag.is_set()):
                
                self.update_completed_flag.clear()
                
                self.update_thread = threading.Thread(target=self.get_new_val_parameters)
                self.update_thread.daemon = True
                self.update_thread.start()
    
    def get_new_val_parameters(self):
        """!@brief Check for new parameter value
        @details after camera features are loaded, this method periodically 
        calls for the most recent value of each parameter.
        """
        
        if(not self.feat_widgets):
            self.update_completed_flag.set()
            return
        
        params = Queue()
        for key in self.feat_widgets.keys():
            value, type = global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].read_param_value(key)
            name = key
            param = {"name": name,
                    "attr_type": type,
                    "attr_value": value}
            params.put_nowait(param)
        
        while(not params.empty()):
            parameter = params.get()
            if(not(self.preview_live or self.recording)):
                self.parameter_values[parameter["name"]] = parameter["attr_value"]
            else:
                self.update_completed_flag.set()
                return
        self.update_flag.set()
        self.signal_update_parameters.emit()
    
    def update_parameters(self):
        """!@brief Writes new values of the parameters to the GUI.
        @details After get_new_val_parameters finishes, the update_flag is set 
        and this method can transfer the new values of the parameters to the GUI. 
        Like start_refresh_parameters, this method is bound to the timer.
        """
        if (self.connected and not self.param_flag.is_set() and 
            self.update_flag.is_set()
            and not(self.preview_live or self.recording)):
#TODO Make showing params faster and remove line above 
            
            self.update_flag.clear()
            
            for parameter in self.feat_widgets:
                try:
                    value = self.parameter_values[parameter]
                    widget = self.feat_widgets[parameter]
                    if(value == None) or (widget.hasFocus()):
                        continue

                    
                    if(type(widget) == QtWidgets.QLineEdit):
                        widget.setText(str(value))
                    elif(type(widget) == QtWidgets.QComboBox):
                        index = widget.findText(str(value), QtCore.Qt.MatchFixedString)
                        #Set found index to be the active one
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    elif(type(widget) == QtWidgets.QDoubleSpinBox or
                         type(widget) == QtWidgets.QSpinBox):
                        widget.setValue(value)
                    elif(type(widget) == QtWidgets.QCheckBox):
                        widget.setChecked(value)
                except:
                    pass
            self.update_completed_flag.set()
    
    def load_parameters(self):
        """!@brief Fills layout with feature name and value pairs
        @details Based on the feature type a new label, text area, checkbox or
        combo box is created. In this version all available parameters are shown.
        """
        
        #Start filling features in only with connected camera
        if self.connected and not self.param_flag.is_set():
            #Status message
            
            self.send_status_msg.emit("Reading features", 0, self.camIndex)
            
            #empty feature queue
            self.get_params_thread = threading.Thread(
                target=global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].get_parameters,
                kwargs={'feature_queue': self.feat_queue,
                        'flag': self.param_flag,
                        'visibility': Config_level(self.combo_config_level.currentIndex()+1)})
            self.param_callback_thread = threading.Thread(target=self.callback_parameters)
            
            
            self.param_callback_thread.setDaemon(True)
            self.get_params_thread.setDaemon(True)
            self.param_callback_thread.start()
            self.get_params_thread.start()
    
    def save_cam_config(self):
        """!@brief Opens file dialog for user to select where to save camera 
        configuration.
        @details Called by Save configuration button. Configuration is saved 
        as an .xml file and its contents are dependent on module used in Camera 
        class to save the config.
        """
        
        if(self.connected and not self.recording and not self.preview_live):
            #Open file dialog for choosing a save location and name
            name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Save Configuration",
                                                         filter="XML files (*.xml)",
                                                         directory="config.xml")
            
            #Save camera config to path specified in name (0 index)
            global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].save_config(name[0])
    
    def load_cam_config(self):
        """!@brief Allows a user to choose saved xml configuration and load it
        into the camera
        @details Allowes only xml file in the file dialog and after loading prints
        a status message
        """
        if self.connected:
            if(not self.recording and not self.preview_live):
                name = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             "Load Configuration",
                                                             filter="XML files (*.xml)")
               
                #Set label text to chosen folder path
                if(name[0]):
                    tries = 0
                    while(tries <= 10):
                        if(global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].load_config(name[0])):
                            self.send_status_msg.emit("Configuration loaded", 0, self.camIndex)
                            return
                        else:
                            tries += 1
                    self.send_status_msg.emit("Loading failed", 2500, self.camIndex)
            else:
                self.send_status_msg.emit("Stop recording and preview before loading config", 0, self.camIndex)
        
    def callback_parameters(self):
        """!@brief Auxiliary method used to transfer thread state change into
        the main thread.
        """
        self.param_flag.wait()
        
        if(self.parameters_signal.text() != "A"):
            self.parameters_signal.setText("A")
        else:
            self.parameters_signal.setText("B")

    def _get_QImage_format(self, format_string):
        """!@brief The image format provided by camera object (according to 
        GenICam standard) is transoformed to one of the color formats supported
        by PyQt.
        @param[in] format_string text containing color format defined by GenICam
        or another standard.
        """
        image_format = None
        
        if(format_string == 'Format_Mono'):
            image_format = QtGui.QImage.Format_Mono
        elif(format_string == 'Format_MonoLSB'):
            image_format = QtGui.QImage.Format_MonoLSB
        elif(format_string == 'Format_Indexed8'):
            image_format = QtGui.QImage.Format_Indexed8
        elif(format_string == 'Format_RGB32'):
            image_format = QtGui.QImage.Format_RGB32
        elif(format_string == 'Format_ARGB32'):
            image_format = QtGui.QImage.Format_ARGB32
        elif(format_string == 'Format_ARGB32_Premultiplied'):
            image_format = QtGui.QImage.Format_ARGB32_Premultiplied
        elif(format_string == 'Format_RGB16'):
            image_format = QtGui.QImage.Format_RGB16
        elif(format_string == 'Format_ARGB8565_Premultiplied'):
            image_format = QtGui.QImage.Format_ARGB8565_Premultiplied
        elif(format_string == 'Format_RGB666'):
            image_format = QtGui.QImage.Format_RGB666
        elif(format_string == 'Format_ARGB6666_Premultiplied'):
            image_format = QtGui.QImage.Format_ARGB6666_Premultiplied
        elif(format_string == 'Format_RGB555'):
            image_format = QtGui.QImage.Format_RGB555
        elif(format_string == 'Format_ARGB8555_Premultiplied'):
            image_format = QtGui.QImage.Format_ARGB8555_Premultiplied
        elif(format_string == 'Format_RGB888' or format_string == 'RGB8'):
            image_format = QtGui.QImage.Format_RGB888
        elif(format_string == 'Format_RGB444'):
            image_format = QtGui.QImage.Format_RGB444
        elif(format_string == 'Format_ARGB4444_Premultiplied'):
            image_format = QtGui.QImage.Format_ARGB4444_Premultiplied
        elif(format_string == 'Format_RGBX8888'):
            image_format = QtGui.QImage.Format_RGBX8888
        elif(format_string == 'Format_RGBA8888' or format_string == 'RGBa8'):
            image_format = QtGui.QImage.Format_RGBA8888
        elif(format_string == 'Format_RGBA8888_Premultiplied'):
            image_format = QtGui.QImage.Format_RGBA8888_Premultiplied
        elif(format_string == 'Format_BGR30'):
            image_format = QtGui.QImage.Format_BGR30
        elif(format_string == 'Format_A2BGR30_Premultiplied'):
            image_format = QtGui.QImage.Format_A2BGR30_Premultiplied
        elif(format_string == 'Format_RGB30'):
            image_format = QtGui.QImage.Format_RGB30
        elif(format_string == 'Format_A2RGB30_Premultiplied'):
            image_format = QtGui.QImage.Format_A2RGB30_Premultiplied
        elif(format_string == 'Format_Alpha8'):
            image_format = QtGui.QImage.Format_Alpha8
        elif(format_string == 'Format_Grayscale8' or format_string == 'Mono8'):
            image_format = QtGui.QImage.Format_Grayscale8
        elif(format_string == 'Format_Grayscale16' or format_string == 'Mono16'):
            image_format = QtGui.QImage.Format_Grayscale16
        elif(format_string == 'Format_RGBX64'):
            image_format = QtGui.QImage.Format_RGBX64
        elif(format_string == 'Format_RGBA64'):
            image_format = QtGui.QImage.Format_RGBA64
        elif(format_string == 'Format_RGBA64_Premultiplied'):
            image_format = QtGui.QImage.Format_RGBA64_Premultiplied
        elif(format_string == 'Format_BGR888' or format_string == 'BGR8'):
            image_format = QtGui.QImage.Format_BGR888
        else:
            image_format = QtGui.QImage.Format_Invalid
        
        return image_format
        
        '''
        SFNC OPTIONS not yet implemented
        Mono1p
        Mono2p, Mono4p, Mono8s, Mono10, Mono10p, Mono12, Mono12p, Mono14, 
        , R8, G8, B8, , RGB8_Planar, , RGB10, RGB10_Planar, 
        RGB10p32, RGB12, RGB12_Planar, RGB16, RGB16_Planar, RGB565p, BGR10, 
        BGR12, BGR16, BGR565p, , BGRa8, YUV422_8, YCbCr411_8, YCbCr422_8, 
        YCbCr601_422_8, YCbCr709_422_8, YCbCr8, BayerBG8, BayerGB8, BayerGR8, 
        BayerRG8, BayerBG10, BayerGB10, BayerGR10, BayerRG10, BayerBG12, 
        BayerGB12, BayerGR12, BayerRG12, BayerBG16, BayerGB16, BayerGR16, 
        BayerRG16, Coord3D_A8, Coord3D_B8, Coord3D_C8, Coord3D_ABC8, 
        Coord3D_ABC8_Planar, Coord3D_A16, Coord3D_B16, Coord3D_C16, 
        Coord3D_ABC16, Coord3D_ABC16_Planar, Coord3D_A32f, Coord3D_B32f, 
        Coord3D_C32f, Coord3D_ABC32f, Coord3D_ABC32f_Planar, Confidence1, 
        Confidence1p, Confidence8, Confidence16, Confidence32f, Raw8, Raw16, 
        Device-specific
        - GigE Vision Specific:
        Mono12Packed, BayerGR10Packed, BayerRG10Packed, BayerGB10Packed, 
        BayerBG10Packed, BayerGR12Packed, BayerRG12Packed, BayerGB12Packed, 
        BayerBG12Packed, RGB10V1Packed, RGB12V1Packed, 
        - Deprecated:
            will not be implemented for now as they are not used in genicam anymore
        '''
        '''
        SFNC OPTIONS - all
        Mono1p
        Mono2p, Mono4p, Mono8, Mono8s, Mono10, Mono10p, Mono12, Mono12p, Mono14, 
        Mono16, R8, G8, B8, RGB8, RGB8_Planar, RGBa8, RGB10, RGB10_Planar, 
        RGB10p32, RGB12, RGB12_Planar, RGB16, RGB16_Planar, RGB565p, BGR10, 
        BGR12, BGR16, BGR565p, BGR8, BGRa8, YUV422_8, YCbCr411_8, YCbCr422_8, 
        YCbCr601_422_8, YCbCr709_422_8, YCbCr8, BayerBG8, BayerGB8, BayerGR8, 
        BayerRG8, BayerBG10, BayerGB10, BayerGR10, BayerRG10, BayerBG12, 
        BayerGB12, BayerGR12, BayerRG12, BayerBG16, BayerGB16, BayerGR16, 
        BayerRG16, Coord3D_A8, Coord3D_B8, Coord3D_C8, Coord3D_ABC8, 
        Coord3D_ABC8_Planar, Coord3D_A16, Coord3D_B16, Coord3D_C16, 
        Coord3D_ABC16, Coord3D_ABC16_Planar, Coord3D_A32f, Coord3D_B32f, 
        Coord3D_C32f, Coord3D_ABC32f, Coord3D_ABC32f_Planar, Confidence1, 
        Confidence1p, Confidence8, Confidence16, Confidence32f, Raw8, Raw16, 
        Device-specific
        - GigE Vision Specific:
        Mono12Packed, BayerGR10Packed, BayerRG10Packed, BayerGB10Packed, 
        BayerBG10Packed, BayerGR12Packed, BayerRG12Packed, BayerGB12Packed, 
        BayerBG12Packed, RGB10V1Packed, RGB12V1Packed, 
        - Deprecated:
        Mono8Signed (Deprecated, use Mono8s)
        RGB8Packed (Deprecated, use RGB8) ,BGR8Packed (Deprecated, use BGR8), 
        RGBA8Packed (Deprecated, use RGBa8), BGRA8Packed (Deprecated, use BGRa8), 
        RGB10Packed (Deprecated, use RGB10), BGR10Packed (Deprecated, use BGR10), 
        RGB12Packed (Deprecated, use RGB12), BGR12Packed (Deprecated, use BGR12), 
        RGB16Packed (Deprecated, use RGB16), BGR16Packed (Deprecated, use BGR16), 
        RGB10V2Packed (Deprecated, use RGB10p32), BGR10V2Packed (Deprecated, use BGR10p32), 
        RGB565Packed (Deprecated, use RGB565p), BGR565Packed (Deprecated, use BGR565p), 
        YUV411Packed (Deprecated, use YUV411_8_UYYVYY), YUV422Packed (Deprecated, use YUV422_8_UYVY), 
        YUV444Packed (Deprecated, use YUV8_UYV), YUYVPacked (Deprecated, use YUV422_8), 
        RGB8Planar (Deprecated, use RGB8_Planar), RGB10Planar (Deprecated, use RGB10_Planar),
        RGB12Planar (Deprecated, use RGB12_Planar), RGB16Planar (Deprecated, use RGB16_Planar), 
        '''
