from PyQt5 import QtGui, QtWidgets


class HW_Control(QtWidgets.QGroupBox):
    def __init__(self):
        super(HW_Control, self).__init__()

        ##Holds image of running state
        self.icon_run = QtGui.QPixmap("./icons/icon_standby.png")
        ##Holds image of stopped of a camera
        self.icon_stop = QtGui.QPixmap("./icons/icon_busy.png")

        self.speed = 0.0
        self.light = 0.0
        self.rotation_status = False
        self.light_status = False

        self.speed_min = 0
        self.speed_max = 100
        self.light_min = 0
        self.light_max = 100

        self.add_widgets()
        self.connect_actions()
        self.set_texts()

    def add_widgets(self):
        self.setObjectName(u"hw_control")

        self.gridLayout_HW = QtWidgets.QGridLayout(self)
        self.gridLayout_HW.setObjectName("gridLayout_HW")

        self.btn_toggle_rotation = QtWidgets.QPushButton(self)
        self.btn_toggle_rotation.setObjectName("btn_toggle_rotation")
        self.gridLayout_HW.addWidget(self.btn_toggle_rotation, 2, 5, 1, 1)

        self.label_light_control = QtWidgets.QLabel(self)
        self.label_light_control.setObjectName("label_light_control")
        self.gridLayout_HW.addWidget(self.label_light_control, 0, 1, 1, 1)

        self.dial_light = QtWidgets.QDial(self)
        self.dial_light.setObjectName("dial_light")
        self.dial_light.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.dial_light, 1, 1, 2, 1)

        self.spinBox_light = QtWidgets.QSpinBox(self)
        self.spinBox_light.setObjectName("spinBox_light")
        self.spinBox_light.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.spinBox_light, 1, 2, 1, 1)

        self.btn_toggle_light = QtWidgets.QPushButton(self)
        self.btn_toggle_light.setObjectName("btn_toggle_light")
        self.gridLayout_HW.addWidget(self.btn_toggle_light, 2, 2, 1, 1)

        self.dial_speed = QtWidgets.QDial(self)
        self.dial_speed.setObjectName("dial_speed")
        self.dial_speed.setRange(self.speed_min, self.speed_max)
        self.gridLayout_HW.addWidget(self.dial_speed, 1, 4, 2, 1)

        self.label_speed_control = QtWidgets.QLabel(self)
        self.label_speed_control.setObjectName("label_speed_control")
        self.gridLayout_HW.addWidget(self.label_speed_control, 0, 4, 1, 1)

        self.spinBox_speed = QtWidgets.QSpinBox(self)
        self.spinBox_speed.setObjectName("spinBox_speed")
        self.spinBox_speed.setRange(self.speed_min, self.speed_max)
        self.gridLayout_HW.addWidget(self.spinBox_speed, 1, 5, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_HW.addItem(spacerItem, 1, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_HW.addItem(spacerItem1, 1, 6, 1, 1)


#TODO replace with led
        self.icon_rotation = QtWidgets.QLabel(self)
        self.icon_rotation.setObjectName("icon_rotation")
        self.gridLayout_HW.addWidget(self.icon_rotation, 2, 6, 1, 1)

#TODO replace with led
        self.icon_light = QtWidgets.QLabel(self)
        self.icon_light.setObjectName("icon_light")
        self.gridLayout_HW.addWidget(self.icon_light, 2, 3, 1, 1)

    def connect_actions(self):
#TODO
        self.btn_toggle_light.clicked.connect(self.toggle_light)
        self.btn_toggle_rotation.clicked.connect(self.toggle_rotation)

        self.dial_light.valueChanged.connect(lambda: self.update_light(0))
        self.spinBox_light.valueChanged.connect(lambda: self.update_light(1))

        self.dial_speed.valueChanged.connect(lambda: self.update_speed(0))
        self.spinBox_speed.valueChanged.connect(lambda: self.update_speed(1))

    def set_texts(self):
        self.setTitle("HW control")
        self.btn_toggle_rotation.setText("Toggle rotation")
        self.label_light_control.setText("Light control")
        self.btn_toggle_light.setText("Toggle light")
        self.label_speed_control.setText("Speed control")
        
        self.icon_light.setPixmap(self.icon_stop)
        self.icon_rotation.setPixmap(self.icon_stop)
    

    # ==============================================
    # Custom methods
    # ==============================================

    def toggle_light(self):
        if self.light_status:
            self.light_status = False
            self.icon_light.setPixmap(self.icon_stop)
#TODO send_toggle_light OFF
        else:
            self.light_status = True
            self.icon_light.setPixmap(self.icon_run)
#TODO send_toggle_light ON

    def toggle_rotation(self):
        if self.rotation_status:
            self.rotation_status = False
            self.icon_rotation.setPixmap(self.icon_stop)
#TODO send_toggle_light OFF
        else:
            self.rotation_status = True
            self.icon_rotation.setPixmap(self.icon_run)
#TODO send_toggle_light ON

    def update_light(self, source):
        if source == 0:
            self.light = self.dial_light.value()
            self.spinBox_light.setValue(self.light)
        elif source == 1:
            self.light = self.spinBox_light.value()
            self.dial_light.setValue(self.light)

#Maybe set new light level only when the spin box is not clicked
        if self.light_status:
            pass
#TODO send_light VAL

    def update_speed(self, source):
        if source == 0:
            self.speed = self.dial_speed.value()
            self.spinBox_speed.setValue(self.speed)
        elif source == 1:
            self.speed = self.spinBox_speed.value()
            self.dial_speed.setValue(self.speed)

#Maybe set new speed only when the spin box is not clicked
        if self.rotation_status:
            pass
#TODO send_speed VAL



