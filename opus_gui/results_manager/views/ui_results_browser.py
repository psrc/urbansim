# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/results_manager/views/results_browser.ui'
#
# Created: Sun May 10 17:20:29 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ResultsBrowser(object):
    def setupUi(self, ResultsBrowser):
        ResultsBrowser.setObjectName("ResultsBrowser")
        ResultsBrowser.resize(819, 744)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ResultsBrowser.sizePolicy().hasHeightForWidth())
        ResultsBrowser.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QtWidgets.QGridLayout(ResultsBrowser)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.splitter_2 = QtWidgets.QSplitter(ResultsBrowser)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setAutoFillBackground(False)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.configSplitter = QtWidgets.QSplitter(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configSplitter.sizePolicy().hasHeightForWidth())
        self.configSplitter.setSizePolicy(sizePolicy)
        self.configSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.configSplitter.setHandleWidth(12)
        self.configSplitter.setObjectName("configSplitter")
        self.groupBox = QtWidgets.QGroupBox(self.configSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setBaseSize(QtCore.QSize(0, 100))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lst_available_runs = QtWidgets.QListWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_available_runs.sizePolicy().hasHeightForWidth())
        self.lst_available_runs.setSizePolicy(sizePolicy)
        self.lst_available_runs.setMinimumSize(QtCore.QSize(0, 0))
        self.lst_available_runs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lst_available_runs.setBaseSize(QtCore.QSize(100, 50))
        self.lst_available_runs.setAlternatingRowColors(True)
        self.lst_available_runs.setObjectName("lst_available_runs")
        self.verticalLayout_4.addWidget(self.lst_available_runs)
        self.groupBox_2 = QtWidgets.QGroupBox(self.configSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setBaseSize(QtCore.QSize(20, 0))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lst_years = QtWidgets.QListWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_years.sizePolicy().hasHeightForWidth())
        self.lst_years.setSizePolicy(sizePolicy)
        self.lst_years.setMinimumSize(QtCore.QSize(0, 0))
        self.lst_years.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lst_years.setBaseSize(QtCore.QSize(20, 50))
        self.lst_years.setAlternatingRowColors(True)
        self.lst_years.setObjectName("lst_years")
        self.verticalLayout_3.addWidget(self.lst_years)
        self.groupBox_4 = QtWidgets.QGroupBox(self.configSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setBaseSize(QtCore.QSize(500, 0))
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.indicator_table = QtWidgets.QTableWidget(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.indicator_table.sizePolicy().hasHeightForWidth())
        self.indicator_table.setSizePolicy(sizePolicy)
        self.indicator_table.setMinimumSize(QtCore.QSize(0, 0))
        self.indicator_table.setBaseSize(QtCore.QSize(500, 50))
        self.indicator_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.indicator_table.setDragDropOverwriteMode(False)
        self.indicator_table.setAlternatingRowColors(True)
        self.indicator_table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.indicator_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.indicator_table.setTextElideMode(QtCore.Qt.ElideNone)
        self.indicator_table.setShowGrid(True)
        self.indicator_table.setColumnCount(3)
        self.indicator_table.setObjectName("indicator_table")
        self.indicator_table.setColumnCount(3)
        self.indicator_table.setRowCount(0)
        self.verticalLayout_2.addWidget(self.indicator_table)
        self.verticalLayout.addWidget(self.configSplitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cb_auto_gen = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_auto_gen.sizePolicy().hasHeightForWidth())
        self.cb_auto_gen.setSizePolicy(sizePolicy)
        self.cb_auto_gen.setTristate(False)
        self.cb_auto_gen.setObjectName("cb_auto_gen")
        self.horizontalLayout.addWidget(self.cb_auto_gen)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_current_selection = QtWidgets.QLabel(self.groupBox_3)
        font = QtWidgets.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lbl_current_selection.setFont(font)
        self.lbl_current_selection.setObjectName("lbl_current_selection")
        self.horizontalLayout_2.addWidget(self.lbl_current_selection)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pb_generate_results = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_generate_results.sizePolicy().hasHeightForWidth())
        self.pb_generate_results.setSizePolicy(sizePolicy)
        self.pb_generate_results.setMinimumSize(QtCore.QSize(0, 0))
        self.pb_generate_results.setObjectName("pb_generate_results")
        self.verticalLayout_5.addWidget(self.pb_generate_results)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabwidget_visualizations = QtWidgets.QTabWidget(self.splitter_2)
        self.tabwidget_visualizations.setMinimumSize(QtCore.QSize(0, 200))
        self.tabwidget_visualizations.setObjectName("tabwidget_visualizations")
        self.starttab = QtWidgets.QWidget()
        self.starttab.setObjectName("starttab")
        self.tabwidget_visualizations.addTab(self.starttab, "")
        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(ResultsBrowser)
        self.tabwidget_visualizations.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ResultsBrowser)

    def retranslateUi(self, ResultsBrowser):
        ResultsBrowser.setWindowTitle(QtWidgets.QApplication.translate("ResultsBrowser", "Result Browser", None))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("ResultsBrowser", "Configure an indicator to view", None))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("ResultsBrowser", "Simulation Runs", None))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("ResultsBrowser", "Years", None))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("ResultsBrowser", "Indicators", None))
        self.indicator_table.setSortingEnabled(False)
        self.cb_auto_gen.setToolTip(QtWidgets.QApplication.translate("ResultsBrowser", "Automatically generate and view the indicator when it\'s selected", None))
        self.cb_auto_gen.setText(QtWidgets.QApplication.translate("ResultsBrowser", "Automatically generate", None))
        self.lbl_current_selection.setText(QtWidgets.QApplication.translate("ResultsBrowser", "current selection", None))
        self.pb_generate_results.setText(QtWidgets.QApplication.translate("ResultsBrowser", "Generate results", None))
        self.tabwidget_visualizations.setTabText(self.tabwidget_visualizations.indexOf(self.starttab), QtWidgets.QApplication.translate("ResultsBrowser", "starttab", None))

        ################################3
        self.cb_auto_gen.setText(QtWidgets.QApplication.translate("ResultsBrowser", "Uncertainty options generate", None))
  