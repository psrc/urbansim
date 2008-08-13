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

import os, re
import glob
from opus_core.logger import logger

class OpusSyntaxChecker(object):
    """We want to avoid using tabs in .py files, and the files also need to have the GNU license. """
    
    def _py_file_names(self, prev, dir):
        """Returns a list of the .py files in this directory. """
        prev.extend(map(lambda file: os.path.join(dir[0], file), glob.glob1(dir[0], '*.py' )))
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
            if not os.path.basename(py_file_name) in file_names_that_do_not_need_gpl and not self._has_GPL(py_file_name): 
                logger.log_error("missing GPL in file %s" % py_file_name)
                files_with_no_license.append(py_file_name)
            if lines_with_tabs:
                logger.log_error("tab(s) in file %s" % py_file_name)
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
                lines_with_tabs.append(str(line_counter) + ': ' + line)
        return lines_with_tabs
        
    gpl_text = "under the terms of the GNU General Public License"
    gpl_text = re.sub('[ ]+', '.*', gpl_text)    # replace white aspaces with *, for regular expression
    def _has_GPL(self, file_name):
        """Return false if there is no GPL in this file's header. """
        f=open(file_name, 'r')
        header_text = f.read(1000)               # read the first 1000 bytes (about a page worth) lines of text from file
        f.close()
        return re.search(self.gpl_text, ''.join(header_text.split()))
        
        

from opus_core.tests import opus_unittest
import tempfile
from os.path import join
from shutil import rmtree

class TestSyntaxChecker(opus_unittest.OpusTestCase):
    license = """
#UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
#You can redistribute this program and/or modify it under the terms of the
#GNU General Public License as published by the Free Software Foundation
#(http://www.gnu.org/copyleft/gpl.html).
#
#This program is distributed in the hope that it will be useful, but WITHOUT
#ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
#and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
#other acknowledgments. """ 

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
        self.failUnlessRaises(SyntaxError, OpusSyntaxChecker()._check_syntax_for_dir, self.temp_dir)
        logger.talk()
        
    def test_GPL_finder(self):
        mock_python_file = open(join(self.temp_dir, 'del_me_b.py'), 'w')
        mock_python_file.write('This line is okay and does not have a tab on it')
        mock_python_file.close()
        logger.be_quiet()
        self.failUnlessRaises(SyntaxError, OpusSyntaxChecker()._check_syntax_for_dir, self.temp_dir)
        logger.talk()
        
    def test_no_syntax_violations(self):
        mock_python_file = open(join(self.temp_dir, 'del_me_c.py'), 'w')
        mock_python_file.write(self.license)
        mock_python_file.write('This line is okay and does not have a tab on it')
        mock_python_file.close()
        OpusSyntaxChecker()._check_syntax_for_dir(self.temp_dir)


if __name__ == '__main__':
    opus_unittest.main()
