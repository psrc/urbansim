# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results_browser_new.ui'
#
# Created: Tue Aug 12 13:46:01 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ResultsBrowser(object):
    def setupUi(self, ResultsBrowser):
        ResultsBrowser.setObjectName("ResultsBrowser")
        ResultsBrowser.resize(951, 983)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ResultsBrowser.sizePolicy().hasHeightForWidth())
        ResultsBrowser.setSizePolicy(sizePolicy)
        self.twVisualizations = QtGui.QTabWidget(ResultsBrowser)
        self.twVisualizations.setGeometry(QtCore.QRect(10, 340, 931, 631))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twVisualizations.sizePolicy().hasHeightForWidth())
        self.twVisualizations.setSizePolicy(sizePolicy)
        self.twVisualizations.setAutoFillBackground(False)
        self.twVisualizations.setObjectName("twVisualizations")
        self.tabTable = QtGui.QWidget()
        self.tabTable.setGeometry(QtCore.QRect(0, 0, 925, 602))
        self.tabTable.setObjectName("tabTable")
        self.twVisualizations.addTab(self.tabTable, "")
        self.tabMap = QtGui.QWidget()
        self.tabMap.setGeometry(QtCore.QRect(0, 0, 925, 572))
        self.tabMap.setObjectName("tabMap")
        self.twVisualizations.addTab(self.tabMap, "")
        self.groupBox_3 = QtGui.QGroupBox(ResultsBrowser)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 931, 211))
        self.groupBox_3.setAutoFillBackground(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.splitter = QtGui.QSplitter(self.groupBox_3)
        self.splitter.setGeometry(QtCore.QRect(10, 30, 911, 171))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.lstAvailableRuns = QtGui.QListWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstAvailableRuns.sizePolicy().hasHeightForWidth())
        self.lstAvailableRuns.setSizePolicy(sizePolicy)
        self.lstAvailableRuns.setMinimumSize(QtCore.QSize(300, 0))
        self.lstAvailableRuns.setAlternatingRowColors(True)
        self.lstAvailableRuns.setObjectName("lstAvailableRuns")
        self.vboxlayout.addWidget(self.lstAvailableRuns)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(25, 0))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lstYears = QtGui.QListWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstYears.sizePolicy().hasHeightForWidth())
        self.lstYears.setSizePolicy(sizePolicy)
        self.lstYears.setMinimumSize(QtCore.QSize(40, 0))
        self.lstYears.setAlternatingRowColors(True)
        self.lstYears.setObjectName("lstYears")
        self.verticalLayout.addWidget(self.lstYears)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.wdgLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.wdgLayout.setObjectName("wdgLayout")
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.wdgLayout.addWidget(self.label_2)
        self.tableWidget = QtGui.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(37)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(500, 0))
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.wdgLayout.addWidget(self.tableWidget)
        self.splitter_2 = QtGui.QSplitter(ResultsBrowser)
        self.splitter_2.setGeometry(QtCore.QRect(10, 230, 931, 101))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setHandleWidth(10)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 441, 61))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.lblViewIndicator = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblViewIndicator.sizePolicy().hasHeightForWidth())
        self.lblViewIndicator.setSizePolicy(sizePolicy)
        self.lblViewIndicator.setObjectName("lblViewIndicator")
        self.gridLayout.addWidget(self.lblViewIndicator, 2, 1, 1, 1)
        self.lblViewYear = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblViewYear.sizePolicy().hasHeightForWidth())
        self.lblViewYear.setSizePolicy(sizePolicy)
        self.lblViewYear.setObjectName("lblViewYear")
        self.gridLayout.addWidget(self.lblViewYear, 1, 1, 1, 1)
        self.lblViewRun = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblViewRun.sizePolicy().hasHeightForWidth())
        self.lblViewRun.setSizePolicy(sizePolicy)
        self.lblViewRun.setMinimumSize(QtCore.QSize(200, 0))
        self.lblViewRun.setObjectName("lblViewRun")
        self.gridLayout.addWidget(self.lblViewRun, 0, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setAutoFillBackground(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 431, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pbnGenerateResults = QtGui.QPushButton(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbnGenerateResults.sizePolicy().hasHeightForWidth())
        self.pbnGenerateResults.setSizePolicy(sizePolicy)
        self.pbnGenerateResults.setMinimumSize(QtCore.QSize(125, 0))
        self.pbnGenerateResults.setObjectName("pbnGenerateResults")
        self.gridLayout_2.addWidget(self.pbnGenerateResults, 0, 0, 1, 1)
        self.cbAutoGen = QtGui.QCheckBox(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbAutoGen.sizePolicy().hasHeightForWidth())
        self.cbAutoGen.setSizePolicy(sizePolicy)
        self.cbAutoGen.setChecked(True)
        self.cbAutoGen.setTristate(False)
        self.cbAutoGen.setObjectName("cbAutoGen")
        self.gridLayout_2.addWidget(self.cbAutoGen, 0, 1, 1, 1)
        self.pbnExportResults = QtGui.QPushButton(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbnExportResults.sizePolicy().hasHeightForWidth())
        self.pbnExportResults.setSizePolicy(sizePolicy)
        self.pbnExportResults.setMinimumSize(QtCore.QSize(125, 0))
        self.pbnExportResults.setObjectName("pbnExportResults")
        self.gridLayout_2.addWidget(self.pbnExportResults, 1, 0, 1, 1)

        self.retranslateUi(ResultsBrowser)
        self.twVisualizations.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ResultsBrowser)

    def retranslateUi(self, ResultsBrowser):
        ResultsBrowser.setWindowTitle(QtGui.QApplication.translate("ResultsBrowser", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.twVisualizations.setTabText(self.twVisualizations.indexOf(self.tabTable), QtGui.QApplication.translate("ResultsBrowser", "Table", None, QtGui.QApplication.UnicodeUTF8))
        self.twVisualizations.setTabText(self.twVisualizations.indexOf(self.tabMap), QtGui.QApplication.translate("ResultsBrowser", "Map", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("ResultsBrowser", "Available indicators to browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ResultsBrowser", "Simulation Runs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ResultsBrowser", "Years", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ResultsBrowser", "Indicators", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(False)
        self.groupBox.setTitle(QtGui.QApplication.translate("ResultsBrowser", "Indicator being currently viewed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ResultsBrowser", "Run:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ResultsBrowser", "Year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ResultsBrowser", "Indicator:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ResultsBrowser", "Browsing options", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnGenerateResults.setText(QtGui.QApplication.translate("ResultsBrowser", "Generate results", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAutoGen.setText(QtGui.QApplication.translate("ResultsBrowser", "  Automatically  generate results", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnExportResults.setText(QtGui.QApplication.translate("ResultsBrowser", "Export results", None, QtGui.QApplication.UnicodeUTF8))

