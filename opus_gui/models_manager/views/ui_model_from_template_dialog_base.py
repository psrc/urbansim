# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'model_from_template_dialog_base.ui'
#
# Created: Tue Jan 06 13:30:44 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ModelFromTemplateDialogBase(object):
    def setupUi(self, ModelFromTemplateDialogBase):
        ModelFromTemplateDialogBase.setObjectName("ModelFromTemplateDialogBase")
        ModelFromTemplateDialogBase.resize(627,250)
        self.verticalLayout = QtGui.QVBoxLayout(ModelFromTemplateDialogBase)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(ModelFromTemplateDialogBase)
        self.groupBox.setObjectName("groupBox")
        self.vlayout = QtGui.QVBoxLayout(self.groupBox)
        self.vlayout.setObjectName("vlayout")
        self.frame = QtGui.QFrame(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215,50))
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100,0))
        self.label.setMaximumSize(QtCore.QSize(200,16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.leModelName = QtGui.QLineEdit(self.frame)
        self.leModelName.setObjectName("leModelName")
        self.horizontalLayout.addWidget(self.leModelName)
        self.vlayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(ModelFromTemplateDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ModelFromTemplateDialogBase)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),ModelFromTemplateDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),ModelFromTemplateDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ModelFromTemplateDialogBase)

    def retranslateUi(self, ModelFromTemplateDialogBase):
        ModelFromTemplateDialogBase.setWindowTitle(QtGui.QApplication.translate("ModelFromTemplateDialogBase", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ModelFromTemplateDialogBase", "Create new model from model template", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ModelFromTemplateDialogBase", "Model name:", None, QtGui.QApplication.UnicodeUTF8))

