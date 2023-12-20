# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger

class LaTeX(object):
    def _num_of_columns(self, table):
        num_of_columns = 0
        for row in table:
            if len(row) > num_of_columns:
                num_of_columns = len(row)
        if (num_of_columns == 0):
            logger.log_warning('Table has no columns; creating a single empty column so LaTeX will not fail')
            num_of_columns = 1
        return num_of_columns
        
    def create_rows(self, table, num_of_columns, default='', add_math_env=False):
        """
        Return a string containing one line per row of this table, 
        with each column separated by a '&' from the next column.
        """
        s = ''
        for row in table:
            if len(row) > 0:
                s += ('%s ' % row[0])
                for col in range(1, num_of_columns):
                    if col >= len(row):
                        s += '& %s ' % default
                    else:
                        s += '& %s ' % row[col]
                s += '\\\\\n'
        if add_math_env:
            s = re.sub('>', '$>$', s)
            s = re.sub('<', '$<$', s)
        return s

    def save_specification_table_to_tex_file(self, table, output_file, default='', label=None, caption=None):
        """
        Outputs a LaTeX file of the given table to the given output file.
        """
        f = open(output_file, 'w')
        
        num_of_columns = self._num_of_columns(table)
        prefix = '% UrbanSim LaTeX table output\n'
        prefix += '\\begin{landscape}\n'
        prefix += '\\begin{center}\n'
        prefix += '\\begin{longtable}{%sp{6in}}\n' % ('l'*(num_of_columns-1))
        if caption is not None:
            prefix += '\\caption{%s}\n' % caption
        if label is not None:
            prefix += '\\label{%s}\n' % label
        if caption is not None:
            prefix += '\\\\\n'
        f.write(prefix)
        
        header = '\hline\n'
        header += '% header\n'
        if len(table) > 0:
            if len(table[0]) > 0:
                header += '%s ' % table[0][0]
                for col in range(1, num_of_columns):
                    if col >= len(table[0]):
                        header += '& %s ' % default
                    else:
                        header += '& %s ' % table[0][col]
                header += '\\\\\n'
        header += '\hline\n'
        f.write(header)
        
        body = '% body\n'
        body += self.create_rows(table[1:], num_of_columns, default, add_math_env=True)
        body += '\hline\n'
        f.write(body)
        
        footer = '\\end{longtable}\n'
        footer += '\\end{center}\n'
        footer += '\\end{landscape}\n'
        f.write(footer)
        
        f.close()


import os
import re
from opus_core.tests import opus_unittest
import tempfile
from shutil import rmtree

