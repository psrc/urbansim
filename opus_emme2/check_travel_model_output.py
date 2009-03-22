# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
import sys
import os
import string

from glob import glob
from opus_core.logger import logger

class CheckTravelModelOutput(object):
    """Check existance & length of travel model reports after each travel 
        model run. """
    low = -0.05
    high = 0.5
    
    def __init__(self):
        self.missing_files = []
        self.missized_files = {} #{file_name: {actual_size:val, percent_difference:val}}
            
    def _expected_directory_contents(self, data_dir):
        """{directory: files of good output} """
        directory_and_path = {'bank1': os.path.join(data_dir, "bank1.tab"),
                                'bank2': os.path.join(data_dir, "bank2.tab"),
                                'bank3': os.path.join(data_dir, "bank3.tab")}
                
        directories_content = map(lambda dir: self._get_directory_contents(open(directory_and_path[dir],'r')), \
                                    directory_and_path.keys())
        return dict(zip(directory_and_path.keys(), directories_content))
    
    def _get_directory_contents(self, text_file):   
        text_file.readline() #ignore the header
        expected_file_sizes = {}
        for (size, file_name) in map(lambda line: string.split(line), text_file.readlines()):
            expected_file_sizes[file_name] = int(size)
        text_file.close()
        return expected_file_sizes

    def find_errors(self, travel_model_year_dir, expected_files_and_sizes_dir):
        expected_file_info = self._expected_directory_contents(expected_files_and_sizes_dir)
        #logger.log_status("Total expected files: ", str(reduce(lambda old_sum, key: len(expected_file_info[key]) + old_sum, \
                                                    #expected_file_info.keys(), 0)))
        
        for dir_name in expected_file_info.keys():
            real_data_files = map(lambda file_name: (os.path.basename(file_name), os.stat(file_name)[6]), \
                                    glob(os.path.join(travel_model_year_dir, dir_name,"*.rp*")))
            real_data_files = dict(real_data_files)
            for file_name, expected_size in expected_file_info[dir_name].iteritems():
                if real_data_files.has_key(file_name):
                    if expected_size != 0:
                        percent_difference = float(real_data_files[file_name] - expected_size) / expected_size
                    else:
                        percent_difference = real_data_files[file_name]
                    if not (CheckTravelModelOutput.low < percent_difference < CheckTravelModelOutput.high):
                        self.missized_files[os.path.join(dir_name, file_name)] = {'actual_size': real_data_files[file_name], \
                                                                                    'percent_difference':percent_difference}
                else:
                    self.missing_files.append(os.path.join(dir_name, file_name))

        return self.missing_files or self.missized_files

    def check_reports_creation_and_sizes(self, travel_model_year_dir, expected_files_and_sizes_dir="expected_file_sizes_e05"):
        """If there are missing files or any files over 10% missized then an exception will be thrown.
           If there are files 5-10% missized then a warning will be printed."""
        
           
        if self.find_errors(travel_model_year_dir,
                            os.path.join(expected_files_and_sizes_dir, 
                                         os.path.abspath(travel_model_year_dir).split(os.sep)[-1])):
            # range: (-5%, 50%) -- smaller than 5% or larger than 50% original size are not allowed

            if self.missing_files:
                logger.log_error("%d missing report files: %s" % (len(self.missing_files), str(self.missing_files)))
            if self.missized_files:
                logger.log_error("The following files are out of range(-5%, 50%) : " + \
                                                            reduce(lambda prev, file: prev + file[0] + " off by %d percent, \n" \
                                                                    % (file[1]['percent_difference']*100) , \
                                                                    self.missized_files, ""))                    
            if self.missing_files:
                raise LookupError("Error, %d missing report files: %s" % (len(self.missing_files), str(self.missing_files)))

            if self.missized_files:
                raise StandardError("Error, the following files are out of range(-5%, 50%) : " + \
                                                            reduce(lambda prev, file: prev + file[0] + " off by %d percent, \n" \
                                                                    % (file[1]['percent_difference']*100) , \
                                                                    self.missized_files, ""))
            

from opus_core.tests import opus_unittest
from os.path import abspath, join
from shutil import rmtree
import tempfile
    
class TestTravelOutputChecker(opus_unittest.OpusTestCase):
    def setUp(self):
        temp_dir =  tempfile.mkdtemp(prefix='opus_tmp')
        data_dir = os.path.join(temp_dir, "opus_emme2", "data", "expected_file_sizes", "2000_t05")
        os.makedirs(data_dir)
        sample_data = {'bank1':{'file1.rp0':300, 'file2.rp3':1024},
                        'bank2':{'file3.rpt':2048},
                        'bank3':{'file4.rp0':1234, 'file5.rp2':12, 'file6.rp1':1233}}
        
        original_dir = os.path.abspath('.')
        os.chdir(data_dir)
        for (dir_name, files_in_dir) in sample_data.iteritems():
            data_file = open(dir_name+'.tab', 'w')
            os.mkdir(join(temp_dir, dir_name))
            data_file.write('size\tfile_name\n')
            for file_name, file_size in files_in_dir.iteritems():
                data_file.write('%d\t%s\n' % (file_size, file_name))
                a_file = open(join(temp_dir, dir_name, file_name), 'w')
                a_file.write('n'*(file_size+1)) # make a small error in file size
                a_file.close()
            data_file.close()
        os.chdir(original_dir)
        self.temp_dir = temp_dir
        
    def tearDown(self):
        rmtree(self.temp_dir)
        
    def test_checker(self):            
        checker = CheckTravelModelOutput()
        # travel_model_year_dir is temp_dir in this test
        data_dir = os.path.join(self.temp_dir, "opus_emme2", "data", "expected_file_sizes", "2000_t05")
        self.assert_(not checker.find_errors(self.temp_dir, data_dir))
            
    def test_emme2_wrapper(self):
        checker = CheckTravelModelOutput()
        old_stdout = sys.stdout
        sys.stdout = None
        try:
            data_dir = os.path.join(self.temp_dir, "opus_emme2", "data", "expected_file_sizes")
            checker.check_reports_creation_and_sizes('2000_t05', data_dir)
            sys.stdout = old_stdout
            self.assert_(False, "Should have thrown an exception but did not.")
        except:
            pass

        sys.stdout = old_stdout


if __name__ == "__main__":
    opus_unittest.main()
        