from PyQt5 import QtCore, QtWidgets, QtGui
import global_camera
from PyQt5.QtCore import pyqtSignal as Signal
import os
import threading
from queue import Queue
from config_level import Config_level


class Tab_camera(QtWidgets.QWidget):

    def __init__(self):
        super(Tab_camera, self).__init__()

        self.add_widgets()
        self.connect_actions()
        self.set_texts()

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

        self.file_manager_save_location = QtWidgets.QPushButton(self.conf_recording)
        self.file_manager_save_location.setObjectName(u"file_manager_save_location")

        self.gridLayout_5.addWidget(self.file_manager_save_location, 2, 0, 1, 1)

        self.line_edit_save_location = QtWidgets.QLineEdit(self.conf_recording)
        self.line_edit_save_location.setObjectName(u"line_edit_save_location")

        self.gridLayout_5.addWidget(self.line_edit_save_location, 2, 1, 1, 3)

        self.label_sequence_duration = QtWidgets.QLabel(self.conf_recording)
        self.label_sequence_duration.setObjectName(u"label_sequence_duration")

        self.gridLayout_5.addWidget(self.label_sequence_duration, 3, 0, 1, 2)

        self.line_edit_sequence_duration = QtWidgets.QLineEdit(self.conf_recording)
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
        self.file_manager_save_location.clicked.connect(lambda: self.get_directory(self.line_edit_save_location))
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
        self.file_manager_save_location.setText("Save Location")
        self.label_sequence_duration.setText("Sequence duration [s]")
        self.label_sequence_duration_tip.setText("Tip: Leave empty for manual control using Start/Stop recording buttons")
        self.btn_save_sequence_settings.setText("Save settings")
        self.btn_reset_sequence_settings.setText("Default settings")
        self.ctl_image.setTitle("Image Control")
        self.ctl_record.setTitle("")
        self.btn_single_frame.setText("Single frame")
        self.btn_start_recording.setText("Start/Stop recording")
        self.btn_start_preview.setText("Start/Stop preview")
        self.ctl_zoom.setTitle("")
        self.btn_zoom_in.setText("Zoom In")
        self.btn_zoom_out.setText("Zoom Out")
        self.btn_zoom_fit.setText("Fit to window")
        self.btn_zoom_100.setText("Zoom to 100%")

    # Recording
    def setup_validators(self):
        """!@brief create input constrains for various widgets
        @details if a text widget needs certain input type, the validators are
        set up here. For example setting prohibited characters of the file saved.
        """
        self.line_edit_sequence_duration.setValidator(QtGui.QDoubleValidator(0,16777216,5))
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
        self.send_status_msg.emit("Configuration restored",2500)
    
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
        self.send_status_msg.emit("Configuration saved", 0)
    

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
    



