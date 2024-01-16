# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from PyQt5.QtCore  import  QByteArray
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtGui import QIcon, QImage,  QPainter, QPixmap, QMovie

class ViewAnimationForm(QWidget):
    def __init__(self, visualization, parent_widget = None):
        
        QWidget.__init__(self, parent_widget)
        self.inGui = False
        self.visualization = visualization

        size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widgetLayout = QGridLayout(self)
        self.setSizePolicy(size)

        self.scroll = QScrollArea()
        file_path = self.visualization.get_file_path()       
        self.label = QLabel()
        
        movie = QMovie((file_path), QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        self.label.setMovie(movie)
        movie.start() 
        
        self.scroll.setWidget(self.label)
        self.widgetLayout.addWidget(self.scroll)

        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = visualization.table_name

    def removeElement(self):
        return True
    
    


    
