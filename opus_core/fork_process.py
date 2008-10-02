#
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

import os
import sys

from shutil import rmtree
from tempfile import mkdtemp

from opus_core.logger import logger
from opus_core.misc import module_path_from_opus_path
from opus_core.file_utilities import write_resources_to_file

class ForkProcess(object):
    """Fork a new process."""
    
    def fork_new_process(self, module_name, resources, delete_temp_dir=True, optional_args='',
                         quiet=False):
        """Invoke the module whose fully-qualified opus name is module_name and pass it the 
        pickled resources.  Stores resources in pickle_file_path.
        If quiet=True, the console output for the command will not appear.
        """
        pickle_dir = mkdtemp()
        try:
            if resources is None:
                pickle_file_path = None
            else:
                pickle_file_path = os.path.join(pickle_dir, 'resources.pickle')
                write_resources_to_file(pickle_file_path, resources)
            
            python_cmd = self._assemble_command_line_call(module_name, 
                                                          resources, 
                                                          pickle_file_path, 
                                                          optional_args)
            
            if quiet:
                log_file_path = os.path.join(pickle_dir, '_log_.log')
                python_cmd += ' > %s 2>&1' % log_file_path
        
            logger.log_status("Invoking: %s" % python_cmd)
            exit_status = os.system(python_cmd)
            if exit_status!=0:
                raise StandardError("Child python process exited with failure.\nCalling module: %s\nSystem command: %s" % (module_name, python_cmd))
                
        finally:
            if delete_temp_dir and os.path.exists(pickle_dir):
                rmtree(pickle_dir)
                pass
    
    def _assemble_command_line_call(self, module_name, resources, 
                                    pickle_file_path, optional_args=''):
                
        module_path = module_path_from_opus_path(module_name)
        if pickle_file_path is None:
            python_cmd = "%s \"%s\" %s" % (sys.executable, module_path, 
                                           optional_args)
        else:
            python_cmd = "%s \"%s\" -r %s %s" % (sys.executable, module_path, 
                                                 pickle_file_path, 
                                                 optional_args)
            
        return python_cmd
    



import os
import sys
import tempfile
from shutil import rmtree

from opus_core.tests import opus_unittest


class TestForkProcess(opus_unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_fork_process')
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_module_invalid(self):
        self.assertRaises(StandardError,
                          ForkProcess().fork_new_process,
                          module_name='xxx',
                          resources=None,
                          quiet=True,
                          )
        
    def test_hide_error_messages_if_ask_to_run_silently(self):
        # Create file that raises an error when executed
        path_to_python_file_to_invoke = os.path.join(self.temp_dir, 'raise_exception.py')
        f = file(path_to_python_file_to_invoke, 'w')
        try:
            f.write('if __name__ == "__main__": raise Exception()')
        finally:
            f.close()
            
        f = file(os.path.join(self.temp_dir, '__init__.py'), 'w')
        try:
            f.write('')
        finally:
            f.close()
    
        old_sys_path = sys.path[:]
        sys.path.append(self.temp_dir)
        try:
            self.assertRaises(StandardError,
                              ForkProcess().fork_new_process,
                              module_name='raise_exception',
                              resources=None,
                              quiet=True,
                              )
        finally:
            sys.path = old_sys_path


if __name__ == '__main__':
    opus_unittest.main()