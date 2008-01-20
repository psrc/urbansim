# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# UI specific includes
from opusabout_ui import Ui_UrbansimAbout

class UrbansimAboutGui(QDialog, Ui_UrbansimAbout):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent

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
