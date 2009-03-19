# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QString
from opus_gui.data_manager.views.ui_executetoolset import Ui_ExecuteToolSetGui
from opus_gui.data_manager.run.run_tool import OpusTool, RunToolThread

class ExecuteToolSetGui(QDialog, Ui_ExecuteToolSetGui):
    def __init__(self, mainwindow, tool_config_nodes, config_to_filename):
        QDialog.__init__(self, mainwindow)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.tool_config_nodes = tool_config_nodes
        self.config_to_filename = config_to_filename
        self.setWindowTitle('Executing set of %d nodes' % \
                            len(self.tool_config_nodes))

    def on_cancelExec_released(self):
        #print "cancelPushButton pressed"
        self.close()
    
    def on_execToolSet_released(self):
        # Execute each tool in the set in a separate thread
        for config_node in self.tool_config_nodes:
            # Create a dict that maps of child node tags to their text values
            params = {} 
            for child in config_node:
                key = str(child.tag).strip()
                value = str(child.text).strip()
                params[key] = value
            tool_filename = self.config_to_filename[config_node]
            import_path = 'opus_gui.data_manager.run.tools.%s' % tool_filename
            thread = RunToolThread(OpusTool(import_path, tool_filename))
            thread.run()
