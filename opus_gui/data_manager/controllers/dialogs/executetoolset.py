# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QString, Qt, QRegExp, QObject, SIGNAL, QSize
from opus_gui.data_manager.views.ui_executetoolset import Ui_ExecuteToolSetGui
from opus_gui.data_manager.run.run_tool import OpusTool, RunToolThread

class ExecuteToolSetGui(QDialog, Ui_ExecuteToolSetGui):
    def __init__(self, mainwindow, tool_config_nodes, config_to_filename):
        QDialog.__init__(self, mainwindow)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.tool_config_nodes = tool_config_nodes
        self.config_to_filename = config_to_filename
        self.setWindowTitle('Executing set of %d nodes' % len(self.tool_config_nodes))

    def on_cancelExec_released(self):
        #print "cancelPushButton pressed"
        self.close()

    def on_execToolSet_released(self):
        self.execToolSet.setEnabled(False)
        self.textEdit_2.clear()
        self.progressBar_2.setValue(0)

        # Execute each tool in the set in a separate thread
        for config_node in self.tool_config_nodes:
            # Create a dict that maps of child node tags to their text values
            params = {}
            for child in config_node:
                key = str(child.tag).strip()
                value = str(child.text).strip()
                params[key] = value
            import_path = self.config_to_filename[config_node]
            #thread = RunToolThread(OpusTool(import_path, params))
            #thread.run()
            opus_tool = OpusTool(import_path, params)
            run_tool_thread = RunToolThread(opus_tool)
            QObject.connect(run_tool_thread, SIGNAL("toolFinished(PyQt_PyObject)"),
                        self.toolFinishedFromThread)
            QObject.connect(run_tool_thread, SIGNAL("toolProgressPing(PyQt_PyObject)"),
                        self.toolProgressPingFromThread)
            QObject.connect(run_tool_thread, SIGNAL("toolLogPing(PyQt_PyObject)"),
                        self.toolLogPingFromThread)
            run_tool_thread.run()

    def toolFinishedFromThread(self,success):
        #print "toolFinishedFromThread - %s" % (success)
        if success:
            self.progressBar_2.setValue(100)
        self.execToolSet.setEnabled(True)
        self.cancelExec.setText(QString('Close'))

    def toolLogPingFromThread(self,log):
        #print "toolLogPingFromThread - %s" % (log)
        self.textEdit_2.insertPlainText(log)

    def toolProgressPingFromThread(self,progress):
        #print "toolProgressPingFromThread - %s" % (progress)
        self.progressBar_2.setValue(progress)
