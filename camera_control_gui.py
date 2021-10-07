from PyQt5 import QtCore, QtGui, QtWidgets
import global_camera
from PyQt5.QtCore import pyqtSignal as Signal, QRect
from PyQt5.QtGui import QPixmap
import threading
import win32api
import time

import global_camera
import global_queue

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
        self.scrollArea_1.setObjectName(u"scrollArea_1")
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_1.setObjectName(u"scrollAreaWidgetContents_1")
        self.scrollAreaWidgetContents_1.setGeometry(QRect(0, 0, 282, 352))
        self.camera_preview_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_1)
        self.camera_preview_1.setObjectName(u"camera_preview_1")
        self.camera_preview_1.setGeometry(QRect(10, 10, 261, 331))
        self.camera_preview_1.setAutoFillBackground(False)
        self.camera_preview_1.setPixmap(QPixmap(u"default_preview.png"))
        self.camera_preview_1.setScaledContents(False)
        self.camera_preview_1.setIndent(-1)
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)

        self.gridLayout_2.addWidget(self.scrollArea_1, 0, 0, 1, 1)

        self.scrollArea_2 = QtWidgets.QScrollArea(self)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 281, 352))
        self.camera_preview_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.camera_preview_2.setObjectName(u"camera_preview_2")
        self.camera_preview_2.setGeometry(QRect(10, 10, 261, 331))
        self.camera_preview_2.setAutoFillBackground(False)
        self.camera_preview_2.setPixmap(QPixmap(u"default_preview.png"))
        self.camera_preview_2.setScaledContents(False)
        self.camera_preview_2.setIndent(-1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_2.addWidget(self.scrollArea_2, 0, 1, 1, 1)

        self.scrollArea_3 = QtWidgets.QScrollArea(self)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 282, 351))
        self.camera_preview_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.camera_preview_3.setObjectName(u"camera_preview_3")
        self.camera_preview_3.setGeometry(QRect(10, 10, 261, 331))
        self.camera_preview_3.setAutoFillBackground(False)
        self.camera_preview_3.setPixmap(QPixmap(u"default_preview.png"))
        self.camera_preview_3.setScaledContents(False)
        self.camera_preview_3.setIndent(-1)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_2.addWidget(self.scrollArea_3, 1, 0, 1, 1)

        self.scrollArea_4 = QtWidgets.QScrollArea(self)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 281, 351))
        self.camera_preview_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.camera_preview_4.setObjectName(u"camera_preview_4")
        self.camera_preview_4.setGeometry(QRect(10, 10, 261, 331))
        self.camera_preview_4.setAutoFillBackground(False)
        self.camera_preview_4.setPixmap(QPixmap(u"default_preview.png"))
        self.camera_preview_4.setScaledContents(False)
        self.camera_preview_4.setIndent(-1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.gridLayout_2.addWidget(self.scrollArea_4, 1, 1, 1, 1)
    
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
   
    def update_recording_config(self, name, location, duration):
        """!@brief This method is used to tell the instance of this class current recording configuration
        @param[in] name Template for naming saved files
        @param[in] location Where should the images be saved
        @param[in] duration Length of a recording sequence
        """

        self.save_location = location
        self.save_filename = name
        self.sequence_duration = duration
    