# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, re
import glob
from opus_core.misc import list2string
from opus_core.logger import logger
from functools import reduce

class OpusSyntaxChecker(object):
    """We want to avoid using tabs in .py files, and the files also need to have the GNU license. """
    
    def _py_file_names(self, prev, dir):
        """Returns a list of the .py files in this directory. """
        prev.extend([os.path.join(dir[0], file) for file in glob.glob1(dir[0], '*.py' )])
        return prev
        
    def check_syntax_for_opus_package(self, opus_package_name, file_names_that_do_not_need_gpl=[]):
        """Checks the syntax of the files in this opus package.
        Prints a list of files in the root with tabs in the *.py files or files which do not contain GPL license.
        """
        import_cmd = 'import %s' % opus_package_name
        exec(import_cmd)
        root_dir = eval('%s.__path__[0]' % opus_package_name)
        self._check_syntax_for_dir(root_dir, file_names_that_do_not_need_gpl)

    def _check_syntax_for_dir(self, root_dir, file_names_that_do_not_need_gpl=[]):
        py_file_names = reduce(self._py_file_names, os.walk(root_dir), [])
        
        files_with_no_license = []
        files_with_tab = []
        for py_file_name in py_file_names:
            lines_with_tabs = self._has_tabs(py_file_name)
            if self._file_needs_GPL(os.path.basename(py_file_name), file_names_that_do_not_need_gpl) and not self._has_GPL(py_file_name):
                logger.log_error("missing GPL in file %s" % py_file_name)
                files_with_no_license.append(py_file_name)
            if lines_with_tabs:
                logger.log_error("tab(s) in file %s, line(s) %s" % (py_file_name, list2string(lines_with_tabs, ", ")))
                files_with_tab.append(py_file_name)
                
        if files_with_no_license or files_with_tab:
            files_with_problems = files_with_no_license+files_with_tab
            raise SyntaxError("Please fix reported syntax problems with python files: %s."%(','.join(files_with_problems)))

    def _has_tabs(self, file_name):
        f=open(file_name)
        line_counter = 0
        lines_with_tabs = []
        for line in f.readlines():
            line_counter += 1
            if '\t' in line:
                lines_with_tabs.append(line_counter)
        return lines_with_tabs
        
    gpl_text = "See opus_core/LICENSE"
    gpl_text = re.sub('[ ]+', '.*', gpl_text)    # replace white spaces with *, for regular expression
    def _has_GPL(self, file_name):
        """Return false if there is no GPL in this file's header. """
        f=open(file_name, 'r')
        header_text = f.read(1000)               # read the first 1000 bytes (about a page worth) lines of text from file
        f.close()
        return re.search(self.gpl_text, ''.join(header_text.split()))
        
    def _file_needs_GPL(self, py_file_basename, file_names_that_do_not_need_gpl=[]):
        """Return true if the file needs the GPL, return false otherwise"""
        i = 0
        while (i < len(file_names_that_do_not_need_gpl)):
            if(re.compile(file_names_that_do_not_need_gpl[i]).search(py_file_basename)):
                return False
            i += 1
        return True

from opus_core.tests import opus_unittest
import tempfile
from os.path import join
from shutil import rmtree

class TestSyntaxChecker(opus_unittest.OpusTestCase):
    license = """
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE""" 

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
    def tearDown(self):
        rmtree(self.temp_dir)
        
    def test_no_tabs(self):
        mock_python_file = open(join(self.temp_dir, 'del_me_a.py'), 'w')
        mock_python_file.write(self.license)
        mock_python_file.write('\t This line has a tab on it')
        mock_python_file.close()
        logger.be_quiet()
        self.assertRaises(SyntaxError, OpusSyntaxChecker()._check_syntax_for_dir, self.temp_dir)
        logger.talk()
        
    def test_GPL_finder(self):
        mock_python_file = open(join(self.temp_dir, 'del_me_b.py'), 'w')
        mock_python_file.write('This line is okay and does not have a tab on it')
        mock_python_file.close()
        logger.be_quiet()
        self.assertRaises(SyntaxError, OpusSyntaxChecker()._check_syntax_for_dir, self.temp_dir)
        logger.talk()
        
    def test_no_syntax_violations(self):
        mock_python_file = open(join(self.temp_dir, 'del_me_c.py'), 'w')
        mock_python_file.write(self.license)
        mock_python_file.write('This line is okay and does not have a tab on it')
        mock_python_file.close()
        OpusSyntaxChecker()._check_syntax_for_dir(self.temp_dir)

        

if __name__ == '__main__':
    opus_unittest.main()
