# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# PyQt5 includes for python bindings to QT
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog

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
        # This is to assure that stateChanged is fired if necessary,
        # i.e. if the initial state of the check box is "unchecked".
        # In this case, the "latest tab" check box has to be disabled,
        # which is handled by the stateChanged handler.
        assert(self.prevProjPrefCheckBox.isChecked())
        
        load_on_start = self.gui_config.load_latest_on_start
        self.prevProjPrefCheckBox.setChecked(load_on_start)
        tab_on_start = self.gui_config.load_latest_tab_on_start
        self.prevProjPrefTabCheckBox.setChecked(tab_on_start)

    @pyqtSlot(int)
    def on_prevProjPrefCheckBox_stateChanged(self, newState):
        self.prevProjPrefTabCheckBox.setEnabled(newState != 0)

    @pyqtSlot()
    def on_applyButton_clicked(self):
        # Apply the changes
        fonts = self.gui_config.fonts
        fonts['menu'] = self.menuFontSizeSpinBox.value()
        fonts['tabs'] = self.mainTabsFontSizeSpinBox.value()
        fonts['general'] = self.generalTextFontSizeSpinBox.value()

        self.gui_config.load_latest_on_start = \
            self.prevProjPrefCheckBox.isChecked()
        self.gui_config.load_latest_tab_on_start = \
            self.prevProjPrefTabCheckBox.isChecked()

        self.opus_gui_window.updateFontSize()

        self.gui_config.save()

    @pyqtSlot()
    def on_okButton_clicked(self):
        self.on_applyButton_clicked()
        self.close()

    @pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()
