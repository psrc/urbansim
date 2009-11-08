#
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

from opus_core.logger import logger
from opus_core.resources import Resources
import os, pickle, tempfile
from opus_core.configuration import Configuration
        
def write_resources_to_file(filename, resources):
    """Given a filename and a resource object, this will dump a dictionary of the resources to the file."""
    loc_resources = {}
    for key in resources.keys():
        loc_resources[key]=resources[key]
        
    f = open(filename,'w')
    try:
        pickle.dump(loc_resources, f)
    finally:
        f.close()
    
def get_resources_from_file(filename):
    """Given a filename of a file containing a dictionary, this will load the dictionary from the file."""
    return Configuration(pickle.load(open(filename, "r")))
    
def get_resources_from_string(resources_string):
    """Given a string containing a dictionary, this will load the dictionary from the file."""
    return Configuration(pickle.loads(resources_string))
    
def write_to_file(file_name, content_string):
    """Given a file name and a content_string, write the string to the file """
    f = open(filename, "w")
    f.write(content_string)
    f.close()
    
def write_to_file(file_name, content_string_list):
    """Given a file name and a content_string_list, write the list of strings to the file """
    f = open(file_name, "w")
    f.writelines(content_string_list)
    f.close()    
    
def read_file_content(file_name):
    """Read a file content, return a string"""
    f = open(file_name, "r")
    return "".join(f.readlines())
    
from opus_core.tests import opus_unittest
class FileUtilitiesTests(opus_unittest.OpusTestCase):
    """Test files utilities in this module."""
    def setUp(self):
        self.file_name = tempfile.mktemp()
        
    def tearDown(self):
        os.remove(self.file_name)
        
    def test_read_write_resources_to_file(self):
        data = {"arg1":1, "arg2":"2", "dict1":{"three":3,"four":4}}
        resources = Resources(data)
        write_resources_to_file(self.file_name, resources)
        data2 = get_resources_from_file(self.file_name)
        self.assertEquals(data, data2)
        
    def test_read_write_to_file(self):
        content = "test\n test2\n\n\ttest"
        write_to_file(self.file_name, content)
        loaded_content = read_file_content(self.file_name)
        self.assertEquals(content, loaded_content)
        content = ["test","test2","","test3"]
        write_to_file(self.file_name, content)
        loaded_content = read_file_content(self.file_name)            
        self.assertEquals("".join(content), loaded_content)
    
    def test_read_resources_from_string(self):
        data = {"arg1":1, "arg2":"2", "dict1":{"three":3,"four":4}}
        resources = Resources(data)
        write_resources_to_file(self.file_name, resources)                        
        resources_string = read_file_content(self.file_name)
        loaded_resources = get_resources_from_string(resources_string)
        self.assertEquals(resources, loaded_resources)
        
if __name__ == "__main__":
    opus_unittest.main()
    