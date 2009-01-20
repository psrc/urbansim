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
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QDialog

# UI specific includes
from opus_gui.main.views.ui_opuspreferences import Ui_PreferencesDialog

class UrbansimPreferencesGui(QDialog, Ui_PreferencesDialog):
    def __init__(self, opus_gui_window):
        '''
        Dialogbox for editing GUI preferences.
        @param opus_gui_window (OpusGui): Parent Opus Main Window
        '''
        QDialog.__init__(self, opus_gui_window)
        self.setupUi(self)
        self.opus_gui_window = opus_gui_window
        self.gui_config = opus_gui_window.gui_config
        self._initSpinBoxes()
        self._initRadioButtions()

    def _initSpinBoxes(self):
        fonts = self.gui_config.fonts
        self.menuFontSizeSpinBox.setValue(fonts['menu'])
        self.mainTabsFontSizeSpinBox.setValue(fonts['tabs'])
        self.generalTextFontSizeSpinBox.setValue(fonts['general'])

    def _initRadioButtions(self):
        load_on_start = self.gui_config.load_latest_on_start
        self.prevProjPrefCheckBox.setChecked(load_on_start)

    def on_applyButton_released(self):
        # Apply the changes
        fonts = self.gui_config.fonts
        fonts['menu'] = self.menuFontSizeSpinBox.value()
        fonts['tabs'] = self.mainTabsFontSizeSpinBox.value()
        fonts['general'] = self.generalTextFontSizeSpinBox.value()

        self.gui_config.load_latest_on_start = \
            self.prevProjPrefCheckBox.isChecked()

        self.opus_gui_window.updateFontSize()

        self.gui_config.save()

    def on_okButton_released(self):
        self.on_applyButton_released()
        self.close()

    def on_cancelButton_released(self):
        self.close()
