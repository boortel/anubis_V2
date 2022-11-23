# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Preview_widget(object):
    def __init__(self, dialog, name):
        super(Preview_widget, self).__init__()
        self.name = name
        self.setupUi(dialog)
        self.connect_actions()
        
        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        self.preview_fit = False
        self.preview_zoom = 1
        self.w_preview_window = 0
        self.h_preview_window = 0

        #self.connect_actions()

    def setupUi(self, Form):
        Form.setObjectName(self.name)
        Form.resize(643, 465)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 623, 445))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout_2")
        self.label_preview = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_preview.setText("")
        self.label_preview.setObjectName("label_preview")
        self.horizontalLayout.addWidget(self.label_preview)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)


        self.ctl_zoom = QtWidgets.QGroupBox(Form)
        self.ctl_zoom.setObjectName(u"ctl_zoom")
        self.gridLayout = QtWidgets.QGridLayout(self.ctl_zoom)
        self.gridLayout.setObjectName(u"gridLayout_6")
        self.btn_zoom_in = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_in.setObjectName(u"btn_zoom_in")

        self.gridLayout.addWidget(self.btn_zoom_in, 0, 0, 1, 1)

        self.btn_zoom_out = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_out.setObjectName(u"btn_zoom_out")

        self.gridLayout.addWidget(self.btn_zoom_out, 0, 1, 1, 1)

        self.btn_zoom_fit = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_fit.setObjectName(u"btn_zoom_fit")

        self.gridLayout.addWidget(self.btn_zoom_fit, 1, 0, 1, 1)

        self.btn_zoom_100 = QtWidgets.QPushButton(self.ctl_zoom)
        self.btn_zoom_100.setObjectName(u"btn_zoom_100")

        self.gridLayout.addWidget(self.btn_zoom_100, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.ctl_zoom)

    def connect_actions(self):
        self.btn_zoom_out.clicked.connect(lambda: self.set_zoom(-1))
        self.btn_zoom_fit.clicked.connect(lambda: self.set_zoom(0))
        self.btn_zoom_in.clicked.connect(lambda: self.set_zoom(1))
        self.btn_zoom_100.clicked.connect(lambda: self.set_zoom(100))


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate(self.name, self.name))
        self.ctl_zoom.setTitle("")
        self.btn_zoom_in.setText("Zoom In")
        self.btn_zoom_out.setText("Zoom Out")
        self.btn_zoom_fit.setText("Fit to window")
        self.btn_zoom_100.setText("Zoom to 100%")

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

    def draw_image(self, image, width, height):
        if(self.preview_fit == True):

            self.w_preview_window = self.scrollArea.size().width()
            self.h_preview_window = self.scrollArea.size().height()
            image_scaled_window = image.scaled(self.w_preview_window, 
                                                self.h_preview_window, 
                                                QtCore.Qt.KeepAspectRatio)
        else:#else use zoom percentage
            self.w_preview_window = width*self.preview_zoom
            self.h_preview_window = height*self.preview_zoom
            image_scaled_window = image.scaled(self.w_preview_window,
                                        self.h_preview_window,
                                        QtCore.Qt.KeepAspectRatio)
        
        self.image_pixmap_window = QtGui.QPixmap.fromImage(image_scaled_window)

    def update(self):
        #Resize preview label if preview window size changed
        if(self.w_preview_window != self.label_preview.size().width() or
                   self.h_preview_window != self.label_preview.size().height()):
            self.label_preview.resize(self.w_preview_window,
                                            self.h_preview_window)
        
        #set a new image to the preview area
        self.label_preview.setPixmap(self.image_pixmap_window)
        self.label_preview.show()

    def reset(self):
        pass