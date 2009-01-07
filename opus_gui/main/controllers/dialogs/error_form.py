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
from PyQt4.QtCore import QString, QSize
from PyQt4.QtGui import QDialog, QPixmap
# UI specific includes
from opus_gui.main.views.ui_error_form import Ui_dlgErrorForm
from opus_core.misc import directory_path_from_opus_path
import os
from PyQt4.QtCore import Qt

class ErrorForm(QDialog, Ui_dlgErrorForm):
    ERROR = 0
    WARNING = 1
    INFORMATION = 2
    
    def __init__(self, mainwindow, text, detailed_text, mode = ERROR, flags = Qt.Dialog):
        QDialog.__init__(self, mainwindow, flags)
        self.setupUi(self)
        if mode == ErrorForm.ERROR:
            img = QPixmap(':/Images/Images/big_error.png')
        elif mode == ErrorForm.WARNING:
            img = QPixmap(':/Images/Images/big_warning.png')
        elif mode == ErrorForm.INFORMATION:
            img = QPixmap(':/Images/Images/big_information.png')            

        self.lblImage.setPixmap(img)
        self.lblText.setText('<qt><b>%s</b></qt>'%text)
        self.lblDetailText.setText(QString(detailed_text))
        self.details_showing = True
        self.detail_expansion_size = self.saDetails.height() + self.gridLayout.verticalSpacing()
        self.on_pbnShowDetails_released()
        
    def on_btnOk_released(self):
        self.close()
        
    def on_pbnShowDetails_released(self):
        if self.details_showing:
            self.detail_expansion_size = self.saDetails.height() + self.gridLayout.verticalSpacing()
            self.details_showing = False
            self.pbnShowDetails.setText('Show Details...')
            #self.gridLayout.removeWidget(self.saDetails)
            self.saDetails.hide()
            self.resize(self.width(), self.height() - self.detail_expansion_size)
            self.adjustSize()
        else:
            self.pbnShowDetails.setText('Hide Details...')
            self.details_showing = True
            #self.resize(self.width(), self.height() + self.detail_expansion_size )
            self.saDetails.show()   

            #self.gridLayout.addWidget(self.saDetails)
            self.adjustSize()
            
    def warning(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = ErrorForm(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = ErrorForm.WARNING,
                        flags = flags)
        frm.show()

    def error(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = ErrorForm(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = ErrorForm.ERROR,
                        flags = flags)
        frm.show()

    def information(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = ErrorForm(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = ErrorForm.INFORMATION,
                        flags = flags)
        frm.show()

        
    warning = staticmethod(warning)    
    error = staticmethod(error)
    information = staticmethod(information)