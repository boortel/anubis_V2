from PyQt5 import QtGui, QtWidgets


class HW_Control(QtWidgets.QGroupBox):
    def __init__(self):
        super(HW_Control, self).__init__()

        ##Holds image of running state
        self.icon_run = QtGui.QPixmap("./icons/icon_standby.png")
        ##Holds image of stopped of a camera
        self.icon_stop = QtGui.QPixmap("./icons/icon_busy.png")

        self.speed = 0
        self.direction = 0
        self.light1 = 0
        self.light2 = 0
        self.rotation_status = False
        self.light_status_1 = False
        self.light_status_2 = False

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
        self.gridLayout_HW.addWidget(self.btn_toggle_rotation, 2, 11, 1, 1)

        self.btn_change_direction = QtWidgets.QPushButton(self)
        self.btn_change_direction.setObjectName("btn_change_direction")
        self.gridLayout_HW.addWidget(self.btn_change_direction, 4, 11, 1, 1)

        self.label_light_control = QtWidgets.QLabel(self)
        self.label_light_control.setObjectName("label_light_control")
        self.gridLayout_HW.addWidget(self.label_light_control, 0, 1, 1, 1)

        self.dial_light_1 = QtWidgets.QDial(self)
        self.dial_light_1.setObjectName("dial_light_1")
        self.dial_light_1.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.dial_light_1, 1, 1, 2, 1)

        self.spinBox_light_1 = QtWidgets.QSpinBox(self)
        self.spinBox_light_1.setObjectName("spinBox_light_1")
        self.spinBox_light_1.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.spinBox_light_1, 1, 3, 1, 1)

        self.btn_toggle_light_1 = QtWidgets.QPushButton(self)
        self.btn_toggle_light_1.setObjectName("btn_toggle_light_1")
        self.gridLayout_HW.addWidget(self.btn_toggle_light_1, 2, 3, 1, 1)

        self.dial_speed = QtWidgets.QDial(self)
        self.dial_speed.setObjectName("dial_speed")
        self.dial_speed.setRange(self.speed_min, self.speed_max)
        self.gridLayout_HW.addWidget(self.dial_speed, 1, 10, 2, 1)

        self.label_speed_control = QtWidgets.QLabel(self)
        self.label_speed_control.setObjectName("label_speed_control")
        self.gridLayout_HW.addWidget(self.label_speed_control, 0, 10, 1, 1)

        self.spinBox_speed = QtWidgets.QSpinBox(self)
        self.spinBox_speed.setObjectName("spinBox_speed")
        self.spinBox_speed.setRange(self.speed_min, self.speed_max)
        self.gridLayout_HW.addWidget(self.spinBox_speed, 1, 11, 1, 1)


        

        self.btn_toggle_light_2 = QtWidgets.QPushButton(self)
        self.btn_toggle_light_2.setObjectName("btn_toggle_light_2")
        self.gridLayout_HW.addWidget(self.btn_toggle_light_2, 5, 3, 1, 1)

        self.spinBox_light_2 = QtWidgets.QSpinBox(self)
        self.spinBox_light_2.setObjectName("spinBox_light_2")
        self.spinBox_light_2.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.spinBox_light_2, 4, 3, 1, 1)

        self.dial_light_2 = QtWidgets.QDial(self)
        self.dial_light_2.setObjectName("dial_light_2")
        self.dial_light_2.setRange(self.light_min, self.light_max)
        self.gridLayout_HW.addWidget(self.dial_light_2, 4, 1, 2, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_HW.addItem(spacerItem, 1, 12, 1, 1)


#TODO replace with led
        self.icon_rotation = QtWidgets.QLabel(self)
        self.icon_rotation.setObjectName("icon_rotation")
        self.gridLayout_HW.addWidget(self.icon_rotation, 2, 12, 1, 1)

#TODO replace with led
        self.icon_light_1 = QtWidgets.QLabel(self)
        self.icon_light_1.setObjectName("icon_light_1")
        self.gridLayout_HW.addWidget(self.icon_light_1, 2, 4, 1, 1)

        self.icon_light_2 = QtWidgets.QLabel(self)
        self.icon_light_2.setObjectName("icon_light_2")
        self.gridLayout_HW.addWidget(self.icon_light_2, 5, 4, 1, 1)

    def connect_actions(self):
#TODO
        self.btn_toggle_light_1.clicked.connect(self.toggle_light_1)
        self.btn_toggle_light_2.clicked.connect(self.toggle_light_2)
        self.btn_toggle_rotation.clicked.connect(self.toggle_rotation)

        self.dial_light_1.valueChanged.connect(lambda: self.update_light_1(0))
        self.spinBox_light_1.valueChanged.connect(lambda: self.update_light_1(1))
        
        self.dial_light_2.valueChanged.connect(lambda: self.update_light_2(0))
        self.spinBox_light_2.valueChanged.connect(lambda: self.update_light_2(1))

        self.dial_speed.valueChanged.connect(lambda: self.update_speed(0))
        self.spinBox_speed.valueChanged.connect(lambda: self.update_speed(1))

        self.btn_change_direction.clicked.connect(self.change_direction)

    def set_texts(self):
        self.setTitle("HW control")
        self.btn_toggle_rotation.setText("Toggle Rotation")
        self.btn_change_direction.setText("Change Direction")
        self.label_light_control.setText("Light Control")
        self.btn_toggle_light_1.setText("Toggle Light 1")
        self.btn_toggle_light_2.setText("Toggle Light 2")
        self.label_speed_control.setText("Speed Control")
        
        self.icon_light_1.setPixmap(self.icon_stop)
        self.icon_light_2.setPixmap(self.icon_stop)
        self.icon_rotation.setPixmap(self.icon_stop)
    

    # ==============================================
    # Custom methods
    # ==============================================

    def toggle_light_2(self):
        if self.light_status_2:
            self.light_status_2 = False
            self.icon_light_2.setPixmap(self.icon_stop)
#TODO send_toggle_light OFF
        else:
            self.light_status_2 = True
            self.icon_light_2.setPixmap(self.icon_run)
#TODO send_toggle_light ON

    def toggle_light_1(self):
        if self.light_status_1:
            self.light_status_1 = False
            self.icon_light_1.setPixmap(self.icon_stop)
#TODO send_toggle_light OFF
        else:
            self.light_status_1 = True
            self.icon_light_1.setPixmap(self.icon_run)
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

    def update_light_1(self, source):
        if source == 0:
            self.light1 = self.dial_light_1.value()
            self.spinBox_light_1.setValue(self.light1)
        elif source == 1:
            self.light1 = self.spinBox_light_1.value()
            self.dial_light_1.setValue(self.light1)
#Maybe set new light level only when the spin box is not clicked
        if self.light_status_1:
            pass
#TODO send_light VAL

    def update_light_2(self, source):
        if source == 0:
            self.light2 = self.dial_light_2.value()
            self.spinBox_light_2.setValue(self.light2)
        elif source == 1:
            self.light2 = self.spinBox_light_2.value()
            self.dial_light_2.setValue(self.light2)

#Maybe set new light level only when the spin box is not clicked
        if self.light_status_2:
            pass
#TODO send_light VAL

    def change_direction(self):
        if self.direction == 0:
            self.direction = 1
#TODO send_direction 1
        else:
            self.direction = 1
#TODO send_direction 0


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



