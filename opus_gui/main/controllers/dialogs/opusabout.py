# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString, QUrl
from PyQt4.QtGui import QDialog, QDesktopServices
# UI specific includes
from opus_gui.main.views.ui_opusabout import Ui_UrbansimAbout

class UrbansimAboutGui(QDialog, Ui_UrbansimAbout):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow

    def on_webPushButton_released(self):
        #print "webPushButton pressed"
        QDesktopServices.openUrl(QUrl(QString("http://www.urbansim.org/")))

    def on_docPushButton_released(self):
        #print "docPushButton pressed"
        QDesktopServices.openUrl(QUrl(QString("http://www.urbansim.org/docs/opus-userguide/")))

    def on_licensePushButton_released(self):
        #print "licensePushButton pressed"
        QDesktopServices.openUrl(QUrl(QString("http://www.gnu.org/copyleft/gpl.html")))

    def on_buttonCancel_released(self):
        #print "cancelPushButton pressed"
        self.close()
