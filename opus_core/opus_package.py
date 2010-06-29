# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, shutil
from opus_core.third_party.path import path
from opus_core.logger import logger
from opus_core.misc import copytree
from opus_core.misc import replace_string_in_files

class OpusPackage(object):
    """An abstraction for creating and manipulating Opus packages.
    """
    
    # Must over-ride following name in child class:
    name = None

    # May over-ride following names in child class:
    required_external_packages = ['numpy>=1.3.0', 'scipy>=0.7.1', 'sqlalchemy>=0.5.6', 
                                    'lxml>=2.2.2', 'Elixir>=0.6.1']
    required_opus_packages = []

    optional_external_packages = ['PyQt>=4.4.4', 'MySQL-python>=1.2.2', 'matplotlib>=0.99', 
                                  'Mapnik>=0.6.0', 'dbfpy', 'pil>=1.1.6', 
                                  'rpy2>=2.1.3']
    optional_opus_packages = []
    
    required_included_file_types = ['*.pdf','*.html','*.png']
    optional_included_file_types = ['*.gif']
    
        
    def _get_mod(self, modulePath):
        return __import__(modulePath, globals(), locals(), ['*'])
    
    def get_package_path(self):
        return self.get_path_for_package(self.get_package_name())
    
    def get_package_parent_path(self):
        return os.path.split(self.get_package_path())[0]

    def get_path_for_package(self, opus_package_name):
        """
        Returns the absolute path to this Opus package.
        """
        mod = self._get_mod(opus_package_name)
        return mod.__path__[0]
    
    def get_opus_core_path(self):
        """Returns absolute path to the 'opus_core' package."""
        mod = self._get_mod('opus_core')
        return mod.__path__[0]

    def get_package_name(self):
        return self.name
       
    def get_required_external_packages(self):
        return self.required_external_packages
        
    def get_required_opus_packages(self):
        return self.required_opus_packages
        
    def get_optional_external_packages(self):
        return self.optional_external_packages
        
    def get_optional_opus_packages(self):
        return self.optional_opus_packages                
        
    def get_required_included_file_types(self):
        return self.required_included_file_types
        
    def get_optional_included_file_types(self):
        return self.optional_included_file_types
            
    def print_package_name(self):
        logger.log_status("Opus package " + self.get_package_name())
    
    def print_package_requires(self):
        self.print_package_requires_opus()
        self.print_package_requires_external()

    def print_package_requires_opus(self):
        logger.log_status("Required Opus packages for "+ self.get_package_name() + ": " + 
                    str(self.get_required_opus_packages()))
                    
    def print_package_requires_external(self):
        logger.log_status("Required external packages for "+ self.get_package_name() + ": " + 
                    str(self.get_required_external_packages()))                    

    def print_package_optional_opus(self):
        logger.log_status("Optional Opus packages for "+ self.get_package_name() + ": " + 
                    str(self.get_optional_opus_packages()))
                    
    def print_package_optional_external(self):
        logger.log_status("Optional external packages for "+ self.get_package_name() + ": " + 
                    str(self.get_optional_external_packages()))
    
    def print_package_required_included_file_types(self):
        logger.log_status("Required file types to include for "+ self.get_package_name() + ": " + 
                    str(self.get_required_included_file_types()))
                    
    def print_package_optional_included_file_types(self):
        logger.log_status("Optional file types to include for "+ self.get_package_name() + ": " + 
                    str(self.get_optional_included_file_types()))                        
    
    #TODO: outdated, include other print methods
    def info(self):
        self.print_package_name()
        self.print_package_requires()
        
        
def create_package(package_parent_dir, package_name):
    """Create a new Opus package named package_name in the
    directory given by package_parent_dir.  
    """
    from opus_core.opus_package_info import package as OpusPackageInfo
    
    package_template = path(OpusPackageInfo().get_path_for_package('opus_core')) / 'package_template'
    new_package_dir=path(package_parent_dir) / package_name
    if not os.path.exists(new_package_dir.parent):
        os.makedirs(new_package_dir.parent)
    copytree(package_template, new_package_dir, skip_subdirectories=['CVS', '.svn'])
    # Replace each instance of opus_core.package_template in any of the
    # template files with the actual name of this Opus package.
    replace_string_in_files(new_package_dir, 'opus_core.package_template', package_name)


from opus_core.tests import opus_unittest
import tempfile
import sys

class OpusPackageTests(opus_unittest.OpusTestCase):        
    def setUp(self):
        class DummyPackage(OpusPackage):
            name = 'opus_core'
            
        self.package = DummyPackage()
        
        self.old_sys_path = sys.path
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
        # Make sure Python can find this temporary package.
        sys.path = [self.temp_dir] + sys.path
            
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        sys.path = self.old_sys_path
        
    def test_get_package_info_does_not_crash(self):
        self.package.info()
        
    def test_get_path_for_package(self):
        test_package_name = "test_get_path_for_package"
        self.path_to_new_package = os.path.join(self.temp_dir, test_package_name)
        
        path = self.package.get_path_for_package("opus_core")
        (path, package_name) = os.path.split(path)
        self.assertEqual(package_name, "opus_core")

        self.assertRaises(ValueError, self.package.get_path_for_package, "...an invalid package name..")
        
    def test_create_package(self):
        test_package_name = "test_create_package"
        self.path_to_new_package = os.path.join(self.temp_dir, test_package_name)
        
        create_package(self.temp_dir, test_package_name)
        self.assertEqual(self.path_to_new_package,
                         self.package.get_path_for_package(test_package_name))
        self.assertEqual(os.path.join(self.temp_dir, test_package_name, "tests"), 
                         self.package.get_path_for_package('%s.tests' % test_package_name))
                
if __name__ == '__main__':
    opus_unittest.main()