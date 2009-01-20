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
import os, copy, tempfile

from xml.etree.cElementTree import tostring, Element

from opus_gui.main.controllers.mainwindow import update_mainwindow_title
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.opus_exceptions.xml_version_exception import XMLVersionException

class OpusProject(object):
    '''
    Methods and attributes for handling an OPUS project file.
    '''

    def __init__(self, opus_gui = None):
        '''
        @param opus_gui (OpusGui): Window to update title when dirty flag change
        '''
        # Project name
        self.name = ''
        # Filename of loaded project
        self.filename = ''
        # XMLController object
        self.xml_config = None
        # Local project tree root
        self._root_node = None
        # Dirty flag
        self._dirty = False
        # Mapping of nodes -> parents
        self._parent_map = {}

    def __is_dirty(self):
        return self._dirty

    def __set_dirty(self, dirty):
        self._dirty = dirty
        update_mainwindow_title()

    dirty = property(__is_dirty, __set_dirty)

    def open(self, filename):
        '''
        Load a project file from XML.
        @return: flag and message (tuple(boolean, String))
        The flag is only True if the project loaded without problems.
        '''
        filename = str(filename)
        if not os.path.exists(filename):
            return (False, "Tried to load project from file '%s', but that file "
                    "does'nt exist" %filename)
        default_path = os.path.dirname(filename)
        filename = os.path.basename(filename)
        try:
            xml_config = XMLConfiguration(filename, default_path)
        # Catch only the errors that XMLConfiguration is known to throw
        except (IOError, SyntaxError, ValueError,
                SyntaxError, XMLVersionException), ex:
            return (False, str(ex))

        self.xml_config = xml_config
        # Grab a working copy of the full tree
        # self._root_node = copy.deepcopy(xml_config.full_tree.getroot())
        self._root_node = xml_config.full_tree.getroot()
        self.name = self.find('./general/project_name').text
        self.filename = os.path.normpath(os.path.join(default_path, filename))

        self.dirty = False
        os.environ['OPUSPROJECTNAME'] = self.name
        return (True, 'Project %s loaded OK' %filename)

    def get_reloaded_xml_tree(self):
        '''
        Create a new, temporary, XMLConfiguration based on the XML structure of
        the working tree and get the root node for that tree.
        @return: the new tree root (Element).
        '''
        # TODO -- maybe consider doing this another way?

        # Write out a temporary file to use when initializing XMLConfig
        tmp_dir = tempfile.mkdtemp('xml_tmp', 'opus_gui')
        tmp_filename = os.path.join(tmp_dir, '_xml_tmp.xml')
        tmp_file = open(tmp_filename, 'w')
        tmp_file.write(tostring(self._root_node))
        tmp_file.close()
        tmp_xml_config = XMLConfiguration(os.path.basename(tmp_filename),
                                          tmp_dir)
        return tmp_xml_config.full_tree.getroot()

    def save(self, filename = None):
        '''
        Save a project file to disk
        @param filename (String): filename to save under.
        If filename is None, the filename that the project loaded from is used.
        @return: flag and message (tuple(boolean, String)
        flag is only True if the file was successfully saved.
        '''
        if not self.is_open(): return

        if filename is None:
            filename = self.filename

        self.update_xml_config()

        try:
            self.xml_config.save_as(filename)
        except IOError, ex:
            return (False, 'An error occurred when trying to save the project.\n'
                    'The error is described as: ' + str(ex))

        self.dirty = False
        return (True, 'Project successfully saved')

    def update_xml_config(self):
        '''
        Updates the XML Configuration object with the XML contents from this
        project.
        '''
        if self.is_open():
            self.xml_config.update(tostring(self._root_node))

    def close(self):
        ''' Close the project - removing any references to files or projects '''
        self.name = ''
        self.filename = ''
        self.xml_config = None
        self._root_node = None
        self.dirty = False
        self._parent_map = None
        os.environ['OPUSPROJECTNAME'] = 'misc'

    def find(self, node_path):
        '''
        Overloading the find method for root_node
        @return the found element (Element) or None
        '''
        if self._root_node is None:
            return None
        return self._root_node.find(node_path)

    def is_open(self):
        '''
        Check if this is an open project
        @return True if there is a loaded project, False otherwise
        '''
        return self.xml_config is not None

    def data_path(self):
        '''
        Get the project's data directory
        @return: Full path to project's data directory (String) or None if the
        project is not open.
        '''
        if not self.is_open(): return None

        opus_data_path = self.xml_config.get_opus_data_path()
        return os.path.join(opus_data_path, self.name)

#    def node_path(self, node):
#        '''
#        Uses XMLConfiguration's parent_map to get a node's path from root.
#        @param node (Element): Node to get full path for
#        @return The full path for the node (String) or None if the node was not
#        in the parent_map (i.e was created after the XML file was loaded from
#        disk)
#        '''
#        if not node in self.xml_config.parent_map:
#            return None
#        parent_path = self.node_path(self.xml_config.parent_map[node]) or ''
#        return parent_path + node.tag + '/'

    def root_node(self):
        '''
        Get the project root node or None
        @return root node for project (Element) or None
        '''
        return self._root_node

class DummyProject(OpusProject):
    '''
    Dummy project to be used for testing and project-agnostic XmlControllers
    '''

    def __init__(self):
        OpusProject.__init__(self)

    def __false(self, *args, **kwargs): return False
    dirty = property(__false, __false)

    def open(self, filename):
        return (False, 'Dummy projects cannot load files')

    def save(self, filename = None):
        return (False, 'Dummy projects cannot save files')

    def get_reloaded_xml_tree(self): return Element('')

    def close(self): pass

    def is_open(self): return False

    def data_path(self): return None

    def node_path(self, node): return ''
