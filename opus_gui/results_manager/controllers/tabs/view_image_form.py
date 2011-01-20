# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from PyQt4.QtCore import QString
from PyQt4.QtGui import QWidget, QGroupBox, QVBoxLayout, QIcon, QGridLayout, QLabel, QImage, QPainter, QPixmap, QScrollArea, QSizePolicy


class ViewImageForm(QWidget):
    def __init__(self, visualization, parent_widget = None):
        QWidget.__init__(self, parent_widget)
        self.inGui = False
        self.visualization = visualization

        size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widgetLayout = QGridLayout(self)
        self.setSizePolicy(size)

        self.scroll = QScrollArea()
        file_path = self.visualization.get_file_path()

        self.lbl_image = QImage(QString(file_path))
        self.label = QLabel()
        self.label.setPixmap(QPixmap.fromImage(self.lbl_image))
        self.scroll.setWidget(self.label)
        self.widgetLayout.addWidget(self.scroll)

        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = visualization.table_name

    def removeElement(self):
        return True
