# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from lxml import etree

from PyQt4.QtGui import QDialog, QApplication, QFileDialog
from PyQt4.QtGui import QTextEdit, QVBoxLayout, QPushButton
from PyQt4.QtCore import SIGNAL, SLOT, Qt

from opus_core.tools.converter import Converter
from opus_gui.util.converter_gui.ui_converter_gui import Ui_ConverterGui

class ConverterGui(QDialog, Ui_ConverterGui):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.frame_log.setVisible(False)
        self.connect(self.pb_get_filename, SIGNAL('released()'), self._get_filename)
        self.connect(self.pb_get_filename_out, SIGNAL('released()'), self._get_filename)
        self.le_filename.setText('')
        self.converter = None
        self.stack_steps.setCurrentIndex(0)
        self.first_page_msg = ('<b>This is a tool to convert Opus project XML files from version 4.x to 4.3</b><br/>'
                               'Please select the project file that you wish to upgrade.')
        self._display_info(self.first_page_msg, icon = 'info')
        self.resize(self.width(), 0) # compress the dialogs height
        self._enable_save()
        self.le_filename.setFocus()
        self.raise_()

    def _get_filename(self):
        if self.stack_steps.currentIndex() == 0:
            filename = QFileDialog.getOpenFileName()
            widget = self.le_filename
        else:
            filename = QFileDialog.getSaveFileName()
            widget = self.le_filename_out
        if not filename:
            return
        widget.setText(filename)
        widget.setToolTip(filename)
        widget.setCursorPosition(len(filename))

    def _enable_save(self, state = True):
        self.pb_save.setEnabled(state)
        self.pb_save.setText('Save' if state else 'Saved')
        self.le_filename_out.setEnabled(state)
        self.pb_get_filename_out.setEnabled(state)

    def _display_info(self, first_msg, secondary_msg = None, icon = 'info', show_message_button = False):
        # show information in the information box for the current stack index
        # icon can be 'info' (default), 'warning' or 'ok'
        # if show_message_button is True, the show message button is shown (only on page 1)
        icon_widgets = (self.p0_info_icon, self.p0_warning_icon, self.p1_info_icon,
                        self.p1_ok_icon, self.p1_warning_icon)
        for widget in icon_widgets:
            widget.setVisible(False)

        # select widgets based on current page
        if self.stack_steps.currentIndex() == 0:
            icon_widgets = {'info': self.p0_info_icon,
                        'warning': self.p0_warning_icon,
                        'ok': self.p0_info_icon}
            text_widget = self.p0_text
        else:
            icon_widgets = {'info': self.p1_info_icon,
                            'warning': self.p1_warning_icon,
                            'ok': self.p1_ok_icon}
            text_widget = self.p1_text

        self.pb_show_warnings.setVisible(show_message_button)
        icon_widgets[icon].setVisible(True)
        if secondary_msg:
            msg = '<qt>%s<br/>%s</qt>' %(first_msg, secondary_msg)
        else:
            msg = '<qt>%s</qt>' %first_msg
        text_widget.setText(msg)

    def on_pb_log_released(self):
        self.frame_log.setVisible(self.pb_log.isChecked())
        self.frame_page2.setVisible(not self.pb_log.isChecked())

    def on_pb_next_released(self):
        # Try to convert the given file. If it was (partly or completely) successful, proceed to the
        # next page. Otherwise stay on the first page to let the user investigate the error.
        self.setCursor(Qt.WaitCursor)
        try:
            self.converter = Converter()
            self.converter.quiet = True
            filename = str(self.le_filename.text())
            self.converter.complete_check(filename)
            self.converter.execute()
            self.txt_log.document().setPlainText('\n'.join(self.converter.successfuls))
            self.pb_save.setEnabled(True)
            self._enable_save()
            self.stack_steps.setCurrentIndex(1)
            # put together an appropriate information message
            total_changes = len(self.converter.successfuls) + len(self.converter.warnings)
            num_warnings = len(self.converter.warnings)
            if self.converter.warnings:
                info = ('<b>Found a total of %d changes, but %d was not completed because of errors.'
                        % (total_changes, num_warnings))
                sec_info = ('You can still save the changes that was successful by selecting a '
                            'filename and clicking %s' % self.pb_save.text())
                self._display_info(info, sec_info, icon = 'warning', show_message_button = True)
                self.pb_show_warnings.setFocus()
            else:
                info = '<b>Found a total of %d changes, all completed OK.</b>' % total_changes
                sec_info = ('To save the changes, select a filename and click <i>%s</i>.'
                            % self.pb_save.text())
                self._display_info(info)
                self.pb_save.setFocus()
            # suggest a converted filename
            path, name_of_file = os.path.split(filename)
            base_name, ext = os.path.splitext(name_of_file)
            suggested_savename = os.path.join(path, base_name + '_opus_43' + ext)
            suggested_savename = os.path.normpath(suggested_savename)
            self.le_filename_out.setText(suggested_savename)

        except SyntaxError, ex:
                self.le_filename.setFocus()
                self.le_filename.selectAll()
                self._display_info('<b>This XML file seems to have an invalid syntax.</b>', ex,
                                   icon = 'warning')
        except IOError, ex:
                self.le_filename.setFocus()
                self.le_filename.selectAll()
                self._display_info('<b>An read error occurred while trying to load the file.</b>',
                                   ex, icon = 'warning')
        except Exception, ex:
                self.le_filename.setFocus()
                self.le_filename.selectAll()
                print repr(ex)
                self._display_info('<b>An error occurred while parsing the file.</b>', ex,
                                   icon = 'warning')
        finally:
            self.setCursor(Qt.ArrowCursor)

    def on_pb_back_released(self):
        # re-select a filename
        self._display_info(self.first_page_msg)
        self.stack_steps.setCurrentIndex(0)

    def on_pb_show_warnings_released(self):
        # show a dialog box with only the warnings from the conversion
        win = QDialog(self)
        win.resize(self.size() * 0.85)
        layout = QVBoxLayout()
        txt = QTextEdit(win)
        txt.setLineWrapMode(txt.NoWrap)
        txt.document().setPlainText('\n'.join(self.converter.warnings))
        pb = QPushButton('Close')
        self.connect(pb, SIGNAL('released()'), win.accept)
        layout.addWidget(txt)
        layout.addWidget(pb)
        win.setLayout(layout)
        win.exec_()

    def on_pb_save_released(self):
        try:
            filename = str(self.le_filename_out.text())
            dummy, just_filename = os.path.split(filename)
            f = open(filename, 'w')
            f.write(etree.tostring(self.converter.root))
            info = ('<b>Successfully wrote converted XML to file %s</b>' % just_filename)
            sec_info = 'If you you have more files to convert, you can go back and select another file'
            self._display_info(info, sec_info, icon = 'ok')
            self._enable_save(False)

        except IOError, ex:
            self._display_info('<b>A file error occurred while trying to save the converted XML.</b>', ex)
        except Exception, ex:
            self._display_info('<b>An error occurred while trying to save the converted XML.</b>', ex)
        finally:
            f.close()

if __name__ == '__main__':
    app = QApplication([], True)
    d = ConverterGui()
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    d.show()
    d.raise_()
    d.activateWindow()
    app.exec_()