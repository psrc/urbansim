# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QWidget, QGroupBox, QVBoxLayout, QIcon

from opus_gui.results.xml_helper_methods import elementsByAttributeValue, get_child_values

class ViewDocumentationForm(QWidget):
    def __init__(self, parent, indicator_node):
        QWidget.__init__(self, parent)
        self.inGui = False
        
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)
        
        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = indicator_node.nodeName()
        
        url_val = get_child_values(
                       parent = indicator_node,
                       child_names = ['documentation_link'])
        
        if 'documentation_link' in url_val: 
            url = url_val['documentation_link']
        else:
            return