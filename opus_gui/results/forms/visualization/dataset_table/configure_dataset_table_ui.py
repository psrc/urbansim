# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure_dataset_table_ui.ui'
#
# Created: Wed Jun 25 01:19:21 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgDatasetTableDialog(object):
    def setupUi(self, dlgDatasetTableDialog):
        dlgDatasetTableDialog.setObjectName("dlgDatasetTableDialog")
        dlgDatasetTableDialog.resize(615, 609)
        self.buttonBox = QtGui.QDialogButtonBox(dlgDatasetTableDialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gbBasicOptions = QtGui.QGroupBox(dlgDatasetTableDialog)
        self.gbBasicOptions.setGeometry(QtCore.QRect(20, 60, 281, 91))
        self.gbBasicOptions.setObjectName("gbBasicOptions")
        self.gridLayoutWidget = QtGui.QWidget(self.gbBasicOptions)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 261, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.cboDataset = QtGui.QComboBox(self.gridLayoutWidget)
        self.cboDataset.setObjectName("cboDataset")
        self.gridLayout.addWidget(self.cboDataset, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gbIndicators = QtGui.QGroupBox(dlgDatasetTableDialog)
        self.gbIndicators.setGeometry(QtCore.QRect(20, 210, 571, 351))
        self.gbIndicators.setObjectName("gbIndicators")
        self.pbnAddIndicator = QtGui.QPushButton(self.gbIndicators)
        self.pbnAddIndicator.setGeometry(QtCore.QRect(260, 170, 51, 32))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pbnAddIndicator.setFont(font)
        self.pbnAddIndicator.setObjectName("pbnAddIndicator")
        self.pbnRemoveIndicator = QtGui.QPushButton(self.gbIndicators)
        self.pbnRemoveIndicator.setGeometry(QtCore.QRect(260, 210, 51, 32))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pbnRemoveIndicator.setFont(font)
        self.pbnRemoveIndicator.setObjectName("pbnRemoveIndicator")
        self.twIndicatorsToVisualize = QtGui.QTableWidget(self.gbIndicators)
        self.twIndicatorsToVisualize.setGeometry(QtCore.QRect(320, 40, 241, 341))
        self.twIndicatorsToVisualize.setWordWrap(True)
        self.twIndicatorsToVisualize.setObjectName("twIndicatorsToVisualize")
        self.twIndicatorsToVisualize.setColumnCount(2)
        self.twIndicatorsToVisualize.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.twIndicatorsToVisualize.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twIndicatorsToVisualize.setHorizontalHeaderItem(1, item)
        self.twAvailableIndicators = QtGui.QTableWidget(self.gbIndicators)
        self.twAvailableIndicators.setGeometry(QtCore.QRect(10, 40, 241, 341))
        self.twAvailableIndicators.setObjectName("twAvailableIndicators")
        self.twAvailableIndicators.setColumnCount(1)
        self.twAvailableIndicators.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.twAvailableIndicators.setHorizontalHeaderItem(0, item)
        self.gbOutputOptions = QtGui.QGroupBox(dlgDatasetTableDialog)
        self.gbOutputOptions.setGeometry(QtCore.QRect(310, 60, 291, 151))
        self.gbOutputOptions.setObjectName("gbOutputOptions")
        self.gridLayoutWidget_2 = QtGui.QWidget(self.gbOutputOptions)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 191, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cboOutputType = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.cboOutputType.setObjectName("cboOutputType")
        self.gridLayout_2.addWidget(self.cboOutputType, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.lblOption1 = QtGui.QLabel(self.gbOutputOptions)
        self.lblOption1.setGeometry(QtCore.QRect(10, 80, 71, 41))
        self.lblOption1.setObjectName("lblOption1")
        self.leOption1 = QtGui.QLineEdit(self.gbOutputOptions)
        self.leOption1.setGeometry(QtCore.QRect(90, 90, 161, 22))
        self.leOption1.setObjectName("leOption1")
        self.pbn_set_storage_location = QtGui.QPushButton(self.gbOutputOptions)
        self.pbn_set_storage_location.setGeometry(QtCore.QRect(260, 90, 21, 21))
        self.pbn_set_storage_location.setObjectName("pbn_set_storage_location")
        self.label_5 = QtGui.QLabel(dlgDatasetTableDialog)
        self.label_5.setGeometry(QtCore.QRect(30, 20, 131, 18))
        self.label_5.setObjectName("label_5")
        self.leVizName = QtGui.QLineEdit(dlgDatasetTableDialog)
        self.leVizName.setGeometry(QtCore.QRect(170, 20, 421, 22))
        self.leVizName.setObjectName("leVizName")

        self.retranslateUi(dlgDatasetTableDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgDatasetTableDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgDatasetTableDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgDatasetTableDialog)

    def retranslateUi(self, dlgDatasetTableDialog):
        dlgDatasetTableDialog.setWindowTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Indicator-spanning table visualization configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.gbBasicOptions.setTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Basic options", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Dataset:", None, QtGui.QApplication.UnicodeUTF8))
        self.gbIndicators.setTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Indicators to visualize", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnAddIndicator.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnRemoveIndicator.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.twIndicatorsToVisualize.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "To visualize", None, QtGui.QApplication.UnicodeUTF8))
        self.twIndicatorsToVisualize.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Format", None, QtGui.QApplication.UnicodeUTF8))
        self.twAvailableIndicators.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Available indicators", None, QtGui.QApplication.UnicodeUTF8))
        self.gbOutputOptions.setTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Output options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOption1.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pbn_set_storage_location.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Visualization name:", None, QtGui.QApplication.UnicodeUTF8))

