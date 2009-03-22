# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
import os, copy, tempfile

from xml.etree.cElementTree import tostring, Element

from opus_gui.main.controllers.instance_handlers import update_mainwindow_title
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
        # Always close the project before loading another one to avoid mixing
        # data if the load is only partly successful
        self.close()
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
        # TODO -- a better way to do this is to keep two layers from the loaded
        # XML file. One that is the inherited layer (one level above) and one
        # that is this level.

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

    def root_node(self):
        '''
        Get the project root node or None
        @return root node for project (Element) or None
        '''
        return self._root_node


class DummyProject(OpusProject):
    '''
    Dummy project to be used for testing and for XmlControllers that don't
    have a real dependency of a project.
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


from opus_core.tests import opus_unittest
class TestOpusProject(opus_unittest.OpusTestCase):
    ''' Test suite for Opus Project '''

    def setUp(self):
        # Validate that the test data is present
        self.testdatapath = os.path.split(__file__)[0]
        self.testdatapath = os.path.join(self.testdatapath, 'testdata')
        self.testfile_valid = os.path.join(self.testdatapath,
                                           'project_valid.xml')
        self.testfile_invalid = os.path.join(self.testdatapath,
                                             'project_invalid.xml')

    def test_verify_testdata_available(self):
        for file in [self.testfile_invalid, self.testfile_valid]:
            self.assertTrue(os.path.exists(file),
                            'Required test data (%s) don not exist' % file )

    def project_is_closed(self, instance):
        '''
        Returns True of the values of the project are set to their defaults
        '''
        set_to_default = True
        if 'OPUSPROJECTNAME' in os.environ:
            set_to_default = os.environ['OPUSPROJECTNAME'] == 'misc'

        return set_to_default and \
            (instance.name == '') and \
            (instance.filename == '') and \
            (instance.xml_config == None) and \
            (instance._root_node == None) and \
            (instance.dirty == False) and \
            (instance._parent_map == None)

    def test_close(self):
        ''' Make sure that the project closed up OK '''
        instance = OpusProject()

        TESTVALUE = 'A TEST VALUE'

        instance.name = TESTVALUE
        instance.filename = TESTVALUE
        instance.xml_config = TESTVALUE
        instance._root_node = TESTVALUE
        instance.dirty = TESTVALUE

        # We also want to test that the environment variable 'OPUSPROJECTNAME'
        # is reset as it should, but need to be careful not to leave any side
        # effects from the test
        prev_environ = None
        if 'OPUSPROJECTNAME' in os.environ:
            prev_environ = os.environ['OPUSPROJECTNAME']
        os.environ['OPUSPROJECTNAME'] = TESTVALUE
        try:
            instance.close()
            self.assertTrue(self.project_is_closed(instance), 'Not all values where reset when the project was closed')
            self.assertFalse(instance.is_open())
        finally:
            if prev_environ is not None:
                os.environ['OPUSPROJECTNAME'] = prev_environ
            else:
                del os.environ['OPUSPROJECTNAME']

    def test_open(self):
        p = OpusProject()
        dont_exist = p.open('__I__WONT__EXIST__')
        self.assertTrue(len(dont_exist) == 2 and
                        dont_exist[0] == False)
        del dont_exist
        invalid = p.open(self.testfile_invalid)
        self.assertTrue(len(invalid) == 2 and
                        invalid[0] == False)
        self.assertFalse
        del invalid
        valid = p.open(self.testfile_valid)
        self.assertTrue(len(valid) == 2 and
                        valid[0] == True)
        self.assertTrue(p.dirty is False)
        # Test that it's actually a link to the xml tree and not a copy
        self.assertTrue(p.root_node() is p.xml_config.full_tree.getroot())
        # Test that the XML is correct
        self.assertTrue(p.root_node().tag == 'opus_project')
        # Test that the find method is equivalent to using nodes find
        self.assertTrue(p.find('general/project_name') is
                        p.root_node().find('general/project_name'))
        # Test that the name got parsed OK
        self.assertEquals(p.name, 'test_project')
        # Test that the data path is based on the name
        self.assertTrue(p.data_path().endswith('/test_project'))
        # Make sure no data is left arond when we open another file and fails
        p.open('__I__WONT__EXIST__')
        self.assertTrue(self.project_is_closed(p))

    def test_save(self):
        p = OpusProject()
        pass

    def test_data_path(self):
        pass

if __name__ == '__main__':
    opus_unittest.main()
