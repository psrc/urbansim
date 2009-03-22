# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

'''
A custom MessageBox class to replace much of QT's very inflexible QMessageBox functionanlity.

MessageBox provides a way to display informational, warning, and error messages, 
along with details (i.e. a stacktrace or more information on what may have caused 
an error). The different modes only change which icon is displayed. 
Unlike QMessageBox, the window can be resized.

The interface is very similar to QMessageBox. Here are some sample uses:

   ...
   except Exception, e:
        errorinfo = formatExceptionInfo()
        MessageBox.error(mainwindow = self.mainwindow,
                          text = "There was a problem running the simulation.",
                          detailed_text = errorinfo)

   ...
   msg = 'The table %s has been truncated to %i rows because of memory limitations.'%(visualization.table_name,limit)
   detailed_msg = '<qt>To view the full results, open the following file:<br><br><small>%s</small></qt>'%visualization.get_file_path()
   MessageBox.warning(mainwindow = self.mainwindow,
                                  text = msg,
                                  detailed_text = detailed_msg)

   ...
   run_data = '\n'.join(added_runs)
   msg = 'The following simulation runs have been automatically added to the results manager:\n\n%s'%run_data
   MessageBox.information(mainwindow = self.mainwindow,
                              text = 'Simulation runs have been added to this project.',
                              detailed_text = msg)
'''


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QPixmap
# UI specific includes
from opus_gui.main.views.ui_message_box import Ui_dlgMessageBox
from PyQt4.QtCore import Qt

class MessageBox(QDialog, Ui_dlgMessageBox):
    ERROR = 0
    WARNING = 1
    INFORMATION = 2
    
    def __init__(self, mainwindow, text, detailed_text = None, mode = ERROR, flags = Qt.Dialog):
        QDialog.__init__(self, mainwindow, flags)
        self.setupUi(self)
        if mode == MessageBox.ERROR:
            img = QPixmap(':/Images/Images/big_error.png')
        elif mode == MessageBox.WARNING:
            img = QPixmap(':/Images/Images/big_warning.png')
        elif mode == MessageBox.INFORMATION:
            img = QPixmap(':/Images/Images/big_information.png')            

        self.lblImage.setPixmap(img)
        self.lblText.setText('<qt><b>%s</b></qt>'%text)
        self.lblDetailText.setText(QString(detailed_text))
        if detailed_text != '' and detailed_text != None:
            self.lblDetailText.setText(QString(detailed_text))
        else:
            self.pbnShowDetails.hide()
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
            self.setUpdatesEnabled(False)
            self.saDetails.hide()
            self.resize(self.width(), self.height() - self.detail_expansion_size)
            self.setUpdatesEnabled(True)
            self.adjustSize()
        else:
            self.pbnShowDetails.setText('Hide Details...')
            self.details_showing = True
            self.saDetails.show()   
            self.adjustSize()
            
    def warning(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = MessageBox(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = MessageBox.WARNING,
                        flags = flags)
        frm.show()

    def error(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = MessageBox(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = MessageBox.ERROR,
                        flags = flags)
        frm.show()

    def information(mainwindow, text, detailed_text, flags = Qt.Dialog|Qt.WindowMaximizeButtonHint):
        frm = MessageBox(mainwindow = mainwindow, 
                        text = text, 
                        detailed_text = detailed_text,
                        mode = MessageBox.INFORMATION,
                        flags = flags)
        frm.show()

        
    warning = staticmethod(warning)    
    error = staticmethod(error)
    information = staticmethod(information)