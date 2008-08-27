# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables_new.ui'
#
# Created: Wed Aug 27 12:34:12 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesNewGui(object):
    def setupUi(self, AllVariablesNewGui):
        AllVariablesNewGui.setObjectName("AllVariablesNewGui")
        AllVariablesNewGui.resize(QtCore.QSize(QtCore.QRect(0,0,657,499).size()).expandedTo(AllVariablesNewGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AllVariablesNewGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(AllVariablesNewGui)
        self.variableBox.setObjectName("variableBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.variableBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.nameWidget = QtGui.QWidget(self.variableBox)
        self.nameWidget.setObjectName("nameWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.nameWidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(self.nameWidget)
        self.label.setMinimumSize(QtCore.QSize(100,0))
        self.label.setMaximumSize(QtCore.QSize(100,16777215))
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit(self.nameWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout.addWidget(self.lineEdit)
        self.vboxlayout1.addWidget(self.nameWidget)

        self.datasetWidget = QtGui.QWidget(self.variableBox)
        self.datasetWidget.setObjectName("datasetWidget")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.datasetWidget)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_2 = QtGui.QLabel(self.datasetWidget)
        self.label_2.setMinimumSize(QtCore.QSize(100,0))
        self.label_2.setMaximumSize(QtCore.QSize(100,16777215))
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)

        self.lineEdit_2 = QtGui.QLineEdit(self.datasetWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.hboxlayout1.addWidget(self.lineEdit_2)
        self.vboxlayout1.addWidget(self.datasetWidget)

        self.useWidget = QtGui.QWidget(self.variableBox)
        self.useWidget.setObjectName("useWidget")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.useWidget)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_3 = QtGui.QLabel(self.useWidget)
        self.label_3.setMinimumSize(QtCore.QSize(100,0))
        self.label_3.setMaximumSize(QtCore.QSize(100,16777215))
        self.label_3.setObjectName("label_3")
        self.hboxlayout2.addWidget(self.label_3)

        self.comboBox = QtGui.QComboBox(self.useWidget)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout2.addWidget(self.comboBox)
        self.vboxlayout1.addWidget(self.useWidget)

        self.sourceWidget = QtGui.QWidget(self.variableBox)
        self.sourceWidget.setObjectName("sourceWidget")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.sourceWidget)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_4 = QtGui.QLabel(self.sourceWidget)
        self.label_4.setMinimumSize(QtCore.QSize(100,0))
        self.label_4.setMaximumSize(QtCore.QSize(100,16777215))
        self.label_4.setObjectName("label_4")
        self.hboxlayout3.addWidget(self.label_4)

        self.comboBox_2 = QtGui.QComboBox(self.sourceWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.hboxlayout3.addWidget(self.comboBox_2)
        self.vboxlayout1.addWidget(self.sourceWidget)

        self.definitionWidget = QtGui.QWidget(self.variableBox)
        self.definitionWidget.setObjectName("definitionWidget")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.definitionWidget)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_5 = QtGui.QLabel(self.definitionWidget)
        self.label_5.setMinimumSize(QtCore.QSize(100,0))
        self.label_5.setMaximumSize(QtCore.QSize(100,16777215))
        self.label_5.setObjectName("label_5")
        self.hboxlayout4.addWidget(self.label_5)

        self.textEdit = QtGui.QTextEdit(self.definitionWidget)
        self.textEdit.setObjectName("textEdit")
        self.hboxlayout4.addWidget(self.textEdit)
        self.vboxlayout1.addWidget(self.definitionWidget)
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(AllVariablesNewGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.hboxlayout5 = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout5.setObjectName("hboxlayout5")

        spacerItem = QtGui.QSpacerItem(441,24,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout5.addWidget(self.line)

        self.saveChanges = QtGui.QPushButton(self.widget)
        self.saveChanges.setEnabled(True)
        self.saveChanges.setObjectName("saveChanges")
        self.hboxlayout5.addWidget(self.saveChanges)

        self.cancelWindow = QtGui.QPushButton(self.widget)
        self.cancelWindow.setObjectName("cancelWindow")
        self.hboxlayout5.addWidget(self.cancelWindow)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesNewGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesNewGui)

    def retranslateUi(self, AllVariablesNewGui):
        AllVariablesNewGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesNewGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("AllVariablesNewGui", "New Expression", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Name - ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Dataset - ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Use -", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "both", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "model variable", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Source - ", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "primary attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "expression", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(QtGui.QApplication.translate("AllVariablesNewGui", "python module", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Definition - ", None, QtGui.QApplication.UnicodeUTF8))
        self.saveChanges.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesNewGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

