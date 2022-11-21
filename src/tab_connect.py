from PyQt5 import QtGui, QtWidgets 
import src.global_camera as global_camera
from PyQt5.QtCore import pyqtSignal as Signal
import threading
import time

class Tab_connect(QtWidgets.QWidget):
    #signals
    ##Used to send status message to the GUI
    send_status_msg = Signal(str, int)
    ##Signals current state of camera connection
    connection_update = Signal(bool, int, str, int)#connected, state - 0=disconnected 1=standby 2=busy, camera name, camera tab index

    conntabList = [-1, -1, -1, -1]
    
    signal_toggle_controls = Signal(bool)
    signal_update_detected = Signal()

    def __init__(self):
        super(Tab_connect, self).__init__()

        self.connected = False
        self.connected_cams_names = {"0": "","1": "","2": "","3": ""}

        self.flag_updated = threading.Event()

        self.add_widgets()
        self.connect_actions()
        self.set_texts()
        

    def add_widgets(self):
        self.setObjectName("tab_connect")
        self.layout_main = QtWidgets.QVBoxLayout(self)
        self.layout_main.setObjectName("layout_main")
        self.widget_4 = QtWidgets.QWidget(self)
        self.widget_4.setObjectName("widget_4")
        self.layout_buttons = QtWidgets.QHBoxLayout(self.widget_4)
        self.layout_buttons.setObjectName("layout_buttons")
        self.btn_connect_camera = QtWidgets.QPushButton(self.widget_4)
        self.btn_connect_camera.setObjectName("btn_connect_camera")
        self.layout_buttons.addWidget(self.btn_connect_camera)
        self.btn_refresh_cameras = QtWidgets.QPushButton(self.widget_4)
        self.btn_refresh_cameras.setObjectName("btn_refresh_cameras")
        self.layout_buttons.addWidget(self.btn_refresh_cameras)
        self.btn_disconnect_camera = QtWidgets.QPushButton(self.widget_4)
        self.btn_disconnect_camera.setObjectName("btn_disconnect_camera")
        self.layout_buttons.addWidget(self.btn_disconnect_camera)
        self.layout_main.addWidget(self.widget_4)
        self.list_detected_cameras = QtWidgets.QListWidget(self)
        self.list_detected_cameras.setObjectName("list_detected_cameras")

        self.label_conn_tab = QtWidgets.QLabel(self.widget_4)
        self.label_conn_tab.setObjectName(u"label_conn_tab")
        self.layout_buttons.addWidget(self.label_conn_tab)

        self.combo_tab_selector = QtWidgets.QComboBox(self.widget_4)
        self.combo_tab_selector.addItem("Cam1")
        self.combo_tab_selector.addItem("Cam2")
        self.combo_tab_selector.addItem("Cam3")
        self.combo_tab_selector.addItem("Cam4")
        self.combo_tab_selector.setObjectName(u"combo_tab_selector")
        self.layout_buttons.addWidget(self.combo_tab_selector)
        
        self.layout_main.addWidget(self.list_detected_cameras)
        
        

    def connect_actions(self):
        self.btn_refresh_cameras.clicked.connect(self.refresh_cameras)
        
        self.btn_connect_camera.clicked.connect(self.create_connect_thread)
        
        self.list_detected_cameras.itemDoubleClicked.connect(self.create_connect_thread)
        #možná lambda s indexem itemu

        self.signal_update_detected.connect(self.refresh_cameras)
        
        self.btn_disconnect_camera.clicked.connect(self.create_disconnect_thread)
        self.signal_toggle_controls.connect(self.toggle_controls)

    def create_connect_thread(self):
        self.thread_conn = threading.Thread(target=self.connect_camera, args=(self.list_detected_cameras.currentRow(),))
        self.thread_conn.setDaemon(True)
        self.thread_conn.start()

    def create_disconnect_thread(self):
        self.thread_disconn = threading.Thread(target=self.disconnect_camera)
        self.thread_disconn.setDaemon(True)
        self.thread_disconn.start()

    def set_texts(self):
        self.btn_connect_camera.setText("Connect")
        self.btn_refresh_cameras.setText("Refresh")
        self.btn_disconnect_camera.setText("Disconnect")

        self.label_conn_tab.setText("Camera tab")
        self.combo_tab_selector.setItemText(0, "Camera 1")
        self.combo_tab_selector.setItemText(1, "Camera 2")
        self.combo_tab_selector.setItemText(2, "Camera 3")
        self.combo_tab_selector.setItemText(3, "Camera 4")
    
    def refresh_cameras(self):
        """!@brief Calls function to detect connected cameras and prints them
        as items in a list.
        @details If no cameras are present nothing will happen. If cameras are
        detected, all previous item are cleared and cameras detected in this call
        are printed.
        """
        #set status message
        self.send_status_msg.emit("Searching for cameras", 1500)
        
        #clear the list so the cameras won't appear twice or more
        self.list_detected_cameras.clear()
        
        #Get a list of cameras and inser each one to the interface as an 
        #entry in the list.
        self.detected = global_camera.cams.search_for_cameras()
        for index, device in enumerate(self.detected):
            output = device['mechanism'] + ': ' + device['model'] + device['id_']
