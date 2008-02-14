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

from opus_gui.config.datamanager.configurescript_ui import Ui_ConfigureScriptGui

import random

class ConfigureScriptGui(QDialog, Ui_ConfigureScriptGui):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent.mainwindow, fl)
        self.setupUi(self)
        self.parent = parent
        self.vars = {}
        # To test... add some dummy vars
        self.vboxlayout = QVBoxLayout(self.variableBox)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.test_widget = []
        self.hboxlayout = []
        self.test_text = []
        self.test_line = []
        self.numberofvars = random.randint(2, 10)
        for x in xrange(0,self.numberofvars):
            print "Looping::%d" % (x)
            self.test_widget.insert(x,QWidget(self.variableBox))
            self.test_widget[x].setObjectName(QString("test_widget").append(str(x)))
            self.hboxlayout.insert(x,QHBoxLayout(self.test_widget[x]))
            self.hboxlayout[x].setMargin(4)
            self.hboxlayout[x].setSpacing(4)
            self.hboxlayout[x].setObjectName(QString("hboxlayout").append(str(x)))
            self.test_text.insert(x,QLabel(self.test_widget[x]))
            self.test_text[x].setObjectName(QString("test1_text").append(str(x)))
            self.test_text[x].setText(QString("test").append(str(x)))
            self.hboxlayout[x].addWidget(self.test_text[x])
            self.test_line.insert(x,QLineEdit(self.test_widget[x]))
            self.test_line[x].setEnabled(True)
            self.test_line[x].setMinimumSize(QSize(200,0))
            self.test_line[x].setObjectName(QString("test_line").append(str(x)))
            self.hboxlayout[x].addWidget(self.test_line[x])
            self.vboxlayout.addWidget(self.test_widget[x])
        
    def on_createConfig_released(self):
        print "create pressed"
        for x in xrange(0,self.numberofvars):
            self.vars[self.test_text[x].text()] = self.test_line[x].text()
        for key,val in self.vars.iteritems():
            print "Key: %s , Val: %s" % (key,val)
        self.close()

    def on_cancelConfig_released(self):
        print "cancel pressed"
        self.close()