class LatexTests(opus_unittest.OpusTestCase):
    """Some of the test methods in this class have names that follow
    this pattern: test_<name of method>_method_<aspect of this method being tested>
    """
    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='opus_tmp')
        self.output_file = os.path.join(self.tempdir, 'test_output')
        logger.enable_hidden_error_and_warning_words()
    
    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()
        rmtree(self.tempdir)
    
        
    def test_class_exists(self):
        try: LaTeX()
        except:
            self.fail('Unable to initialize Latex class!')
    
            
    def test_save_specification_table_to_tex_file_method_exists(self):
        try: LaTeX().save_specification_table_to_tex_file
        except:
            self.fail('Unable to access create_tex_table()!')
    
            
    def test_save_specification_table_to_tex_file_method_takes_input(self):
        try: LaTeX().save_specification_table_to_tex_file([[1]], self.output_file)
        except TypeError:
            self.fail('Unable to pass input to save_specification_table_to_tex_file()!')
       

    def test_save_specification_table_to_tex_file_method_creates_expected_output_file(self):
        LaTeX().save_specification_table_to_tex_file([[1]], self.output_file)
        self.assertTrue(os.path.isfile(self.output_file), 
            'Output file was not created or was named incorrectly!')
            
            
    def test_save_specification_table_to_tex_file_method_outputs_in_tabular_block(self):
        LaTeX().save_specification_table_to_tex_file([[1]], self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()
        
        m = re.search(r'\\begin\{longtable\}(\s|.)*\\end\{longtable\}', lines)
        self.assertTrue(m is not None, 'No tabular block found!')
            
    
    def test_save_specification_table_to_tex_file_method_output_params(self):
        LaTeX().save_specification_table_to_tex_file([[1, 2, 3]], self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        m = re.search(r'\\begin\{[^\{\}]*\}\s*\{[clr|]{2}', lines)
        self.assertTrue(m is not None, 'Incorrect params found!')   
        
    
    def test_save_specification_table_to_tex_file_method_number_of_hlines(self):
        LaTeX().save_specification_table_to_tex_file([[1, 2, 3]], self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        m = re.search(r'^(\s|.)*\\hline(\s|.)*\\hline(\s|.)*\\hline(\s|.)*$', 
                      lines)
        self.assertTrue(m is not None, 'Too few \\hline\'s found!')           

        m = re.search(r'^(\s|.)*\\hline(\s|.)*\\hline(\s|.)*\\hline(\s|.)*\\hline(\s|.)*$', lines)
        self.assertTrue(m is None, 'Too many \\hline\'s found!')
        
    
    def test_save_specification_table_to_tex_file_method_consistent_columns(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5,      6],
                 [     7,      8,      9]]
        num_cols = len(table[0])
        
        LaTeX().save_specification_table_to_tex_file(table, self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        matches = re.findall(r'(.*)\\\\', lines)

        for match in matches:
            cols = len(re.split(r'(?<!\\)&', match))
            self.assertTrue(cols == num_cols, 
                         "Incorrect number of columns found: '%s\\\\'" % match)
                          
  
    def test_save_specification_table_to_tex_file_method_number_of_rows(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5,      6],
                 [     7,      8,      9]]
                 
        rows = len(table)
        LaTeX().save_specification_table_to_tex_file(table, self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        matches = re.findall(r'(.*)\\\\', lines)

        self.assertTrue(len(matches) == rows, 
                     'Incorrect number of rows generated!')
        

    def test_save_specification_table_to_tex_file_method_correct_header_values(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5,      6],
                 [     7,      8,      9]]
                 
        LaTeX().save_specification_table_to_tex_file(table, self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        # This first match should be the header.
        m = re.search(r'(.*)\\\\', lines)
        self.assertTrue(m is not None, 'No header found!')
        
        entries = re.split(r'(?<!\\)&', m.group())
        
        for i in range(len(entries)):
            m = re.search(r'^\s*%s\s*(?:\\\\)?\s*$' 
                          % re.escape(str(table[0][i])), entries[i])
            self.assertTrue(m is not None, 
                         "Unexpected output. Expected '%s'. Received '%s'." 
                         % (table[0][i], entries[i]))
            
    
    def test_save_specification_table_to_tex_file_method_correct_row_values(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5,      6],
                 [     7,      8,      9]]
                 
        LaTeX().save_specification_table_to_tex_file(table, self.output_file)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        # Skip the header.
        m = re.findall(r'(.*)\\\\', lines)[1:]
        self.assertTrue(m is not None, 'No non-header rows found!')
        
        for i in range(len(m)):
            entries = re.split(r'(?<!\\)&', m[i])
            
            for j in range(len(entries)):
                match = re.search(r'^\s*%s\s*(?:\\\\)?\s*$' 
                                  % re.escape(str(table[i+1][j])), entries[j])

                self.assertTrue(match is not None, 
                             "Unexpected output. Expected '%s'. Received '%s'." 
                             % (table[i+1][j], entries[j]))
                             
    def test_save_specification_table_to_tex_file_method_takes_input_with_default(self):
        try: LaTeX().save_specification_table_to_tex_file([[1]], self.output_file, default='')
        except TypeError:
            self.fail('Unable to pass input (with default) to save_table_to_tex'
                      '_file()!')
                             
     
    def test_save_specification_table_to_tex_file_method_uneven_rows_underfull(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5],
                 [     7,      8,      9]]
                 
        cols = len(table[0])
        default = '-'
        LaTeX().save_specification_table_to_tex_file(table, self.output_file, default)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        # Skip the header.
        m = re.findall(r'(.*)\\\\', lines)[1:]
        self.assertTrue(m is not None, 'No non-header rows found!')
        
        for i in range(len(m)):
            entries = re.split(r'(?<!\\)&', m[i])
            
            for j in range(cols):
                if j >= len(table[i+1]):
                    pattern = (r'^\s*%s\s*(?:\\\\)?\s*$' 
                               % re.escape(default))
                    expected = default
                else:
                    pattern = (r'^\s*%s\s*(?:\\\\)?\s*$' 
                               % re.escape(str(table[i+1][j])))
                    expected = table[i+1][j]
                
                try:
                    match = re.search(pattern, entries[j])
                except IndexError:
                    self.fail('Output column incorrect width!')

                self.assertTrue(match is not None, 
                             "Unexpected output. Expected '%s'. Received '%s'." 
                             % (expected, entries[j]))
                             
     
    def test_save_specification_table_to_tex_file_method_uneven_rows_overfull(self):
        table = [['COL1', 'COL2', 'COL3'],
                 [     1,      2,      3],
                 [     4,      5,      6,    7],
                 [     8,      9,      10]]
                 
        cols = len(table[0])
        default = '-'
        LaTeX().save_specification_table_to_tex_file(table, self.output_file, default)
        f = open(self.output_file)
        lines = ''.join(f.readlines())
        f.close()

        # Skip the header.
        m = re.findall(r'(.*)\\\\', lines)[1:]
        self.assertTrue(m is not None, 'No non-header rows found!')
        
        for i in range(len(m)):
            entries = re.split(r'(?<!\\)&', m[i])
            
            for j in range(cols):
                if j >= len(table[i+1]):
                    pattern = (r'^\s*%s\s*(?:\\\\)?\s*$' 
                               % re.escape(default))
                    expected = default
                else:
                    pattern = (r'^\s*%s\s*(?:\\\\)?\s*$' 
                               % re.escape(str(table[i+1][j])))
                    expected = table[i+1][j]
                
                try:
                    match = re.search(pattern, entries[j])
                except IndexError:
                    self.fail('Output column incorrect width!')

                self.assertTrue(match is not None, 
                             "Unexpected output. Expected '%s'. Received '%s'." 
                             % (expected, entries[j]))
            
    def create_rows_method_correct_number_of_rows(self):
        """
        Does create_rows create the correct number of rows?
        """
        latex = LaTeX()
        results = latex.create_rows([[1,2,3],[4,5,6]], 2)
        self.assertEqual(2, len(results.split('\n')))
                
if __name__ == '__main__':
    opus_unittest.main()
