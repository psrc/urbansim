# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opus_result_generator_gui.ui'
#
# Created: Sat Dec 29 09:26:24 2007
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(80,10,431,311))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150,140,113,32))
        self.pushButton.setObjectName("pushButton")

        self.widget = QtGui.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(70,20,271,92))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        self.lineEdit_2 = QtGui.QLineEdit(self.widget)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridlayout.addWidget(self.lineEdit_2,0,0,1,1)

        self.comboBox_2 = QtGui.QComboBox(self.widget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridlayout.addWidget(self.comboBox_2,0,1,1,1)

        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridlayout.addWidget(self.lineEdit,1,0,1,1)

        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.gridlayout.addWidget(self.comboBox,1,1,1,1)

        self.lineEdit_3 = QtGui.QLineEdit(self.widget)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridlayout.addWidget(self.lineEdit_3,2,0,1,1)

        self.comboBox_3 = QtGui.QComboBox(self.widget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridlayout.addWidget(self.comboBox_3,2,1,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,800,22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Generate results", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setText(QtGui.QApplication.translate("MainWindow", "Indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(QtGui.QApplication.translate("MainWindow", "[select]", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", "Dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "[select]", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "gridcell", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "zone", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "taz", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "county", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "all_data", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_3.setText(QtGui.QApplication.translate("MainWindow", "Source data", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(QtGui.QApplication.translate("MainWindow", "[select]", None, QtGui.QApplication.UnicodeUTF8))

