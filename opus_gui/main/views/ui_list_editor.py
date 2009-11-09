# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/main/views/list_editor.ui'
#
# Created: Sun May 10 00:57:43 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ListEditor(object):
    def setupUi(self, ListEditor):
        ListEditor.setObjectName("ListEditor")
        ListEditor.resize(310, 280)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ListEditor)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_up = QtGui.QToolButton(ListEditor)
        self.tb_up.setObjectName("tb_up")
        self.verticalLayout.addWidget(self.tb_up)
        self.tb_down = QtGui.QToolButton(ListEditor)
        self.tb_down.setObjectName("tb_down")
        self.verticalLayout.addWidget(self.tb_down)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtGui.QListWidget(ListEditor)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(ListEditor)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.toolButton = QtGui.QToolButton(ListEditor)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_value = QtGui.QLineEdit(ListEditor)
        self.le_value.setObjectName("le_value")
        self.horizontalLayout.addWidget(self.le_value)
        self.tb_change = QtGui.QToolButton(ListEditor)
        self.tb_change.setObjectName("tb_change")
        self.horizontalLayout.addWidget(self.tb_change)
        self.tb_add = QtGui.QToolButton(ListEditor)
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout.addWidget(self.tb_add)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(ListEditor)
        QtCore.QMetaObject.connectSlotsByName(ListEditor)

    def retranslateUi(self, ListEditor):
        ListEditor.setWindowTitle(QtGui.QApplication.translate("ListEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tb_up.setText(QtGui.QApplication.translate("ListEditor", "^", None, QtGui.QApplication.UnicodeUTF8))
        self.tb_down.setText(QtGui.QApplication.translate("ListEditor", "v", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ListEditor", "Selected:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("ListEditor", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.tb_change.setText(QtGui.QApplication.translate("ListEditor", "=", None, QtGui.QApplication.UnicodeUTF8))
        self.tb_add.setText(QtGui.QApplication.translate("ListEditor", "+", None, QtGui.QApplication.UnicodeUTF8))

