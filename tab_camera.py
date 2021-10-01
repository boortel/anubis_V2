from PyQt5 import QtCore, QtWidgets 
import global_camera
from PyQt5.QtCore import pyqtSignal as Signal
import os
import threading
from queue import Queue
from config_level import Config_level

class Tab_camera(QtWidgets.QWidget):
    #signals
    ##Used to send status message to the GUI
    send_status_msg = Signal(str, int)

    def __init__(self, camIndex):
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

        self.tab_index = 0
        
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

        # TODO: zeptat se na lambda

        # Recording
        self.line_edit_save_location.textChanged.connect(self.send_conf_update)
        self.line_edit_sequence_duration.textChanged.connect(self.send_conf_update)
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

    # TBD: nejsou presunuty funkce z camera_control_gui

    # Recording
    def setup_validators(self):
        """!@brief create input constrains for various widgets
        @details if a text widget needs certain input type, the validators are
        set up here. For example setting prohibited characters of the file saved. Not used yet!
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
        
        # TODO: zeptat se

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

        # TODO: zeptat se - pouze zapis do statusu?

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
    

# Camera

    # TODO: omylem odstraneno? pohledat v puvodnim projektu

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
        self.top_items = {}
        self.children_items = {}
        
        self.tree_features.clear()
        
        for name in self.feat_widgets:
            self.feat_widgets[name].deleteLater()
        
        for name in self.feat_labels:
            self.feat_labels[name].deleteLater()
        
        self.feat_widgets.clear()
        self.feat_labels.clear()
        
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
                    self.feat_widgets[param["name"]].activated.connect(lambda new_val,param=param: global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].set_parameter(param["name"],new_val+1))
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
        #called every 4 seconds
        if (self.feat_widgets and self.connected and self.tab_index == 1 and
            not(self.preview_live or self.recording) and 
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
        tries = 0
        while(tries <= 10):
            if(global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].get_parameters(params, 
                    threading.Event(), 
                    self.combo_config_level.currentIndex()+1)):
                break
            else:
                tries += 1
                
        if(tries >= 10):
            self.update_completed_flag.set()
            return
        
        while(not params.empty()):
            parameter = params.get()
            if(not(self.preview_live or self.recording) and 
               self.tab_index == 1):
                self.parameter_values[parameter["name"]] = parameter["attr_value"]
            else:
                self.update_completed_flag.set()
                return
        self.update_flag.set()
    
    def update_parameters(self):
        """!@brief Writes new values of the parameters to the GUI.
        @details After get_new_val_parameters finishes, the update_flag is set 
        and this method can transfer the new values of the parameters to the GUI. 
        Like start_refresh_parameters, this method is bound to the timer.
        """
        if (self.connected and not self.param_flag.is_set() and 
            self.tab_index == 1 and
            self.update_flag.is_set() and not(self.preview_live or self.recording)):
            
            self.update_flag.clear()
            
            for parameter in self.feat_widgets:
                try:
                    value = self.parameter_values[parameter]
                    widget = self.feat_widgets[parameter]
                    if(value == None):
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
            
            self.send_status_msg.emit("Reading features", 0)
            
            #empty feature queue
            self.get_params_thread = threading.Thread(
                target=global_camera.cams.active_devices[global_camera.active_cam[self.camIndex]].get_parameters,
                kwargs={'feature_queue': self.feat_queue,
                        'flag': self.param_flag,
                        'visibility': Config_level(self.combo_config_level.currentIndex()+1)})
            self.param_callback_thread = threading.Thread(target=self.callback_parameters)
            
            self.param_callback_thread.start().daemon = True
            self.get_params_thread.start().daemon = True

            self.param_callback_thread.start()
            self.get_params_thread.start()
    
    def save_cam_config(self):
        """!@brief Opens file dialog for user to select where to save camera 
        configuration.
        @details Called by Save configuration button. Configuration is saved 
        as an .xml file and its contents are dependent on module used in Camera 
        class to save the config.
        """
        
        if(self.connected):
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
                            self.send_status_msg.emit("Configuration loaded", 0)
                            return
                        else:
                            tries += 1
                    self.send_status_msg.emit("Loading failed", 2500)
            else:
                self.send_status_msg.emit("Stop recording and preview before loading config", 0)
        
    def callback_parameters(self):
        """!@brief Auxiliary method used to transfer thread state change into
        the main thread.
        """
        self.param_flag.wait()
        
        if(self.parameters_signal.text() != "A"):
            self.parameters_signal.setText("A")
        else:
            self.parameters_signal.setText("B")