#in the future maybe add icon based on interface type
            self.list_detected_cameras.addItem(output)
            if (device['mechanism'] + ': ' + device['model'] + device['id_']) in self.connected_cams_names.values():
                self.list_detected_cameras.item(index).setBackground(QtGui.QColor('#70BF4E'))
        
        self.flag_updated.set()
    
    def connect_camera(self, index):
        """!@brief Connect to selected camera
        @details This method is called either by double clicking camera in a 
        list or by pressing connect button
        @param[in] index index of selected camera in the list
        """
        #Something must be selected and the selected cam must not be already connected
        if index != -1 and self.list_detected_cameras.currentItem().text() not in self.connected_cams_names.values():
            self.signal_toggle_controls.emit(True)
            #If some camera is connected, disconnect it first
            if self.conntabList[self.combo_tab_selector.currentIndex()] == 1:
                self.disconnect_camera(toggle_controls=False)
            #Print status message
            self.send_status_msg.emit("Connecting camera", 0)

            #refresh cameras and undercolor connected
            self.connected_cams_names[str(self.combo_tab_selector.currentIndex())] = self.list_detected_cameras.item(index).text()
            self.flag_updated.clear()
            self.signal_update_detected.emit()
            self.flag_updated.wait()
            #Connect camera
            global_camera.change_active_cam(global_camera.cams.select_camera(self.detected[index]['mechanism'], self.detected[index]['id_']), self.combo_tab_selector.currentIndex())
            self.send_status_msg.emit("Camera connected", 0)

            #Set up the status bar
            self.conntabList[self.combo_tab_selector.currentIndex()] = 1
            self.connection_update.emit(True, 1, self.detected[index]['model'], self.combo_tab_selector.currentIndex())
            #Sleep to give camera time to initialize everything before user can use it
            time.sleep(1)
            self.signal_toggle_controls.emit(False)
    
    def disconnect_camera(self, toggle_controls=True):
        """!@brief Disconnect current camera
        @details Method disconnects camera and sets all statusbar items to 
        their default state.
        """
        #Disconnect only if already connected
        
        if self.conntabList[self.combo_tab_selector.currentIndex()] == 1:
            if(toggle_controls):
                self.signal_toggle_controls.emit(True)

            #Get default states
            self.connected = False
            
            self.send_status_msg.emit("Disconnecting camera", 0)
            
            #Disconnect camera
            global_camera.cams.disconnect_camera(int(global_camera.active_cam[self.combo_tab_selector.currentIndex()]))
            
            self.connection_update.emit(False, 0, "Not connected", self.combo_tab_selector.currentIndex())
            self.send_status_msg.emit("Camera disconnected", 0)

            #Mark current tab as free
            self.conntabList[self.combo_tab_selector.currentIndex()] = -1

            #Remove cam from list of connected cameras
            self.connected_cams_names[str(self.combo_tab_selector.currentIndex())] = ""
            

            if(toggle_controls):    
                #Imidiately search for new cameras 
                self.signal_update_detected.emit()    
                time.sleep(3)
                self.signal_toggle_controls.emit(False)
            else:
                time.sleep(3)


    def toggle_controls(self, disabled):
        self.btn_connect_camera.setDisabled(disabled)     
        self.btn_disconnect_camera.setDisabled(disabled)  
        self.btn_refresh_cameras.setDisabled(disabled)
        self.combo_tab_selector.setDisabled(disabled)      
        self.list_detected_cameras.setDisabled(disabled) 