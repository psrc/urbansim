# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusMain.ui'
#
# Created: Fri Oct 05 11:42:42 2007
#      by: PyQt4 UI code generator 4-snapshot-20070727
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,902,648).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.toolBox = QtGui.QToolBox(self.splitter)
        self.toolBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setBaseSize(QtCore.QSize(0,0))
        self.toolBox.setObjectName("toolBox")

        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,402,475))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout1 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.treeWidget_2 = QtGui.QTreeWidget(self.datamanager_page)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.treeWidget_2.headerItem().setText(0,"")
        self.gridlayout1.addWidget(self.treeWidget_2,0,0,1,1)
        self.toolBox.addItem(self.datamanager_page,"")

        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0,0,96,79))
        self.modelmanager_page.setObjectName("modelmanager_page")

        self.gridlayout2 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.treeWidget_3 = QtGui.QTreeWidget(self.modelmanager_page)
        self.treeWidget_3.setObjectName("treeWidget_3")
        self.treeWidget_3.headerItem().setText(0,"")
        self.gridlayout2.addWidget(self.treeWidget_3,0,0,1,1)
        self.toolBox.addItem(self.modelmanager_page,"")

        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0,0,96,79))
        self.runmanager_page.setObjectName("runmanager_page")

        self.gridlayout3 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.treeWidget_4 = QtGui.QTreeWidget(self.runmanager_page)
        self.treeWidget_4.setObjectName("treeWidget_4")
        self.treeWidget_4.headerItem().setText(0,"")
        self.gridlayout3.addWidget(self.treeWidget_4,0,0,1,1)
        self.toolBox.addItem(self.runmanager_page,"")

        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0,0,96,79))
        self.resultsmanager_page.setObjectName("resultsmanager_page")

        self.gridlayout4 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.treeWidget_5 = QtGui.QTreeWidget(self.resultsmanager_page)
        self.treeWidget_5.setObjectName("treeWidget_5")
        self.treeWidget_5.headerItem().setText(0,"")
        self.gridlayout4.addWidget(self.treeWidget_5,0,0,1,1)
        self.toolBox.addItem(self.resultsmanager_page,"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_mapView = QtGui.QWidget()
        self.tab_mapView.setObjectName("tab_mapView")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_mapView)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.widgetMap = QtGui.QWidget(self.tab_mapView)
        self.widgetMap.setMinimumSize(QtCore.QSize(100,100))
        self.widgetMap.setAutoFillBackground(True)
        self.widgetMap.setObjectName("widgetMap")
        self.gridlayout5.addWidget(self.widgetMap,0,0,1,1)
        self.tabWidget.addTab(self.tab_mapView,"")

        self.tab_detailView = QtGui.QWidget()
        self.tab_detailView.setObjectName("tab_detailView")

        self.gridlayout6 = QtGui.QGridLayout(self.tab_detailView)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.groupBox_3 = QtGui.QGroupBox(self.tab_detailView)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridlayout6.addWidget(self.groupBox_3,0,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.tab_detailView)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridlayout6.addWidget(self.groupBox_4,1,0,1,1)
        self.tabWidget.addTab(self.tab_detailView,"")

        self.tab_trendView = QtGui.QWidget()
        self.tab_trendView.setObjectName("tab_trendView")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_trendView)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.groupBox_2 = QtGui.QGroupBox(self.tab_trendView)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.frame = QtGui.QFrame(self.groupBox_2)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridlayout9 = QtGui.QGridLayout(self.frame)
        self.gridlayout9.setMargin(9)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")

        self.textEdit = QtGui.QTextEdit(self.frame)
        self.textEdit.setMinimumSize(QtCore.QSize(100,100))
        self.textEdit.setBaseSize(QtCore.QSize(0,0))
        self.textEdit.setObjectName("textEdit")
        self.gridlayout9.addWidget(self.textEdit,0,0,1,1)
        self.gridlayout8.addWidget(self.frame,0,0,1,1)
        self.gridlayout7.addWidget(self.groupBox_2,1,0,1,1)

        self.groupBox = QtGui.QGroupBox(self.tab_trendView)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout10 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout10.setMargin(9)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

        self.tableWidget = QtGui.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.gridlayout10.addWidget(self.tableWidget,0,0,1,1)
        self.gridlayout7.addWidget(self.groupBox,0,0,1,1)
        self.tabWidget.addTab(self.tab_trendView,"")

        self.tab_modelFlow = QtGui.QWidget()
        self.tab_modelFlow.setObjectName("tab_modelFlow")
        self.tabWidget.addTab(self.tab_modelFlow,"")

        self.tab_runStatus = QtGui.QWidget()
        self.tab_runStatus.setObjectName("tab_runStatus")
        self.tabWidget.addTab(self.tab_runStatus,"")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,902,24))
        self.menubar.setObjectName("menubar")

        self.menuModel_Manager = QtGui.QMenu(self.menubar)
        self.menuModel_Manager.setObjectName("menuModel_Manager")

        self.menuRun_Manager = QtGui.QMenu(self.menubar)
        self.menuRun_Manager.setObjectName("menuRun_Manager")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName("menuUtilities")

        self.menuData_Manager = QtGui.QMenu(self.menubar)
        self.menuData_Manager.setObjectName("menuData_Manager")

        self.menuResults_Manager = QtGui.QMenu(self.menubar)
        self.menuResults_Manager.setObjectName("menuResults_Manager")

        self.menuMap = QtGui.QMenu(self.menubar)
        self.menuMap.setObjectName("menuMap")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        self.mpActionZoomOut.setIcon(QtGui.QIcon(":/Images/Images/mActionZoomOut.png"))
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")

        self.mpActionPan = QtGui.QAction(MainWindow)
        self.mpActionPan.setIcon(QtGui.QIcon(":/Images/Images/mActionPan.png"))
        self.mpActionPan.setObjectName("mpActionPan")

        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        self.mpActionAddRasterLayer.setIcon(QtGui.QIcon(":/Images/Images/mActionAddRasterLayer.png"))
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")

        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        self.mpActionZoomIn.setIcon(QtGui.QIcon(":/Images/Images/mActionZoomIn.png"))
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")

        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        self.mpActionAddVectorLayer.setIcon(QtGui.QIcon(":/Images/Images/mActionAddLayer.png"))
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menuMap.addAction(self.mpActionZoomIn)
        self.menuMap.addAction(self.mpActionZoomOut)
        self.menuMap.addAction(self.mpActionPan)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuData_Manager.menuAction())
        self.menubar.addAction(self.menuModel_Manager.menuAction())
        self.menubar.addAction(self.menuRun_Manager.menuAction())
        self.menubar.addAction(self.menuResults_Manager.menuAction())
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuUtilities.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpusGui", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.clear()

        item = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item.setText(0,QtGui.QApplication.translate("MainWindow", "Database", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("MainWindow", "Table", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QTreeWidgetItem(item)
        item2.setText(0,QtGui.QApplication.translate("MainWindow", "Relation", None, QtGui.QApplication.UnicodeUTF8))

        item3 = QtGui.QTreeWidgetItem(item)
        item3.setText(0,QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))

        item4 = QtGui.QTreeWidgetItem(item)
        item4.setText(0,QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_3.clear()

        item5 = QtGui.QTreeWidgetItem(self.treeWidget_3)
        item5.setText(0,QtGui.QApplication.translate("MainWindow", "Model System", None, QtGui.QApplication.UnicodeUTF8))

        item6 = QtGui.QTreeWidgetItem(item5)
        item6.setText(0,QtGui.QApplication.translate("MainWindow", "Model", None, QtGui.QApplication.UnicodeUTF8))

        item7 = QtGui.QTreeWidgetItem(item6)
        item7.setText(0,QtGui.QApplication.translate("MainWindow", "Configuration", None, QtGui.QApplication.UnicodeUTF8))

        item8 = QtGui.QTreeWidgetItem(item6)
        item8.setText(0,QtGui.QApplication.translate("MainWindow", "Specification", None, QtGui.QApplication.UnicodeUTF8))

        item9 = QtGui.QTreeWidgetItem(item6)
        item9.setText(0,QtGui.QApplication.translate("MainWindow", "Coefficients", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_4.clear()

        item10 = QtGui.QTreeWidgetItem(self.treeWidget_4)
        item10.setText(0,QtGui.QApplication.translate("MainWindow", "Scenario Configuration", None, QtGui.QApplication.UnicodeUTF8))

        item11 = QtGui.QTreeWidgetItem(self.treeWidget_4)
        item11.setText(0,QtGui.QApplication.translate("MainWindow", "Run Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_5.clear()

        item12 = QtGui.QTreeWidgetItem(self.treeWidget_5)
        item12.setText(0,QtGui.QApplication.translate("MainWindow", "Indicator Set", None, QtGui.QApplication.UnicodeUTF8))

        item13 = QtGui.QTreeWidgetItem(item12)
        item13.setText(0,QtGui.QApplication.translate("MainWindow", "Table", None, QtGui.QApplication.UnicodeUTF8))

        item14 = QtGui.QTreeWidgetItem(item12)
        item14.setText(0,QtGui.QApplication.translate("MainWindow", "Chart", None, QtGui.QApplication.UnicodeUTF8))

        item15 = QtGui.QTreeWidgetItem(item12)
        item15.setText(0,QtGui.QApplication.translate("MainWindow", "Map", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapView), QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Details Pane #1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "Details Pane #2", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_detailView), QtGui.QApplication.translate("MainWindow", "Detail View", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Trend View", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15pt; font-weight:600; font-style:italic; text-decoration: underline;\">An Image or Trend Graph</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Model Selection Matrix", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("MainWindow", "Foo", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setVerticalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("MainWindow", "Bar", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setVerticalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("MainWindow", "Test1", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("MainWindow", "Test2", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem3)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_trendView), QtGui.QApplication.translate("MainWindow", "Trend View", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_modelFlow), QtGui.QApplication.translate("MainWindow", "Model Flow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_runStatus), QtGui.QApplication.translate("MainWindow", "Run Status", None, QtGui.QApplication.UnicodeUTF8))
        self.menuModel_Manager.setTitle(QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRun_Manager.setTitle(QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUtilities.setTitle(QtGui.QApplication.translate("MainWindow", "Utilities", None, QtGui.QApplication.UnicodeUTF8))
        self.menuData_Manager.setTitle(QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.menuResults_Manager.setTitle(QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMap.setTitle(QtGui.QApplication.translate("MainWindow", "Map", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc
