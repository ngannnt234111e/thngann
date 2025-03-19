# Form implementation generated from reading ui file 'D:\pythonProject2\mid\mid.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 200)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setObjectName("main_layout")
        self.title_label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.main_layout.addWidget(self.title_label)
        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_layout.setObjectName("file_layout")
        self.file_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.file_label.setObjectName("file_label")
        self.file_layout.addWidget(self.file_label)
        self.file_path_edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setObjectName("file_path_edit")
        self.file_layout.addWidget(self.file_path_edit)
        self.browse_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.browse_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.browse_button.setObjectName("browse_button")
        self.file_layout.addWidget(self.browse_button)
        self.main_layout.addLayout(self.file_layout)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        self.open_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.open_button.setMinimumSize(QtCore.QSize(0, 40))
        self.open_button.setObjectName("open_button")
        self.button_layout.addWidget(self.open_button)
        self.save_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.save_button.setMinimumSize(QtCore.QSize(0, 40))
        self.save_button.setObjectName("save_button")
        self.button_layout.addWidget(self.save_button)
        self.main_layout.addLayout(self.button_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chương Trình Đào Tạo Visualizer"))
        self.title_label.setText(_translate("MainWindow", "Chương Trình Đào Tạo Visualizer"))
        self.file_label.setText(_translate("MainWindow", "Choose Dataset:"))
        self.browse_button.setText(_translate("MainWindow", "..."))
        self.open_button.setText(_translate("MainWindow", "Open Chart in Browser"))
        self.save_button.setText(_translate("MainWindow", "Save Chart to HTML File"))
