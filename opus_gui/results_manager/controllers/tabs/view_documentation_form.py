# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QWidget, QGroupBox, QVBoxLayout, QIcon

class ViewDocumentationForm(QWidget):
    def __init__(self, mainwindow, indicator_node):
        QWidget.__init__(self, mainwindow)
        self.mainwindow = mainwindow
        self.inGui = False

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)

        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = indicator_node.nodeName()

        url_val = get_child_values(
                       parent = indicator_node,
                       child_names = ['documentation_link'])

        if 'documentation_link' in url_val:
            url = url_val['documentation_link']
        else:
            return
