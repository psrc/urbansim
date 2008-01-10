# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'january_mockup.ui'
#
# Created: Thu Jan 10 11:20:11 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,950,951).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(9,9,932,893))
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.toolBox = QtGui.QToolBox(self.splitter)
        self.toolBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setBaseSize(QtCore.QSize(0,0))
        self.toolBox.setObjectName("toolBox")

        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,529,779))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.toolBox_2 = QtGui.QToolBox(self.datamanager_page)
        self.toolBox_2.setObjectName("toolBox_2")

        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0,0,491,677))
        self.page.setObjectName("page")

        self.vboxlayout = QtGui.QVBoxLayout(self.page)
        self.vboxlayout.setObjectName("vboxlayout")

        self.treeWidget = QtGui.QTreeWidget(self.page)
        self.treeWidget.setObjectName("treeWidget")
        self.vboxlayout.addWidget(self.treeWidget)
        self.toolBox_2.addItem(self.page,QtGui.QIcon(":/Images/Images/database_link.png"),"")

        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0,0,491,675))
        self.page_2.setObjectName("page_2")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.page_2)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.treeWidget_2 = QtGui.QTreeWidget(self.page_2)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.vboxlayout1.addWidget(self.treeWidget_2)
        self.toolBox_2.addItem(self.page_2,QtGui.QIcon(":/Images/Images/database.png"),"")

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.page_3)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.treeWidget_6 = QtGui.QTreeWidget(self.page_3)
        self.treeWidget_6.setObjectName("treeWidget_6")
        self.vboxlayout2.addWidget(self.treeWidget_6)
        self.toolBox_2.addItem(self.page_3,QtGui.QIcon(":/Images/Images/folder_database.png"),"")
        self.gridlayout.addWidget(self.toolBox_2,0,0,1,1)
        self.toolBox.addItem(self.datamanager_page,QtGui.QIcon(":/Images/Images/database_table.png"),"")

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.toolBox.addItem(self.page_4,QtGui.QIcon(":/Images/Images/cog.png"),"")

        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")
        self.toolBox.addItem(self.page_5,QtGui.QIcon(":/Images/Images/chart_organisation.png"),"")

        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName("page_6")
        self.toolBox.addItem(self.page_6,QtGui.QIcon(":/Images/Images/map_go.png"),"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3,"")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,950,21))
        self.menubar.setObjectName("menubar")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")

        self.mpActionPan = QtGui.QAction(MainWindow)
        self.mpActionPan.setObjectName("mpActionPan")

        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")

        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")

        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")

        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionOpen)
        self.menuProject.addAction(self.actionSave)
        self.menuProject.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(3)
        self.toolBox_2.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpusGui", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.clear()

        item = QtGui.QTreeWidgetItem(self.treeWidget)
        item.setText(0,QtGui.QApplication.translate("MainWindow", "trondheim", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item.setText(1,QtGui.QApplication.translate("MainWindow", "MySQL", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("MainWindow", "hostname", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item1.setText(1,QtGui.QApplication.translate("MainWindow", "trondheim.cs.washington.edu", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QTreeWidgetItem(item)
        item2.setText(0,QtGui.QApplication.translate("MainWindow", "username", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item2.setText(1,QtGui.QApplication.translate("MainWindow", "urbansim", None, QtGui.QApplication.UnicodeUTF8))

        item3 = QtGui.QTreeWidgetItem(item)
        item3.setText(0,QtGui.QApplication.translate("MainWindow", "password", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(0,QtGui.QIcon(":/Images/Images/lock.png"))
        item3.setText(1,QtGui.QApplication.translate("MainWindow", "**********", None, QtGui.QApplication.UnicodeUTF8))

        item4 = QtGui.QTreeWidgetItem(item)
        item4.setText(0,QtGui.QApplication.translate("MainWindow", "port", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item4.setText(1,QtGui.QApplication.translate("MainWindow", "3306", None, QtGui.QApplication.UnicodeUTF8))

        item5 = QtGui.QTreeWidgetItem(item)
        item5.setText(0,QtGui.QApplication.translate("MainWindow", "use_environment_variables", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item5.setText(1,QtGui.QApplication.translate("MainWindow", "True", None, QtGui.QApplication.UnicodeUTF8))

        item6 = QtGui.QTreeWidgetItem(self.treeWidget)
        item6.setText(0,QtGui.QApplication.translate("MainWindow", "aarhus", None, QtGui.QApplication.UnicodeUTF8))
        item6.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item6.setText(1,QtGui.QApplication.translate("MainWindow", "PostgreSQL", None, QtGui.QApplication.UnicodeUTF8))

        item7 = QtGui.QTreeWidgetItem(item6)
        item7.setText(0,QtGui.QApplication.translate("MainWindow", "hostname", None, QtGui.QApplication.UnicodeUTF8))
        item7.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item7.setText(1,QtGui.QApplication.translate("MainWindow", "aarhus.cs.washington.edu", None, QtGui.QApplication.UnicodeUTF8))

        item8 = QtGui.QTreeWidgetItem(item6)
        item8.setText(0,QtGui.QApplication.translate("MainWindow", "username", None, QtGui.QApplication.UnicodeUTF8))
        item8.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item8.setText(1,QtGui.QApplication.translate("MainWindow", "postgres", None, QtGui.QApplication.UnicodeUTF8))

        item9 = QtGui.QTreeWidgetItem(item6)
        item9.setText(0,QtGui.QApplication.translate("MainWindow", "password", None, QtGui.QApplication.UnicodeUTF8))
        item9.setIcon(0,QtGui.QIcon(":/Images/Images/lock.png"))
        item9.setText(1,QtGui.QApplication.translate("MainWindow", "**************", None, QtGui.QApplication.UnicodeUTF8))

        item10 = QtGui.QTreeWidgetItem(item6)
        item10.setText(0,QtGui.QApplication.translate("MainWindow", "port", None, QtGui.QApplication.UnicodeUTF8))
        item10.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item10.setText(1,QtGui.QApplication.translate("MainWindow", "5432", None, QtGui.QApplication.UnicodeUTF8))

        item11 = QtGui.QTreeWidgetItem(item6)
        item11.setText(0,QtGui.QApplication.translate("MainWindow", "use_environment_variables", None, QtGui.QApplication.UnicodeUTF8))
        item11.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item11.setText(1,QtGui.QApplication.translate("MainWindow", "False", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Database Server Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.clear()

        item12 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item12.setText(0,QtGui.QApplication.translate("MainWindow", "working_database", None, QtGui.QApplication.UnicodeUTF8))
        item12.setIcon(0,QtGui.QIcon(":/Images/Images/database.png"))
        item12.setText(1,"")

        item13 = QtGui.QTreeWidgetItem(item12)
        item13.setText(0,QtGui.QApplication.translate("MainWindow", "database_name", None, QtGui.QApplication.UnicodeUTF8))
        item13.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item13.setText(1,QtGui.QApplication.translate("MainWindow", "psrc_2005_data_workspace", None, QtGui.QApplication.UnicodeUTF8))

        item14 = QtGui.QTreeWidgetItem(item12)
        item14.setText(0,QtGui.QApplication.translate("MainWindow", "database_server_connection", None, QtGui.QApplication.UnicodeUTF8))
        item14.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item14.setText(1,QtGui.QApplication.translate("MainWindow", "trondheim", None, QtGui.QApplication.UnicodeUTF8))

        item15 = QtGui.QTreeWidgetItem(item12)
        item15.setText(0,QtGui.QApplication.translate("MainWindow", "schema", None, QtGui.QApplication.UnicodeUTF8))
        item15.setIcon(0,QtGui.QIcon(":/Images/Images/field.png"))
        item15.setText(1,QtGui.QApplication.translate("MainWindow", "none", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Databases", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_6.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_6.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_6.clear()

        item16 = QtGui.QTreeWidgetItem(self.treeWidget_6)
        item16.setText(0,QtGui.QApplication.translate("MainWindow", "C:\\urbansim_cache", None, QtGui.QApplication.UnicodeUTF8))
        item16.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item16.setText(1,"")

        item17 = QtGui.QTreeWidgetItem(item16)
        item17.setText(0,QtGui.QApplication.translate("MainWindow", "eugene", None, QtGui.QApplication.UnicodeUTF8))
        item17.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item17.setText(1,"")

        item18 = QtGui.QTreeWidgetItem(item17)
        item18.setText(0,QtGui.QApplication.translate("MainWindow", "eugene_1980_baseyear_cache", None, QtGui.QApplication.UnicodeUTF8))
        item18.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item18.setText(1,"")

        item19 = QtGui.QTreeWidgetItem(item18)
        item19.setText(0,QtGui.QApplication.translate("MainWindow", "1980", None, QtGui.QApplication.UnicodeUTF8))
        item19.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item19.setText(1,"")

        item20 = QtGui.QTreeWidgetItem(item19)
        item20.setText(0,QtGui.QApplication.translate("MainWindow", "gridcells", None, QtGui.QApplication.UnicodeUTF8))
        item20.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item20.setText(1,"")

        item21 = QtGui.QTreeWidgetItem(item20)
        item21.setText(0,QtGui.QApplication.translate("MainWindow", "city_id", None, QtGui.QApplication.UnicodeUTF8))
        item21.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item21.setText(1,"")

        item22 = QtGui.QTreeWidgetItem(item20)
        item22.setText(0,QtGui.QApplication.translate("MainWindow", "plan_type_id", None, QtGui.QApplication.UnicodeUTF8))
        item22.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item22.setText(1,"")

        item23 = QtGui.QTreeWidgetItem(item20)
        item23.setText(0,QtGui.QApplication.translate("MainWindow", "industrial_sqft", None, QtGui.QApplication.UnicodeUTF8))
        item23.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item23.setText(1,"")

        item24 = QtGui.QTreeWidgetItem(item19)
        item24.setText(0,QtGui.QApplication.translate("MainWindow", "households", None, QtGui.QApplication.UnicodeUTF8))
        item24.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item24.setText(1,"")

        item25 = QtGui.QTreeWidgetItem(item24)
        item25.setText(0,QtGui.QApplication.translate("MainWindow", "household_id", None, QtGui.QApplication.UnicodeUTF8))
        item25.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item25.setText(1,"")

        item26 = QtGui.QTreeWidgetItem(item24)
        item26.setText(0,QtGui.QApplication.translate("MainWindow", "grid_id", None, QtGui.QApplication.UnicodeUTF8))
        item26.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item26.setText(1,"")

        item27 = QtGui.QTreeWidgetItem(item24)
        item27.setText(0,QtGui.QApplication.translate("MainWindow", "persons", None, QtGui.QApplication.UnicodeUTF8))
        item27.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item27.setText(1,"")

        item28 = QtGui.QTreeWidgetItem(self.treeWidget_6)
        item28.setText(0,QtGui.QApplication.translate("MainWindow", "X:\\cache_backup", None, QtGui.QApplication.UnicodeUTF8))
        item28.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item28.setText(1,"")
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3), QtGui.QApplication.translate("MainWindow", "Opus Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), QtGui.QApplication.translate("MainWindow", "Scenario Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Python", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
