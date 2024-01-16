# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/main/views/list_editor.ui'
#
# Created: Sun May 10 00:57:43 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ListEditor(object):
    def setupUi(self, ListEditor):
        ListEditor.setObjectName("ListEditor")
        ListEditor.resize(310, 280)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ListEditor)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_up = QtWidgets.QToolButton(ListEditor)
        self.tb_up.setObjectName("tb_up")
        self.verticalLayout.addWidget(self.tb_up)
        self.tb_down = QtWidgets.QToolButton(ListEditor)
        self.tb_down.setObjectName("tb_down")
        self.verticalLayout.addWidget(self.tb_down)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(ListEditor)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(ListEditor)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.toolButton = QtWidgets.QToolButton(ListEditor)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_value = QtWidgets.QLineEdit(ListEditor)
        self.le_value.setObjectName("le_value")
        self.horizontalLayout.addWidget(self.le_value)
        self.tb_change = QtWidgets.QToolButton(ListEditor)
        self.tb_change.setObjectName("tb_change")
        self.horizontalLayout.addWidget(self.tb_change)
        self.tb_add = QtWidgets.QToolButton(ListEditor)
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout.addWidget(self.tb_add)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(ListEditor)
        QtCore.QMetaObject.connectSlotsByName(ListEditor)

    def retranslateUi(self, ListEditor):
        ListEditor.setWindowTitle(QtWidgets.QApplication.translate("ListEditor", "Form", None))
        self.tb_up.setText(QtWidgets.QApplication.translate("ListEditor", "^", None))
        self.tb_down.setText(QtWidgets.QApplication.translate("ListEditor", "v", None))
        self.label.setText(QtWidgets.QApplication.translate("ListEditor", "Selected:", None))
        self.toolButton.setText(QtWidgets.QApplication.translate("ListEditor", "-", None))
        self.tb_change.setText(QtWidgets.QApplication.translate("ListEditor", "=", None))
        self.tb_add.setText(QtWidgets.QApplication.translate("ListEditor", "+", None))

