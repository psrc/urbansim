# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys
import subprocess

from shutil import rmtree
from tempfile import mkdtemp

from opus_core.logger import logger
from opus_core.misc import module_path_from_opus_path
from opus_core.file_utilities import write_resources_to_file

PIPE = -1
STDOUT = -2
LOG = -3

class ForkProcess(object):
    """Fork a new process."""

    def __init__(self):
        self.popen = None
        self.module_name = None
        self.python_cmd = None
        self._pickle_dir = None
    
    def fork_new_process(self, module_name, resources, delete_temp_dir=True, optional_args=[],
                         stdin=None, stdout=None, stderr=None, run_in_background=False):
        """Invoke the module whose fully-qualified opus name is module_name and pass it the 
        pickled resources.  Stores resources in pickle_file_path.
        If quiet=True, the console output for the command will not appear.
        """
        self.module_name = module_name
        self._pickle_dir = mkdtemp()
        try:
            if resources is None:
                pickle_file_path = None
            else:
                pickle_file_path = os.path.join(self._pickle_dir, 'resources.pickle')
                write_resources_to_file(pickle_file_path, resources)
            
            self.python_cmd = \
                self._assemble_command_line_call(module_name, 
                                                 resources, 
                                                 pickle_file_path, 
                                                 optional_args)
        
            if stdin == PIPE:
                stdin = subprocess.PIPE

            if stdout == PIPE:
                stdout = subprocess.PIPE
            elif stdout == LOG:
                log_file_path = os.path.join(self._pickle_dir, '_log_.log')
                stdout = open(log_file_path, "w")

            if stderr == PIPE:
                stderr = subprocess.PIPE
            elif stderr == STDOUT:
                stderr = subprocess.STDOUT
            elif stderr == LOG:
                log_file_path = os.path.join(self._pickle_dir, '_errlog_.log')
                stderr = open(log_file_path, "w")

            logger.log_status("Invoking: %s" % " ".join(self.python_cmd))
            self.popen = subprocess.Popen(self.python_cmd, stdin=stdin, stdout=stdout, stderr=stdout)
            if not run_in_background:
                self.wait()
                
        finally:
            if not run_in_background and delete_temp_dir:
                pass
                #self.cleanup()
    
    def wait(self):
        if self.popen is not None:
            self.popen.wait()
            self.check_status()
            
    def check_status(self):
        if self.popen is not None and \
           self.popen.returncode is not None and \
           self.popen.returncode != 0:
            raise StandardError("Child python process exited with failure.\nCalling module: %s\nSystem command: %s" % (self.module_name, self.python_cmd))

    def cleanup(self):
        if os.path.exists(self._pickle_dir):
            rmtree(self._pickle_dir)

    def _assemble_command_line_call(self, module_name, resources, 
                                    pickle_file_path, optional_args=[]):
        
        module_path = module_path_from_opus_path(module_name)
        
        python_cmd = [sys.executable, module_path]
        
        if pickle_file_path:
            python_cmd += ["-r", pickle_file_path]
        
        for optional_arg in optional_args:
            python_cmd += [str(optional_arg)]
        
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
