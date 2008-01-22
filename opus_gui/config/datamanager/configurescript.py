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

from configurescript_ui import Ui_ConfigureScriptGui

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

        self.test1_widget = QWidget(self.variableBox)
        self.test1_widget.setObjectName("test1_widget")
        self.hboxlayout1 = QHBoxLayout(self.test1_widget)
        self.hboxlayout1.setMargin(4)
        self.hboxlayout1.setSpacing(4)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.test1_text = QLabel(self.test1_widget)
        self.test1_text.setObjectName("test1_text")
        self.test1_text.setText(QString("test1"))
        self.hboxlayout1.addWidget(self.test1_text)
        self.test1_line = QLineEdit(self.test1_widget)
        self.test1_line.setEnabled(True)
        self.test1_line.setMinimumSize(QSize(200,0))
        self.test1_line.setObjectName("test1_line")
        self.hboxlayout1.addWidget(self.test1_line)
        self.vboxlayout.addWidget(self.test1_widget)
        
        self.test2_widget = QWidget(self.variableBox)
        self.test2_widget.setObjectName("test2_widget")
        self.hboxlayout2 = QHBoxLayout(self.test2_widget)
        self.hboxlayout2.setMargin(4)
        self.hboxlayout2.setSpacing(4)
        self.hboxlayout2.setObjectName("hboxlayout1")
        self.test2_text = QLabel(self.test2_widget)
        self.test2_text.setObjectName("test2_text")
        self.test2_text.setText(QString("test2"))
        self.hboxlayout2.addWidget(self.test2_text)
        self.test2_line = QLineEdit(self.test2_widget)
        self.test2_line.setEnabled(True)
        self.test2_line.setMinimumSize(QSize(200,0))
        self.test2_line.setObjectName("test2_line")
        self.hboxlayout2.addWidget(self.test2_line)
        self.vboxlayout.addWidget(self.test2_widget)

    def on_createConfig_released(self):
        print "create pressed"
        self.vars[self.test1_text.text()] = self.test1_line.text()
        self.vars[self.test2_text.text()] = self.test2_line.text()
        #self.vars.append(["test2", self.test2_line.text()])
        for key,val in self.vars.iteritems():
            print "Key: %s , Val: %s" % (key,val)
        self.close()

    def on_cancelConfig_released(self):
        print "cancel pressed"
        self.close()
