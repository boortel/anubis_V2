from PyQt5 import QtGui, QtWidgets


class HW_Control(QtWidgets.QGroupBox):
    def __init__(self):
        super(HW_Control, self).__init__()

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

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout_HW.addWidget(self.label, 0, 1, 1, 1)

        self.dial_light = QtWidgets.QDial(self)
        self.dial_light.setObjectName("dial_light")
        self.gridLayout_HW.addWidget(self.dial_light, 1, 1, 2, 1)

        self.doubleSpinBox_light = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_light.setObjectName("doubleSpinBox_light")
        self.gridLayout_HW.addWidget(self.doubleSpinBox_light, 1, 2, 1, 1)

        self.btn_toggle_light = QtWidgets.QPushButton(self)
        self.btn_toggle_light.setObjectName("btn_toggle_light")
        self.gridLayout_HW.addWidget(self.btn_toggle_light, 2, 2, 1, 1)

        self.dial_speed = QtWidgets.QDial(self)
        self.dial_speed.setObjectName("dial_speed")
        self.gridLayout_HW.addWidget(self.dial_speed, 1, 4, 2, 1)

        self.label_speed_control = QtWidgets.QLabel(self)
        self.label_speed_control.setObjectName("label_speed_control")
        self.gridLayout_HW.addWidget(self.label_speed_control, 0, 4, 1, 1)

        self.doubleSpinBox_speed = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_speed.setObjectName("doubleSpinBox_speed")
        self.gridLayout_HW.addWidget(self.doubleSpinBox_speed, 1, 5, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_HW.addItem(spacerItem, 1, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_HW.addItem(spacerItem1, 1, 6, 1, 1)


#TODO replace with led
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.gridLayout_HW.addWidget(self.label_3, 2, 3, 1, 1)

#TODO replace with led
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.gridLayout_HW.addWidget(self.label_4, 2, 6, 1, 1)

    def connect_actions(self):
#TODO
        self.btn_toggle_light.clicked.connect(self.toggle_light)
        self.btn_toggle_rotation.clicked.connect(self.toggle_rotation)

    def set_texts(self):
        self.setTitle("HW control")
        self.btn_toggle_rotation.setText("Toggle rotation")
        self.label.setText("Light control")
        self.btn_toggle_light.setText("Toggle light")
        self.label_speed_control.setText("Speed control")
        
        self.label_3.setText("REPL_WITH_LED")
        self.label_4.setText("REPL_WITH_LED")
    

    # ==============================================
    # Custom methods
    # ==============================================

    def toggle_light(self):
        pass

    def toggle_rotation(self):
        pass