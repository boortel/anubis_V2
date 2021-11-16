from PyQt5 import QtGui, QtWidgets

class Camera_control_gui(QtWidgets.QWidget):

    def __init__(self):
        super(Camera_control_gui, self).__init__()

        self.add_widgets()

    def add_widgets(self):
        #self.preview_and_control = QtWidgets.QWidget(self)
        self.setObjectName(u"preview_and_control")

        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.scrollArea_1 = QtWidgets.QScrollArea(self)
        self.scrollArea_1.installEventFilter(self)
        self.scrollArea_1.setWidgetResizable(True)
        
        self.camera_preview_1 = QtWidgets.QLabel(self.scrollArea_1)
        self.camera_preview_1.setAutoFillBackground(False)
        self.camera_preview_1.setText("")
        self.camera_preview_1.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.camera_preview_1.setPixmap(QtGui.QPixmap("default_preview.png"))
        self.camera_preview_1.setScaledContents(False)
        self.camera_preview_1.setIndent(-1)
        self.camera_preview_1.setObjectName("camera_preview_1")
        self.scrollArea_1.setWidget(self.camera_preview_1)

        #self.scrollArea_1 = QtWidgets.QScrollArea(self)
        #self.scrollArea_1.setObjectName(u"scrollArea_1")
        #self.scrollArea_1.setWidgetResizable(True)
        #self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        #self.scrollAreaWidgetContents_1.setObjectName(u"scrollAreaWidgetContents_1")
        #self.scrollAreaWidgetContents_1.setGeometry(QRect(0, 0, 282, 352))

        #self.camera_preview_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_1)
        #self.camera_preview_1.setObjectName(u"camera_preview_1")
        #self.camera_preview_1.setGeometry(QRect(10, 10, 261, 331))
        #self.camera_preview_1.setAutoFillBackground(False)
        #self.camera_preview_1.setPixmap(QPixmap(u"default_preview.png"))
        #self.camera_preview_1.setScaledContents(False)
        #self.camera_preview_1.setIndent(-1)
        #self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)

        self.gridLayout_2.addWidget(self.scrollArea_1, 0, 0, 1, 1)

        self.scrollArea_2 = QtWidgets.QScrollArea(self)
        self.scrollArea_2.installEventFilter(self)
        self.scrollArea_2.setWidgetResizable(True)
        
        self.camera_preview_2 = QtWidgets.QLabel(self.scrollArea_2)
        self.camera_preview_2.setAutoFillBackground(False)
        self.camera_preview_2.setText("")
        self.camera_preview_2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.camera_preview_2.setPixmap(QtGui.QPixmap("default_preview.png"))
        self.camera_preview_2.setScaledContents(False)
        self.camera_preview_2.setIndent(-1)
        self.camera_preview_2.setObjectName("camera_preview_1")
        self.scrollArea_2.setWidget(self.camera_preview_2)

        self.gridLayout_2.addWidget(self.scrollArea_2, 0, 1, 1, 1)

        self.scrollArea_3 = QtWidgets.QScrollArea(self)
        self.scrollArea_3.installEventFilter(self)
        self.scrollArea_3.setWidgetResizable(True)
        
        self.camera_preview_3 = QtWidgets.QLabel(self.scrollArea_3)
        self.camera_preview_3.setAutoFillBackground(False)
        self.camera_preview_3.setText("")
        self.camera_preview_3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.camera_preview_3.setPixmap(QtGui.QPixmap("default_preview.png"))
        self.camera_preview_3.setScaledContents(False)
        self.camera_preview_3.setIndent(-1)
        self.camera_preview_3.setObjectName("camera_preview_1")
        self.scrollArea_3.setWidget(self.camera_preview_3)

        self.gridLayout_2.addWidget(self.scrollArea_3, 1, 0, 1, 1)

        self.scrollArea_4 = QtWidgets.QScrollArea(self)
        self.scrollArea_4.installEventFilter(self)
        self.scrollArea_4.setWidgetResizable(True)
        
        self.camera_preview_4 = QtWidgets.QLabel(self.scrollArea_4)
        self.camera_preview_4.setAutoFillBackground(False)
        self.camera_preview_4.setText("")
        self.camera_preview_4.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.camera_preview_4.setPixmap(QtGui.QPixmap("default_preview.png"))
        self.camera_preview_4.setScaledContents(False)
        self.camera_preview_4.setIndent(-1)
        self.camera_preview_4.setObjectName("camera_preview_1")
        self.scrollArea_4.setWidget(self.camera_preview_4)

        self.gridLayout_2.addWidget(self.scrollArea_4, 1, 1, 1, 1)
   
    def update_recording_config(self, name, location, duration):
        """!@brief This method is used to tell the instance of this class current recording configuration
        @param[in] name Template for naming saved files
        @param[in] location Where should the images be saved
        @param[in] duration Length of a recording sequence
        """

        self.save_location = location
        self.save_filename = name
        self.sequence_duration = duration
    
