# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml.etree import Element

class AbstractManager(object):
    '''
    Handler for a group of UI elements with a XMLController as the center piece
    '''

    def __init__(self, base_widget, tab_base_widget, project, manager_node_path):
        '''
        @param base_widget (QWidget): Widget to place XmlController in
        @param tab_base_widget (QTabWidget): TabWidget to place gui elements (tabs)
        @param project (OpusProject): currently opened project
        @param manager_node_path (String): name of the top level node to manage
        '''
        # Main GUI Window
        self.base_widget = base_widget

        # Where to add tabs
        self.tab_base_widget = tab_base_widget

        # Universal project access
        self.project = project

        # Manager related node in project
        self.xml_root = self.project.find(manager_node_path)
        if self.xml_root is None:
            raise LookupError('The given manager node "%s" is not in the project XML' %
                              manager_node_path)

        # Controlled GUI elements
        self.tab_widgets = []
        self.xml_controller = None

    def close_tab(self, tab_widget):
        '''
        Close the GUI element if it's managed by this manager.
        Nothing is closed if the provided widget is not managed by this manager.
        @param tab_widget (QWidget): The widget to close.
        '''
        if tab_widget in self.tab_widgets:
            self.tab_base_widget.removeTab(self.tab_base_widget.indexOf(tab_widget))
            self.tab_widgets.remove(tab_widget)

    def _attach_tab(self, tab_widget):
        '''
        Couples a widget with this manager and adds it to the managers
        base tab widget.
        @param tab_widget (QWidget): The widget to add
        '''
        self.tab_widgets.append(tab_widget)
        self.tab_base_widget.insertTab(0, tab_widget, tab_widget.tabIcon,
                                  tab_widget.tabLabel)
        self.tab_base_widget.setCurrentIndex(0)
        tab_widget.show()

    def close(self):
        '''
        Close the manager, removing all it's managed tabs + it's XMLController.
        '''
        while len(self.tab_widgets) > 0:
            self.close_tab(self.tab_widgets[0])
        self.xml_controller.close()
