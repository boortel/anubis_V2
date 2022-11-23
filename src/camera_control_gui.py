from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from src.preview_window import Preview_widget

class Camera_control_gui(QtWidgets.QWidget):

    def __init__(self):
        super(Camera_control_gui, self).__init__()

        self.preview_windows = [QtWidgets.QDialog(),QtWidgets.QDialog(),QtWidgets.QDialog(),QtWidgets.QDialog()]
        self.preview_widgets = [Preview_widget(self.preview_windows[0], "Camera 1"), 
                                Preview_widget(self.preview_windows[1], "Camera 2"), 
                                Preview_widget(self.preview_windows[2], "Camera 3"), 
                                Preview_widget(self.preview_windows[3], "Camera 4")]
        
        self.add_widgets()

    def add_widgets(self):

        self.setObjectName(u"preview_and_control")

        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.scrollAreas = [QtWidgets.QScrollArea(self), QtWidgets.QScrollArea(self), QtWidgets.QScrollArea(self), QtWidgets.QScrollArea(self)]
        for scrollArea in self.scrollAreas:
            scrollArea.installEventFilter(self)
            scrollArea.setWidgetResizable(True)
        
        self.camera_previews = [QtWidgets.QLabel(self.scrollAreas[0]), QtWidgets.QLabel(self.scrollAreas[1]), QtWidgets.QLabel(self.scrollAreas[2]), QtWidgets.QLabel(self.scrollAreas[3])]
        
        for camera_preview in self.camera_previews:
            camera_preview.setAutoFillBackground(False)
            camera_preview.setText("")
            camera_preview.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            camera_preview.setPixmap(QtGui.QPixmap("default_preview.png"))
            camera_preview.setScaledContents(False)
            camera_preview.setIndent(-1)
        
        self.camera_previews[0].setObjectName("camera_preview_1")
        self.camera_previews[1].setObjectName("camera_preview_2")
        self.camera_previews[2].setObjectName("camera_preview_3")
        self.camera_previews[3].setObjectName("camera_preview_4")
        self.scrollAreas[0].setWidget(self.camera_previews[0])
        self.scrollAreas[1].setWidget(self.camera_previews[1])
        self.scrollAreas[2].setWidget(self.camera_previews[2])
        self.scrollAreas[3].setWidget(self.camera_previews[3])

        self.gridLayout_2.addWidget(self.scrollAreas[0], 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.scrollAreas[1], 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.scrollAreas[2], 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.scrollAreas[3], 1, 1, 1, 1)
    
    def mouseDoubleClickEvent(self, event):
        widget = self.childAt(event.pos())
        if widget is not None and widget.objectName():
            if widget.objectName() == "camera_preview_1":
                self.preview_windows[0].show()
            elif widget.objectName() == "camera_preview_2":
                self.preview_windows[1].show()
            elif widget.objectName() == "camera_preview_3":
                self.preview_windows[2].show()
            elif widget.objectName() == "camera_preview_4":
                self.preview_windows[3].show()

    def update_recording_config(self, name, location, duration):
        """!@brief This method is used to tell the instance of this class current recording configuration
        @param[in] name Template for naming saved files
        @param[in] location Where should the images be saved
        @param[in] duration Length of a recording sequence
        """

        self.save_location = location
        self.save_filename = name
        self.sequence_duration = duration
    
