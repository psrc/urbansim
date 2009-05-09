# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest
from PyQt4 import QtGui

class OpusGUITestCase(opus_unittest.OpusTestCase):

    def __init__(self, methodName = 'runTest'):
        opus_unittest.OpusTestCase.__init__(self, methodName)
        self.app = QtGui.QApplication([], True)

    def get_data_from_test_files(self, filename, base_file):
        ''' Get data from <filename> in test_files (a dir relative to the test file'''
        path = os.path.split(base_file)[0]
        full_path = os.path.join(path, 'test_files', filename)
        return open(full_path, 'r').read()