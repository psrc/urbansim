#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from sets import Set

from opus_core.resources import Resources
from opus_core.logger import logger

class Storage(object):
    """ Class for reading and writing to a storage device."""
    
    def write_dataset(self, write_resources=None):
        """Writes a dataset to the given storage media.
        Uses write_resourcess to determine what to write:
            'out_table_name' is the name of the 'table' to write. 
            'values' is a dictionary where keys are the attribute names and values 
                are value arrays of the corresponding attributes. 
            'attrtype' is a dictionary where keys are the attribute names and values 
                are the types of the corresponding attributes (PRIMARY,COMPUTED).
        """
        raise NotImplementedError, "Storage method 'write_dataset' not implemented."
                    

from opus_core.tests import opus_unittest


class TestStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = Storage()
        
    def tearDown(self):
        pass
        
    
if __name__ == '__main__':
    opus_unittest.main()