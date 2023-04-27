#    Anubis is a program to control industrial cameras and train and use artificial neural networks
#    Copyright (C) 2021 Lukaszczyk Jakub
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.



from PyQt5 import QtCore, QtGui, QtWidgets
from src.tab_connect import Tab_connect
from src.tab_camera import Tab_camera
from src.tab_model import Tab_model
from src.tab_dataset import Tab_dataset
from src.hw_control_gui import HW_Control
from src.camera_control_gui import Camera_control_gui

import os
import webbrowser


import src.global_camera as global_camera


class Ui_MainWindow(QtCore.QObject):
    """!@brief Main class for user interface
    @details This file implements Ui_MainWindow class which defines the application's
    graphical user interface. Methods setupUi and retranslateUi are generated from
    QtDesigner using pyuic5 tool. When modifying the GUI these methods should be
    carefully edited with regards to calls at their ends which are used to bind
    methods to the widgets and initialize other variables.
    Methods in the class are mainly used to check some conditions and run methods
    of other connected classes like Camera and Computer_vision.
    """
    def __init__(self):
        """!@brief Initialize the class and all its variables
        """
        
        super(Ui_MainWindow,self).__init__()
     
        
        ##Is tensorflow model loaded
        self.model_loaded = False
 
        ##List of detected cameras
        self.detected = []
  
        ##State of recording
        self.recording = [False, False, False, False]
        ##State of live preview
        self.preview_live = [False, False, False, False]
        
        ##Holds image of offline state of a camera
        self.icon_offline = QtGui.QPixmap("./icons/icon_offline.png")
        ##Holds image of standby state of a camera
        self.icon_standby = QtGui.QPixmap("./icons/icon_standby.png")
        ##Holds image of busy state of a camera
        self.icon_busy = QtGui.QPixmap("./icons/icon_busy.png")
        
        ##Timer used to show a status messages for specific time window
        self.status_timer = QtCore.QTimer()

    def setupUi(self, MainWindow):
        """!@brief Create GUI widgets
        @details Excluding section marked as added manually, the whole 
        method is generated by pyuic5 tool and should not be modified otherwise
        because the changes are hard to track outside added manually section. 
        In this method all widgets, tabs, buttons etc. are created but not 
        named yet.
        """
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1206, 790)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #Definition of basic layout
        #----------------------------------------------------------------
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.preview_and_control = Camera_control_gui()

        self.gridLayout.addWidget(self.preview_and_control, 0, 2, 4, 1)        

        #Definition of all the tabs on the left side of the UI
        #--------------------------------------------------------------------
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setAccessibleName("")
        self.tabs.setAccessibleDescription("")
        self.tabs.setObjectName("tabs")
        
        #Tab - Connect camera
        self.tab_connect = Tab_connect()
        self.tabs.addTab(self.tab_connect, "")

        #Tab - Camera control
        self.tab_camera_cfg = []
        self.tab_camera_cfg.append(Tab_camera(0, 
                                    self.preview_and_control.camera_previews[0], 
                                    self.preview_and_control.preview_widgets[0]))
        self.tabs.addTab(self.tab_camera_cfg[0], "")

        self.tab_camera_cfg.append(Tab_camera(1, 
                                    self.preview_and_control.camera_previews[1],
                                    self.preview_and_control.preview_widgets[1]))
        self.tabs.addTab(self.tab_camera_cfg[1], "")

        self.tab_camera_cfg.append(Tab_camera(2, 
                                    self.preview_and_control.camera_previews[2],
                                    self.preview_and_control.preview_widgets[2]))
        self.tabs.addTab(self.tab_camera_cfg[2], "")

        self.tab_camera_cfg.append(Tab_camera(3, 
                                    self.preview_and_control.camera_previews[3],
                                    self.preview_and_control.preview_widgets[3]))
        self.tabs.addTab(self.tab_camera_cfg[3], "")

        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)
        
        self.gridLayout.addWidget(self.tabs, 0, 0, 2, 1)        
        
        #Tab - Dataset
        self.tab_dataset = Tab_dataset([self.tab_camera_cfg[0], 
                                self.tab_camera_cfg[1], 
                                self.tab_camera_cfg[2], 
                                self.tab_camera_cfg[3]])
        self.tabs.addTab(self.tab_dataset, "")

        
        #Tab - Model
        self.tab_model = Tab_model([self.tab_camera_cfg[0], 
                                self.tab_camera_cfg[1], 
                                self.tab_camera_cfg[2], 
                                self.tab_camera_cfg[3]])
        self.tabs.addTab(self.tab_model, "")



        #methods to call on tab change
        self.tabs.currentChanged.connect(self.tab_changed)
        
        #HW Control box
        #--------------------------------------------------------------------
        self.hw_control = HW_Control()
        self.gridLayout.addWidget(self.hw_control, 2, 0, 2, 1)

        #Menubar buttons
        #-------------------------------------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1208, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        
        #Define statusbar
        #------------------------------------------------
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        #self.statusGrid = QtWidgets.QGridLayout(self)
        #self.statusGrid.setObjectName("statusGrid")
        
        #added manually
        self.status_label = QtWidgets.QLabel()
        self.status_label.setObjectName("status_label")
        self.statusbar.addWidget(self.status_label,stretch=60)
         
        self.camera_icon = [None, None, None, None]
        self.camera_status = [None, None, None, None]
        self.fps_status = [None, None, None, None]
        self.receive_status = [None, None, None, None]

        for i in range(0,4):
            self.camera_icon[i] = QtWidgets.QLabel()
            self.camera_icon[i].setObjectName("camera_icon")
            self.camera_icon[i].setScaledContents(True)
            self.statusbar.addPermanentWidget(self.camera_icon[i])
            
            self.camera_status[i] = QtWidgets.QLabel()
            self.camera_status[i].setObjectName("camera_status")
            self.statusbar.addPermanentWidget(self.camera_status[i],stretch=20)
            
            self.fps_status[i] = QtWidgets.QLabel()
            self.fps_status[i].setObjectName("fps_status")
            self.statusbar.addPermanentWidget(self.fps_status[i],stretch=8)
            
            self.receive_status[i] = QtWidgets.QLabel()
            self.receive_status[i].setObjectName("receive_status")
            self.statusbar.addPermanentWidget(self.receive_status[i],stretch=15)
        
        
        MainWindow.setStatusBar(self.statusbar)
        
        #Adding individual items to menus in menubar
        #-------------------------------------------------------------
        
        self.actionOpen_Help = QtWidgets.QAction(MainWindow)
        self.actionOpen_Help.setObjectName("actionOpen_Help")
        
        
        self.action_save_frame = QtWidgets.QAction(MainWindow)
        self.action_save_frame.setObjectName("action_save_frame")
        
        self.actionAbout_Anubis = QtWidgets.QAction(MainWindow)
        self.actionAbout_Anubis.setObjectName("actionAbout_Anubis")
        
        self.actionGit_Repository = QtWidgets.QAction(MainWindow)
        self.actionGit_Repository.setObjectName("actionGit_Repository")
        
        self.actionSave_camera_config = QtWidgets.QAction(MainWindow)
        self.actionSave_camera_config.setObjectName("actionSave_camera_config")
        
        self.actionLoad_camera_config = QtWidgets.QAction(MainWindow)
        self.actionLoad_camera_config.setObjectName("actionLoad_camera_config")
        
        self.menuFile.addAction(self.actionSave_camera_config)
        self.menuFile.addAction(self.actionLoad_camera_config)
        
        self.menuFile.addSeparator()
        
        self.menuHelp.addAction(self.actionOpen_Help)
        
        self.menuHelp.addSeparator()
        
        self.menuHelp.addAction(self.actionAbout_Anubis)
        self.menuHelp.addAction(self.actionGit_Repository)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        #----------------------------------------------------------------
        
        #--------------------------------------------------------------
        
        self.setup_validators()
        self.connect_actions()
        self.retranslateUi(MainWindow)
        self.read_config()
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    
    def retranslateUi(self, MainWindow):
        """!@brief Sets names of widgets.
        @details Widgets are created in setupUi method, this method sets text
        of the buttons, tabs and default texts for all of these widgets.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anubis"))

        self.tabs.setTabText(self.tabs.indexOf(self.tab_connect), _translate("MainWindow", "Connect Camera"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_camera_cfg[0]), _translate("MainWindow", "Camera 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_camera_cfg[1]), _translate("MainWindow", "Camera 2"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_camera_cfg[2]), _translate("MainWindow", "Camera 3"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_camera_cfg[3]), _translate("MainWindow", "Camera 4"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_dataset), _translate("MainWindow", "Dataset"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_model), _translate("MainWindow", "Model"))
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_Help.setText(_translate("MainWindow", "Open Help"))
        self.action_save_frame.setText(_translate("MainWindow", "Save frame"))
        self.actionAbout_Anubis.setText(_translate("MainWindow", "About Anubis"))
        self.actionGit_Repository.setText(_translate("MainWindow", "Git Repository"))
        self.actionSave_camera_config.setText(_translate("MainWindow", "Save camera config"))
        self.actionLoad_camera_config.setText(_translate("MainWindow", "Load camera config"))
        
        #added manually

        for i in range(0,4):
            self.camera_status[i].setText("Cam1: Not connected")
            self.receive_status[i].setText("Received frames: 0")
            self.fps_status[i].setText("FPS: 0")
            self.camera_icon[i].setPixmap(self.icon_offline)
    
#Start of custom methods (not generated by QtDesigner)
    def connect_actions(self):

        """!@brief Connect method calls to appropriate widgets
        @details All static widgets are connected to some method either in this
        class or call method of another object. In this method all such bindings
        done excluding dynamically created widgets like camera's features
        """
        #CONNECTING TAB
        self.tab_connect.send_status_msg.connect(self.set_status_msg)
        self.tab_connect.connection_update.connect(self.update_camera_status)
        self.status_timer.timeout.connect(self.clear_status)

        #CAMERA TAB
        for tab in range(0,4):
            self.tab_camera_cfg[tab].send_status_msg.connect(self.set_status_msg)
            self.tab_camera_cfg[tab].preview_update.connect(self.update_preview)
            self.tab_camera_cfg[tab].connection_update.connect(self.update_camera_status)
            self.tab_camera_cfg[tab].send_status_msg.connect(self.set_status_msg)
            self.tab_camera_cfg[tab].recording_update.connect(self.update_recording)
            self.tab_camera_cfg[tab].fps_info.connect(self.update_fps)
            self.tab_camera_cfg[tab].received_info.connect(self.update_received_frames)
            self.tab_camera_cfg[tab].signal_update_parameters.connect(self.tab_camera_cfg[tab].update_parameters)
        
            self.tab_camera_cfg[tab].signal_show_parameters.connect(self.tab_camera_cfg[tab].show_parameters)
            self.tab_camera_cfg[tab].signal_clear_parameters.connect(self.tab_camera_cfg[tab].clear_parameters)
    
        #DATASET TAB

        #MENU ACTIONS
        self.actionOpen_Help.triggered.connect(lambda: 
                            webbrowser.open(
                                os.path.dirname(os.path.realpath(__file__)) + 
                                "/Help//index.html",
                                new=2))
        self.actionGit_Repository.triggered.connect(lambda: 
                            webbrowser.open("https://github.com/xlukas10/anubis",new=2))
        self.actionAbout_Anubis.triggered.connect(self.about)
    
    def setup_validators(self):
        """!@brief create input constrains for various widgets
        @details if a text widget needs certain input type, the validators are
        set up here. For example setting prohibited characters of the file saved.
        """
        pass    
    
#-----------Common methods--------------------    
    def tab_changed(self):
        """!@brief Called when tab changes and with the Qt timer
        @details Used to do actions when entering specific tab.
        """
        index = self.tabs.currentIndex()
        
        if index == 0:
            pass
        if index == 1:#Camera 1 tab
            #Request parameters from camera and show them in gui
            self.tab_camera_cfg[0].show_parameters()
        if index == 2:#Camera 2 tab
            #Request parameters from camera and show them in gui
            self.tab_camera_cfg[1].show_parameters()
        if index == 3:#Camera 3 tab
            #Request parameters from camera and show them in gui
            self.tab_camera_cfg[2].show_parameters()
        if index == 4:#Camera 4 tab
            #Request parameters from camera and show them in gui
            self.tab_camera_cfg[3].show_parameters()
    
    def set_status_msg(self, message, timeout=0):
        """!@brief Shows message in status bar
        @details Method is called when other methods need to send the user 
        some confrimation or status update.
        @param[in] message Contains text to be displayed in the status bar
        @param[in] timeout For how long should the message be displayed [ms]. Defaults to infinity.
        """
        self.status_timer.stop()
        self.status_label.setText(message)
        #When time out is reached, connected method 
        #(self.clear_status) is called.
        if(timeout > 0):
            self.status_timer.start(timeout)
    
    def clear_status(self):
        """!@brief Empties self.status_label in self.statusbar.
        @details Method is called after active message times out.
        """
        self.status_label.setText("")
    
    def get_directory(self, line_output = None):
        #set_record_path
        """!@brief Opens file dialog for user to set path to save frames.
        @details Method is called by Save Location button. Path is written to 
        the label next to the button and can be further modified.
        """
        #Open file dialog for choosing a folder
        name = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget,
                                                     "Select Folder",
                                                     )
        
        #Set label text to chosen folder path
        if(line_output):
            line_output.setText(name)
        return name
    
    def read_config(self):
        """!@brief Loads configuration from config.ini file
        @details This method is called on startup and loads all modifications
        user made to applications default state.                                 
        """
        
        filename = None,
        save_location = None,
        sequence_duration = None
        
        for tab_i in range(0,4):
            with open("config.ini", 'r') as config:
                for line in config:
                    #reading configuration for recording
                    line = line.rstrip('\n')
                    if(line.startswith(f"filename{tab_i}=")):
                        filename = line.replace(f"filename{tab_i}=", "", 1)
                        #self.line_edit_sequence_name.setText(line.replace("filename=", "", 1))
                    elif(line.startswith(f"save_location{tab_i}=")):
                        save_location = line.replace(f"save_location{tab_i}=", "", 1)
                        #self.line_edit_save_location.setText(line.replace("save_location=", "", 1))
                    elif(line.startswith(f"sequence_duration{tab_i}=")):
                        sequence_duration = line.replace(f"sequence_duration{tab_i}=", "", 1)
                        sequence_duration = float(sequence_duration.replace(",","."))
                        #self.line_edit_sequence_duration.setText(line.replace("sequence_duration=", "", 1))
            
            self.tab_camera_cfg[tab_i].load_config(filename, save_location, sequence_duration)        
        #Set status update
        self.set_status_msg("Configuration loaded",1500)
        
    def about(self):
        """!@brief Shows simple about dialog
        @details About dialog contains informations about version, author etc.
        """
        QtWidgets.QMessageBox.about(self.centralwidget, "About", 
                                    "<p>Author: Jakub Lukaszczyk, Simon Bilik</p>" +
                                    "<p>Version: 1.1</p>" + 
                                    "<p>Original release: 2021</p>" +
                                    "<p>Gui created using Qt</p>")

    def  update_camera_status(self, connected, state, name, tab):
        """!@brief Updates camera status variables and status bar
        @details This method is called when tab_connect sends its update signal.
        The method will change camera state icons and name. If the camera is being 
        disconnected, the fps and received frames will be reseted.
        @param[in] connected The new status of camera (connected or disconnected)
        @param[in] state Numeric state of the camera (0=disconnected, 1=standby, 2=busy)
        @param[in] name Connected camera name. If the camera is being disconnected
        the name is "Not connected", if name shouldn't be updated, pass in "-1"
        @param[in] tab index of connected camera (0 - 3)
        """
        self.tabs.setTabEnabled(tab+1, connected)

        if(self.tab_camera_cfg[tab].connected == False and connected == True):
            self.tab_camera_cfg[tab].connected = connected
            self.tab_camera_cfg[tab].start_auto_refresh()  
        elif(self.tab_camera_cfg[tab].connected == True and connected == False):
            self.tab_camera_cfg[tab].connected = connected
            self.tab_camera_cfg[tab].thread_reset.start()

        self.tab_camera_cfg[tab].connected = connected

        if name != "-1":
            self.camera_status[tab].setText("Camera: " + name)
            
        if(state == 1):
            self.camera_icon[tab].setPixmap(self.icon_standby)
        elif(state == 2):
            self.camera_icon[tab].setPixmap(self.icon_busy)
        else:
            self.camera_icon[tab].setPixmap(self.icon_offline)

            self.update_preview(False, tab)
            self.update_recording(False, tab)
            self.update_fps(0, tab)
            self.update_received_frames(0, tab)              
        
        #Update dataset tab checkboxes
        self.tab_dataset.checkbox_enabler()

    def update_preview(self, state, tab):
        """!@brief Method is used to transfer information about preview 
        state to other objects (mostly tabs)
        @param[in] state Tells whether the preview is active or not
        """
        self.tab_camera_cfg[tab].preview_live = state
        self.preview_live[tab] = state
    
    def update_recording(self, state, tab):
        """!@brief Method is used to transfer information about recording 
        state to other objects (mostly tabs)
        @param[in] state Tells whether the recording is active or not
        """

        self.tab_camera_cfg[tab].recording = state
        self.recording[tab] = state

    def update_fps(self, fps, tab):
        """!@brief Method is used to transfer information from camera preview object
        to the status bar
        @param[in] fps Current fps value
        """
        self.fps = fps

        self.fps_status[tab].setText("FPS: " + str(self.fps))

    def update_received_frames(self, received_amount, tab):
        """!@brief Method is used to transfer information from camera preview object
        to the status bar
        @param[in] received_amount How many frames were received
        """
        self.received = received_amount

        self.receive_status[tab].setText("Received frames: " + str(self.received))

    def update_recording_config(self, name, location, duration):
        """!@brief Method is used to transfer information from recording configuration
        tab to the active camera
        @param[in] name Template for naming saved files
        @param[in] location Where should the images be saved
        @param[in] duration Length of a recording sequence
        """
        self.preview_and_control.update_recording_config(name, location, duration)
