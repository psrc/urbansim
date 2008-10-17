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

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QString
from opus_gui.data_manager.views.ui_executetoolset import Ui_ExecuteToolSetGui
from opus_gui.data_manager.run.run_tool import OpusTool, RunToolThread

class ExecuteToolSetGui(QDialog, Ui_ExecuteToolSetGui):
    def __init__(self, mainwindow, fl, tools, tool_hook_to_tool_name_dict):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.tools = tools
        self.tool_hook_to_tool_name_dict = tool_hook_to_tool_name_dict

    def on_cancelExec_released(self):
        #print "cancelPushButton pressed"
        self.close()
    
    def on_execToolSet_released(self):
        tool_batch = []
        for i in range(0, self.tools.length(), 1):
            node = self.tools.item(i) #this is a QDomNode
            #print 'tool name: ', node.nodeName()
            #toolName = node.nodeName()            
            nodeChildren = node.childNodes() #this is a QDomNodeList
            params = {}
            for j in range(0, nodeChildren.length(), 1):
                child = nodeChildren.item(j) #this is a QDomNode
                #print 'parameter: ', child.nodeName(), ' = ', child.toElement().text()
                params[child.nodeName()] = child.toElement().text()
            toolname = self.getToolName(params[QString('tool_hook')])
            importpath = 'opus_gui.data_manager.run.tools.%s' % toolname
            tool = OpusTool(self.mainwindow, importpath, params)
            y = RunToolThread(self.mainwindow, tool)
            y.run()
    
    def getToolName(self, tool_hook):
        return self.tool_hook_to_tool_name_dict[tool_hook]
