# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure_dataset_table_ui.ui'
#
# Created: Mon Aug 18 10:40:10 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgDatasetTableDialog(object):
    def setupUi(self, dlgDatasetTableDialog):
        dlgDatasetTableDialog.setObjectName("dlgDatasetTableDialog")
        dlgDatasetTableDialog.resize(905, 604)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgDatasetTableDialog.sizePolicy().hasHeightForWidth())
        dlgDatasetTableDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtGui.QDialogButtonBox(dlgDatasetTableDialog)
        self.buttonBox.setGeometry(QtCore.QRect(450, 560, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gbOutputOptions = QtGui.QGroupBox(dlgDatasetTableDialog)
        self.gbOutputOptions.setGeometry(QtCore.QRect(20, 0, 431, 141))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbOutputOptions.sizePolicy().hasHeightForWidth())
        self.gbOutputOptions.setSizePolicy(sizePolicy)
        self.gbOutputOptions.setObjectName("gbOutputOptions")
        self.widget = QtGui.QWidget(self.gbOutputOptions)
        self.widget.setGeometry(QtCore.QRect(10, 30, 411, 101))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.leVizName = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leVizName.sizePolicy().hasHeightForWidth())
        self.leVizName.setSizePolicy(sizePolicy)
        self.leVizName.setMinimumSize(QtCore.QSize(100, 0))
        self.leVizName.setObjectName("leVizName")
        self.gridLayout.addWidget(self.leVizName, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.cboDataset = QtGui.QComboBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboDataset.sizePolicy().hasHeightForWidth())
        self.cboDataset.setSizePolicy(sizePolicy)
        self.cboDataset.setObjectName("cboDataset")
        self.gridLayout.addWidget(self.cboDataset, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.cboOutputType = QtGui.QComboBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboOutputType.sizePolicy().hasHeightForWidth())
        self.cboOutputType.setSizePolicy(sizePolicy)
        self.cboOutputType.setMinimumSize(QtCore.QSize(0, 0))
        self.cboOutputType.setObjectName("cboOutputType")
        self.gridLayout.addWidget(self.cboOutputType, 2, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(dlgDatasetTableDialog)
        self.groupBox.setGeometry(QtCore.QRect(470, 0, 411, 141))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.widget1 = QtGui.QWidget(self.groupBox)
        self.widget1.setGeometry(QtCore.QRect(10, 90, 391, 41))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblOption1 = QtGui.QLabel(self.widget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOption1.sizePolicy().hasHeightForWidth())
        self.lblOption1.setSizePolicy(sizePolicy)
        self.lblOption1.setObjectName("lblOption1")
        self.horizontalLayout.addWidget(self.lblOption1)
        self.leOption1 = QtGui.QLineEdit(self.widget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leOption1.sizePolicy().hasHeightForWidth())
        self.leOption1.setSizePolicy(sizePolicy)
        self.leOption1.setMinimumSize(QtCore.QSize(100, 0))
        self.leOption1.setObjectName("leOption1")
        self.horizontalLayout.addWidget(self.leOption1)
        self.pbn_set_storage_location = QtGui.QPushButton(self.widget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbn_set_storage_location.sizePolicy().hasHeightForWidth())
        self.pbn_set_storage_location.setSizePolicy(sizePolicy)
        self.pbn_set_storage_location.setObjectName("pbn_set_storage_location")
        self.horizontalLayout.addWidget(self.pbn_set_storage_location)
        self.widget2 = QtGui.QWidget(self.groupBox)
        self.widget2.setGeometry(QtCore.QRect(10, 30, 391, 61))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rbSingleTable = QtGui.QRadioButton(self.widget2)
        self.rbSingleTable.setChecked(True)
        self.rbSingleTable.setObjectName("rbSingleTable")
        self.verticalLayout_4.addWidget(self.rbSingleTable)
        self.rbTablePerYear = QtGui.QRadioButton(self.widget2)
        self.rbTablePerYear.setObjectName("rbTablePerYear")
        self.verticalLayout_4.addWidget(self.rbTablePerYear)
        self.rbTablePerIndicator = QtGui.QRadioButton(self.widget2)
        self.rbTablePerIndicator.setObjectName("rbTablePerIndicator")
        self.verticalLayout_4.addWidget(self.rbTablePerIndicator)
        self.line = QtGui.QFrame(dlgDatasetTableDialog)
        self.line.setGeometry(QtCore.QRect(20, 140, 861, 21))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget3 = QtGui.QWidget(dlgDatasetTableDialog)
        self.widget3.setGeometry(QtCore.QRect(490, 289, 58, 104))
        self.widget3.setObjectName("widget3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pbnAddIndicator = QtGui.QPushButton(self.widget3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbnAddIndicator.sizePolicy().hasHeightForWidth())
        self.pbnAddIndicator.setSizePolicy(sizePolicy)
        self.pbnAddIndicator.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pbnAddIndicator.setFont(font)
        self.pbnAddIndicator.setObjectName("pbnAddIndicator")
        self.verticalLayout_3.addWidget(self.pbnAddIndicator)
        self.pbnRemoveIndicator = QtGui.QPushButton(self.widget3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbnRemoveIndicator.sizePolicy().hasHeightForWidth())
        self.pbnRemoveIndicator.setSizePolicy(sizePolicy)
        self.pbnRemoveIndicator.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pbnRemoveIndicator.setFont(font)
        self.pbnRemoveIndicator.setObjectName("pbnRemoveIndicator")
        self.verticalLayout_3.addWidget(self.pbnRemoveIndicator)
        self.verticalLayoutWidget = QtGui.QWidget(dlgDatasetTableDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(21, 159, 461, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.twAvailableIndicators = QtGui.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(37)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twAvailableIndicators.sizePolicy().hasHeightForWidth())
        self.twAvailableIndicators.setSizePolicy(sizePolicy)
        self.twAvailableIndicators.setMinimumSize(QtCore.QSize(200, 0))
        self.twAvailableIndicators.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.twAvailableIndicators.setDragDropOverwriteMode(False)
        self.twAvailableIndicators.setAlternatingRowColors(True)
        self.twAvailableIndicators.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.twAvailableIndicators.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.twAvailableIndicators.setTextElideMode(QtCore.Qt.ElideRight)
        self.twAvailableIndicators.setShowGrid(True)
        self.twAvailableIndicators.setColumnCount(3)
        self.twAvailableIndicators.setObjectName("twAvailableIndicators")
        self.twAvailableIndicators.setColumnCount(3)
        self.twAvailableIndicators.setRowCount(0)
        self.verticalLayout.addWidget(self.twAvailableIndicators)
        self.verticalLayoutWidget_2 = QtGui.QWidget(dlgDatasetTableDialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(559, 159, 321, 391))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.twIndicatorsToVisualize = QtGui.QTableWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twIndicatorsToVisualize.sizePolicy().hasHeightForWidth())
        self.twIndicatorsToVisualize.setSizePolicy(sizePolicy)
        self.twIndicatorsToVisualize.setMinimumSize(QtCore.QSize(200, 0))
        self.twIndicatorsToVisualize.setDragDropOverwriteMode(False)
        self.twIndicatorsToVisualize.setAlternatingRowColors(True)
        self.twIndicatorsToVisualize.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.twIndicatorsToVisualize.setWordWrap(True)
        self.twIndicatorsToVisualize.setObjectName("twIndicatorsToVisualize")
        self.twIndicatorsToVisualize.setColumnCount(2)
        self.twIndicatorsToVisualize.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.twIndicatorsToVisualize.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twIndicatorsToVisualize.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.twIndicatorsToVisualize)

        self.retranslateUi(dlgDatasetTableDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgDatasetTableDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgDatasetTableDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgDatasetTableDialog)

    def retranslateUi(self, dlgDatasetTableDialog):
        dlgDatasetTableDialog.setWindowTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Batch Indicator Visualization: Table", None, QtGui.QApplication.UnicodeUTF8))
        self.gbOutputOptions.setTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Output options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Visualization name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Dataset name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Format:", None, QtGui.QApplication.UnicodeUTF8))
        self.cboOutputType.addItem(QtGui.QApplication.translate("dlgDatasetTableDialog", "Tab delimited file (.tab)", None, QtGui.QApplication.UnicodeUTF8))
        self.cboOutputType.addItem(QtGui.QApplication.translate("dlgDatasetTableDialog", "Fixed field file (.dat)", None, QtGui.QApplication.UnicodeUTF8))
        self.cboOutputType.addItem(QtGui.QApplication.translate("dlgDatasetTableDialog", "Export to SQL database", None, QtGui.QApplication.UnicodeUTF8))
        self.cboOutputType.addItem(QtGui.QApplication.translate("dlgDatasetTableDialog", "ESRI database", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("dlgDatasetTableDialog", "Format options", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOption1.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pbn_set_storage_location.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.rbSingleTable.setToolTip(QtGui.QApplication.translate("dlgDatasetTableDialog", "The table will have the values of all indicators for each year the indicator batch is run on.", None, QtGui.QApplication.UnicodeUTF8))
        self.rbSingleTable.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Output a single table", None, QtGui.QApplication.UnicodeUTF8))
        self.rbTablePerYear.setToolTip(QtGui.QApplication.translate("dlgDatasetTableDialog", "Each table will have the values of the selected indicators for the given year.", None, QtGui.QApplication.UnicodeUTF8))
        self.rbTablePerYear.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Output a table for every year", None, QtGui.QApplication.UnicodeUTF8))
        self.rbTablePerIndicator.setToolTip(QtGui.QApplication.translate("dlgDatasetTableDialog", "Each table will have the values of a given indicator across all years the batch is run on.", None, QtGui.QApplication.UnicodeUTF8))
        self.rbTablePerIndicator.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Output a table for each indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnAddIndicator.setToolTip(QtGui.QApplication.translate("dlgDatasetTableDialog", "Add currently selected indicator on the left to this indicator visualization.", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnAddIndicator.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnRemoveIndicator.setToolTip(QtGui.QApplication.translate("dlgDatasetTableDialog", "Remove currently selected indicator on the right from this indicator visualization.", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnRemoveIndicator.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Available Indicators", None, QtGui.QApplication.UnicodeUTF8))
        self.twAvailableIndicators.setSortingEnabled(False)
        self.label_2.setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Indicators in current visualization", None, QtGui.QApplication.UnicodeUTF8))
        self.twIndicatorsToVisualize.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.twIndicatorsToVisualize.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("dlgDatasetTableDialog", "Field format", None, QtGui.QApplication.UnicodeUTF8))

