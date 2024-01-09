# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest
from PyQt5 import QtWidgets

class OpusGUITestCase(opus_unittest.OpusTestCase):

    def __init__(self, methodName = 'runTest'):
        opus_unittest.OpusTestCase.__init__(self, methodName)
        self.app = QtWidgets.QApplication([])

    def get_data_from_test_files(self, filename, base_file):
        ''' Get data from <filename> in ./test_files (a subdir of the base_file's path)
        Example usage:
        to get the file "sample.xml" from the relative subdir 'testfiles' from within a test module:

          sample_xml_content = get_data_from_test_files('sample.xml', __file__)

         '''
        full_path = os.path.join(self.get_test_data_dir(base_file), filename)
        return open(full_path, 'r').read()

    def get_test_data_dir(self, base_file):
        return os.path.join(os.path.split(base_file)[0], 'test_files')
