# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import tempfile, sys

from PyQt4 import QtGui
from opus_gui.main.views.ui_log_widget import Ui_LogWidget

class _MultiWriter(object):
    def __init__(self, streams):
        self.streams = streams
    def write(self, text):
        for stream in self.streams:
            stream.write(text)
            stream.flush()
    def flush(self):
        for stream in self.streams:
            stream.flush()

class LogWidget(QtGui.QDialog, Ui_LogWidget):

    MAX_LOG_SIZE = 1024*1024*32 # limit file size of log to 32mb

    def __init__(self, parent_widget):
        QtGui.QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.temp_file = None

    def do_refresh(self):
        self.on_pb_refresh_released()

    def on_pb_refresh_released(self):
        if not self.temp_file:
            return
        # Do the same thing as the mac osx terminal does; keep the scrolling to the bottom
        # if it is currently at the bottom, otherwise keep the scrolling position and let the content
        # keep adding up
        scroll_bar = self.te_logging.verticalScrollBar()
        cur_pos = scroll_bar.value()
        at_bottom = cur_pos == scroll_bar.maximum()
        # set content
        self.temp_file.seek(0)
        text = self.temp_file.read()
        self.te_logging.setPlainText(text)
        # scroll to an appropriate position
        if at_bottom or cur_pos > scroll_bar.maximum():
            scroll_bar.setValue(scroll_bar.maximum())
        else:
            scroll_bar.setValue(cur_pos)

    def start_stdout_capture(self):
        if self.temp_file:
            self.temp_file.close()
        self.temp_file = tempfile.TemporaryFile(mode = 'w+')
        standard_writer = _MultiWriter([sys.__stdout__, self.temp_file])
        error_writer = _MultiWriter([sys.__stderr__, self.temp_file])
        sys.stdout = standard_writer
        sys.stderr = error_writer

    def stop_stdout_capture(self):
        if self.temp_file:
            self.temp_file.close()
        self.temp_file = None
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
