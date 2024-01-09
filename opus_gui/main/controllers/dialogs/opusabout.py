# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 



# PyQt5 includes for python bindings to QT
from PyQt5.QtCore  import  QUrl, pyqtSlot
from PyQt5.QtWidgets import QDialog, QDesktopServices
# UI specific includes
from opus_gui.main.views.ui_opusabout import Ui_UrbansimAbout

class UrbansimAboutGui(QDialog, Ui_UrbansimAbout):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow

    @pyqtSlot()
    def on_webPushButton_clicked(self):
        #print "webPushButton pressed"
        QDesktopServices.openUrl(QUrl(("http://www.urbansim.org/")))

    @pyqtSlot()
    def on_docPushButton_clicked(self):
        #print "docPushButton pressed"
        QDesktopServices.openUrl(QUrl(("http://www.urbansim.org/docs/opus-userguide/")))

    @pyqtSlot()
    def on_licensePushButton_clicked(self):
        #print "licensePushButton pressed"
        QDesktopServices.openUrl(QUrl(("http://www.gnu.org/copyleft/gpl.html")))

    @pyqtSlot()
    def on_buttonCancel_clicked(self):
        #print "cancelPushButton pressed"
        self.close()
