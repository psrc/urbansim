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

from opus_gui.config.datamanager.newdbconnection_ui import Ui_NewDbConnectionGui

import random

class NewDbConnectionGui(QDialog, Ui_NewDbConnectionGui):
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
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"),
                        self.databaseTypeSelected)

        self.dbtypearray = [{}, # Nothing here as this corresponds to the no selection case
                            {'host_name':'','protocol':'',
                             'user_name':'','password':'',
                             'use_environment_variables':''}, # Server connections
                            {'Database Path':'/home/aaronr/work/urbansim'}, # ESRI type connections
                            ]
        #self.numberofvars = random.randint(2, 10)
        #for x in xrange(0,self.numberofvars):
        #    print "Looping::%d" % (x)
        #    self.test_widget.insert(x,QWidget(self.variableBox))
        #    self.test_widget[x].setObjectName(QString("test_widget").append(str(x)))
        #    self.hboxlayout.insert(x,QHBoxLayout(self.test_widget[x]))
        #    self.hboxlayout[x].setMargin(4)
        #    self.hboxlayout[x].setSpacing(4)
        #    self.hboxlayout[x].setObjectName(QString("hboxlayout").append(str(x)))
        #    self.test_text.insert(x,QLabel(self.test_widget[x]))
        #    self.test_text[x].setObjectName(QString("test1_text").append(str(x)))
        #    self.test_text[x].setText(QString("test").append(str(x)))
        #    self.hboxlayout[x].addWidget(self.test_text[x])
        #    self.test_line.insert(x,QLineEdit(self.test_widget[x]))
        #    self.test_line[x].setEnabled(True)
        #    self.test_line[x].setMinimumSize(QSize(200,0))
        #    self.test_line[x].setObjectName(QString("test_line").append(str(x)))
        #    self.hboxlayout[x].addWidget(self.test_line[x])
        #    self.vboxlayout.addWidget(self.test_widget[x])
        
    def on_createConfig_released(self):
        print "create pressed - Need to add the config to the XML here..."
        for x in xrange(0,len(self.test_text)):
            self.vars[self.test_text[x].text()] = self.test_line[x].text()
        for key,val in self.vars.iteritems():
            print "Key: %s , Val: %s" % (key,val)
        self.close()

    def on_cancelConfig_released(self):
        print "cancel pressed"
        self.close()

    def databaseTypeSelected(self,index):
        print "Got a new selection"
        for testw in self.test_widget:
            self.vboxlayout.removeWidget(testw)
            testw.hide()
        for key,val in self.dbtypearray[index].iteritems():
            print "Key: %s , Val: %s" % (key,val)
            widgetTemp = QWidget(self.variableBox)
            widgetTemp.setObjectName(QString("test_widget").append(str(key)))
            self.test_widget.append(widgetTemp)
            hlayout = QHBoxLayout(widgetTemp)
            self.hboxlayout.append(hlayout)
            hlayout.setMargin(4)
            hlayout.setSpacing(4)
            hlayout.setObjectName(QString("hboxlayout").append(str(key)))
            test_text = QLabel(widgetTemp)
            self.test_text.append(test_text)
            test_text.setObjectName(QString("test1_text").append(str(key)))
            test_text.setText(QString(str(key)))
            hlayout.addWidget(test_text)
            test_line = QLineEdit(widgetTemp)
            self.test_line.append(test_line)
            test_line.setEnabled(True)
            test_line.setMinimumSize(QSize(200,0))
            test_line.setObjectName(QString("test_line").append(str(key)))
            test_line.setText(QString(str(val)))
            hlayout.addWidget(test_line)
            self.vboxlayout.addWidget(widgetTemp)
        
