from PyQt5 import QtCore, QtWidgets, QtGui
import src.global_camera as global_camera
import os

class Tab_model(QtWidgets.QWidget):
    def __init__(self, camera_tabs = []):
        super(Tab_model, self).__init__()
        self.camera_tabs = camera_tabs
        self.model_folder = "svdd_anubis/models"
        self.add_widgets()
        self.connect_actions()
        self.set_texts()


    def add_widgets(self):
        self.tab_dataset = QtWidgets.QWidget()
        self.tab_dataset.setObjectName("tab_dataset")
        self.gridLayout_4 = QtWidgets.QGridLayout(self)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.label_threshold = QtWidgets.QLabel(self)
        self.label_threshold.setObjectName("label_threshold")
        self.gridLayout_4.addWidget(self.label_threshold,0,2,1,1)

        
        self.label_scores = QtWidgets.QLabel(self)
        self.label_scores.setObjectName("label_scores")
        self.gridLayout_4.addWidget(self.label_scores,5,0,1,1)

        self.label_predict = QtWidgets.QLabel(self)
        self.label_predict.setObjectName("label_predict")
        self.gridLayout_4.addWidget(self.label_predict,0,3,1,1)
        self.checkBox_cameras = [None,None,None,None]


        self.checkBox_cameras[0] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[0].setObjectName("checkBox_camera1")
        self.gridLayout_4.addWidget(self.checkBox_cameras[0], 1, 3, 1, 1)

        self.checkBox_cameras[1] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[1].setObjectName("checkBox_camera2")
        self.gridLayout_4.addWidget(self.checkBox_cameras[1], 2, 3, 1, 1)

        self.checkBox_cameras[2] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[2].setObjectName("checkBox_camera3")
        self.gridLayout_4.addWidget(self.checkBox_cameras[2], 3, 3, 1, 1)
        
        self.checkBox_cameras[3] = QtWidgets.QCheckBox(self)
        self.checkBox_cameras[3].setObjectName("checkBox_camera4")
        self.gridLayout_4.addWidget(self.checkBox_cameras[3], 4, 3, 1, 1)

        self.labels_cameras = [None,None,None,None]
        self.combo_boxes_model = [None,None,None,None]

        i = 0
        for l in self.labels_cameras:
            label = QtWidgets.QLabel(self)
            label.setObjectName(f"label_camera{i}")
            self.gridLayout_4.addWidget(label, i+1 , 0,1,1)
            label.setText(f"Camera {i+1}")
            self.labels_cameras[i] = label
            i += 1

        i = 0
        
        models_available = [name for name in os.listdir(self.model_folder) if os.path.isdir(os.path.join(self.model_folder, name))]
        for c in self.combo_boxes_model:
            combo_box = QtWidgets.QComboBox(self)
            combo_box.setObjectName(f"combo_box{i}")
            combo_box.addItems(models_available)
            self.gridLayout_4.addWidget(combo_box, i+1 , 1,1,1)
            self.combo_boxes_model[i] = combo_box
            #label.setText(f"Camera {i}")
            i += 1
        
        self.double_spin_boxes = [None,None,None,None]
        i = 0
        for l in self.double_spin_boxes:
            spin_box = QtWidgets.QDoubleSpinBox(self)
            spin_box.setObjectName(f"spin_box{i}")
            self.gridLayout_4.addWidget(spin_box, i+1 , 2,1,1)
            spin_box.setMaximum(1000000000)
            spin_box.setValue(1000)
            spin_box.setMinimum(0)
            self.double_spin_boxes[i] = spin_box
            i += 1

        self.labels_scores = [None, None, None, None]
        self.labels_score_name = [None, None, None, None]
        i = 0
        for l in self.labels_scores:
            label = QtWidgets.QLabel(self)
            label.setObjectName(f"label_score_name_{i}")
            self.gridLayout_4.addWidget(label, 6, i,1,1)
            label.setText(f"Camera {i+1}")
            self.labels_score_name[i] = label

            
            label2 = QtWidgets.QLabel(self)
            label2.setObjectName(f"label_score_{i}")
            self.gridLayout_4.addWidget(label2, 7, i,1,1)
            label2.setText(f"0")
            
            self.labels_scores[i] = label2
            i += 1

        self.camera_tabs[0].imp.setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[0].currentText()))
        self.camera_tabs[1].imp.setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[1].currentText()))
        self.camera_tabs[2].imp.setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[2].currentText()))
        self.camera_tabs[3].imp.setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[3].currentText()))
        
        self.gridLayout_4.addItem(QtWidgets.QSpacerItem(20,40,QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
        
    def connect_actions(self):
        self.camera_tabs[0].signal_processing.connect(lambda value: self.checkBox_cameras[0].setChecked(value))
        self.camera_tabs[1].signal_processing.connect(lambda value: self.checkBox_cameras[1].setChecked(value))
        self.camera_tabs[2].signal_processing.connect(lambda value: self.checkBox_cameras[2].setChecked(value))
        self.camera_tabs[3].signal_processing.connect(lambda value: self.checkBox_cameras[3].setChecked(value))
        self.checkBox_cameras[0].clicked.connect(lambda: self.camera_tabs[0].toggle_processing())
        self.checkBox_cameras[1].clicked.connect(lambda: self.camera_tabs[1].toggle_processing())
        self.checkBox_cameras[2].clicked.connect(lambda: self.camera_tabs[2].toggle_processing())
        self.checkBox_cameras[3].clicked.connect(lambda: self.camera_tabs[3].toggle_processing())

        
        self.checkBox_cameras[0].stateChanged.connect(lambda: self.combo_boxes_model[0].setDisabled(self.checkBox_cameras[0].isChecked()))
        self.checkBox_cameras[1].stateChanged.connect(lambda: self.combo_boxes_model[1].setDisabled(self.checkBox_cameras[1].isChecked()))
        self.checkBox_cameras[2].stateChanged.connect(lambda: self.combo_boxes_model[2].setDisabled(self.checkBox_cameras[2].isChecked()))
        self.checkBox_cameras[3].stateChanged.connect(lambda: self.combo_boxes_model[3].setDisabled(self.checkBox_cameras[3].isChecked()))

        self.combo_boxes_model[0].currentIndexChanged.connect(lambda: self.camera_tabs[0].setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[0].currentText())))
        self.combo_boxes_model[1].currentIndexChanged.connect(lambda: self.camera_tabs[1].setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[1].currentText())))
        self.combo_boxes_model[2].currentIndexChanged.connect(lambda: self.camera_tabs[2].setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[2].currentText())))
        self.combo_boxes_model[3].currentIndexChanged.connect(lambda: self.camera_tabs[3].setup_image_process(os.path.join(self.model_folder, self.combo_boxes_model[3].currentText())))
        self.double_spin_boxes[0].valueChanged.connect(lambda: self.camera_tabs[0].imp.change_threshold(self.double_spin_boxes[0].value()))
        self.double_spin_boxes[1].valueChanged.connect(lambda: self.camera_tabs[1].imp.change_threshold(self.double_spin_boxes[1].value()))
        self.double_spin_boxes[2].valueChanged.connect(lambda: self.camera_tabs[2].imp.change_threshold(self.double_spin_boxes[2].value()))
        self.double_spin_boxes[3].valueChanged.connect(lambda: self.camera_tabs[3].imp.change_threshold(self.double_spin_boxes[3].value()))
        self.camera_tabs[0].signal_process_score.connect(lambda value: self.labels_scores[0].setText(str(value)))
        self.camera_tabs[1].signal_process_score.connect(lambda value: self.labels_scores[1].setText(str(value)))
        self.camera_tabs[2].signal_process_score.connect(lambda value: self.labels_scores[2].setText(str(value)))
        self.camera_tabs[3].signal_process_score.connect(lambda value: self.labels_scores[3].setText(str(value)))

    def set_texts(self):
        self.label_predict.setText("Predict")
        self.label_threshold.setText("Threshold")
        self.label_scores.setText("Scores")

   