# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4 import QtGui

from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.tests.mockup_project import MockupOpusProject

from lxml.etree import tostring

class MockupManager(AbstractManager):

    '''
    A manager that doesn't require any parameters to be instantiated.
    '''

    def __init__(self,
                 xml = '<opus_project> <manager /> </opus_project>',
                 manager_node_path = 'manager',
                 opus_project = None):
        self.app = QtGui.QApplication([], True)
        base_widget = QtGui.QWidget()
        base_widget.setLayout(QtGui.QVBoxLayout())
        base_tab_widget = QtGui.QTabWidget(base_widget)
        project = MockupOpusProject(xml) if not opus_project else opus_project
        AbstractManager.__init__(self, base_widget, base_tab_widget, project, manager_node_path)

if __name__ == '__main__':
    instance = MockupManager()
    print 'Instance created'
