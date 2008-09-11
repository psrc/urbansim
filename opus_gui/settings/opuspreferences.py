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

# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# UI specific includes
from opuspreferences_ui import Ui_PreferencesDialog

class UrbansimPreferencesGui(QDialog, Ui_PreferencesDialog):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self._initSpinBoxes()
        self._initRadioButtions()
        
        #hook up the buttons
        QObject.connect(self.okButton, SIGNAL("released()"), self.okay)
        QObject.connect(self.applyButton, SIGNAL("released()"), self.apply)
        QObject.connect(self.cancelButton, SIGNAL("released()"), self.cancel)
        
        #make the font size of the new window match the mainwindow
        #this only needs to happen on init, once the window is a child of
        #the main window it's font will be changed through the main window
        #self.changeFontSize(self.mainwindow.font_size_adjust)
        
    def _initSpinBoxes(self):
        self.menuFontSizeSpinBox.setValue(self.mainwindow.getMenuFontSize())
        self.mainTabsFontSizeSpinBox.setValue(self.mainwindow.getMainTabsFontSize())
        self.generalTextFontSizeSpinBox.setValue(self.mainwindow.getGeneralTextFontSize())

    def _initRadioButtions(self):
        self.prevProjPrefRadioButton.setChecked(self.mainwindow.getOpenLatestProject())
    
    
    def apply(self):
        #apply font change
        self.mainwindow.setMenuFontSize(self.menuFontSizeSpinBox.value())
        self.mainwindow.setMainTabsFontSize(self.mainTabsFontSizeSpinBox.value())
        self.mainwindow.setGeneralTextFontSize(self.generalTextFontSizeSpinBox.value())
        self.mainwindow.setOpenLatestProject(self.prevProjPrefRadioButton.isChecked())
        self.mainwindow.changeFontSize()
        self.mainwindow.updateFontSettingsNode()
        self.mainwindow.updateProjectHistoryNode()
        self.mainwindow.saveGuiConfig()


    def okay(self):
        self.apply()
        self.close()

    def cancel(self):
        self.close()
