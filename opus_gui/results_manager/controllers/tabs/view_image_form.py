# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#


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
