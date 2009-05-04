# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from PyQt4.QtCore import QString, QByteArray
from PyQt4.QtGui import QWidget, QGroupBox, QVBoxLayout, QIcon, QGridLayout, QLabel, QImage, QPainter, QPixmap, QScrollArea, QSizePolicy, QMovie


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
        
        if QByteArray('gif') in QMovie.supportedFormats():
            # QMovie supports gif animations
            movie = QMovie(QString(file_path), QByteArray(), self)
            movie.setCacheMode(QMovie.CacheAll)
            self.label.setMovie(movie)
            movie.start() 
        else:
            #QMovie does not support gif animations
            self.label.setWordWrap(True)
            self.label.setFixedHeight(450)
            self.label.setFixedWidth(600)
            self.label.setText("The Animated Mapnik map was shown in an external viewer. This is because the version of Qt/PyQt in use has not been configured to support gif animations.")
            # Note: the PATH environment variable must contain the filepath to i_view32 (Win) or to animate (Mac & Linux)
            if os.name == 'nt':
            # in Windows, view the gif with IrfanView
                os.system('i_view32 %s /title=%s /B' % (file_path, visualization.table_name))
            else:
            # in Mac and Linux, view the gif with ImageMagick (ImageMagick requires the X Window System that Windows does not have)
                os.system('animate %s &' % file_path)
        
        self.scroll.setWidget(self.label)
        self.widgetLayout.addWidget(self.scroll)

        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = visualization.table_name

    def removeElement(self):
        return True
    
    


    
