# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

'''
A custom MessageBox class to replace much of QT's very inflexible QMessageBox functionality.

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
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QString, pyqtSlot
from PyQt4.QtGui import QDialog
# UI specific includes
from opus_gui.util.icon_library import IconLibrary
from opus_gui.main.views.ui_message_box import Ui_MessageBox

class MessageBox(QDialog, Ui_MessageBox):
    ERROR = 0
    WARNING = 1
    INFORMATION = 2

    def __init__(self, mainwindow, text, detailed_text = None, mode = ERROR, flags = Qt.Dialog):
        QDialog.__init__(self, mainwindow, Qt.Dialog|Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        if mode == MessageBox.ERROR:
            img = IconLibrary.icon('messagebox_critical') #QPixmap(':/Images/Images/big_error.png')
        elif mode == MessageBox.WARNING:
            img = IconLibrary.icon('messagebox_warning') # QPixmap(':/Images/Images/big_warning.png')
        elif mode == MessageBox.INFORMATION:
            img = IconLibrary.icon('messagebox_info') # QPixmap(':/Images/Images/big_information.png')
        pixmap = img.pixmap(64, 64)
        self.lblImage.setPixmap(pixmap)
        self.lblText.setText('<qt><b>%s</b></qt>'%text)
        if detailed_text:
            self.lblDetailText.setText(QString(detailed_text))
        else:
            self.pbnShowDetails.hide()
        self.details_showing = True
        self.detail_expansion_size = self.frame_details.height() + self.layout().spacing()
        self.on_pbnShowDetails_clicked()

    @pyqtSlot()
    def on_btnOk_clicked(self):
        self.close()

    @pyqtSlot()
    def on_pbnShowDetails_clicked(self):
        if self.details_showing:
            self.detail_expansion_size = self.frame_details.height() + self.layout().spacing()
            self.details_showing = False
            self.pbnShowDetails.setText('Show Details...')
            self.pbnShowDetails.setIcon(IconLibrary.icon('arrow_right'))
            self.setUpdatesEnabled(False)
            self.frame_details.hide()
            self.resize(self.width(), self.height() - self.detail_expansion_size)
            self.setUpdatesEnabled(True)
            self.adjustSize()
        else:
            self.pbnShowDetails.setText('Hide Details...')
            self.pbnShowDetails.setIcon(IconLibrary.icon('arrow_down'))
            self.details_showing = True
            self.frame_details.show()
            self.adjustSize()

    @staticmethod
    def warning(mainwindow, text, detailed_text = None):
        frm = MessageBox(mainwindow = mainwindow,
                        text = text,
                        detailed_text = detailed_text,
                        mode = MessageBox.WARNING)
        frm.activateWindow()
        frm.raise_()
        frm.exec_()

    @staticmethod
    def error(mainwindow, text, detailed_text = None):
        frm = MessageBox(mainwindow = mainwindow,
                        text = text,
                        detailed_text = detailed_text,
                        mode = MessageBox.ERROR)
        frm.activateWindow()
        frm.raise_()
        frm.exec_()

    @staticmethod
    def information(mainwindow, text, detailed_text = None):
        frm = MessageBox(mainwindow = mainwindow,
                        text = text,
                        detailed_text = detailed_text,
                        mode = MessageBox.INFORMATION)
        frm.activateWindow()
        frm.raise_()
        frm.exec_()

if __name__ == '__main__':
    import PyQt4.QtGui
    from opus_gui.main.views import opusmain_rc
    app = PyQt4.QtGui.QApplication([], True)
    w = PyQt4.QtGui.QFrame()
    MessageBox.information(w, 'test', 'detail')
    MessageBox.warning(w, 'test', 'detail')
    MessageBox.error(w, 'test', 'detail')