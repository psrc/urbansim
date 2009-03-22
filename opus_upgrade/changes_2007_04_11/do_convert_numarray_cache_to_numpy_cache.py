# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

   
from optparse import OptionParser
import os
import numpy
from distutils.dir_util import mkpath
from shutil import copyfile

from opus_core.store.file_flt_storage import storage_file
from opus_core.misc import load_from_text_file
  
class ConvertNumarrayCacheToNumpyCache(object):
    """
    Creates a copy of an UrbanSim cache that was stored with numarray formats
    and converts the data in the copy to be stored in numpy formats.  
    numarray formatted files end with extensions like '.Float32', whereas
    numpy formatted files end with extensions like '.lf4'.
    """
    
    #this has errors with new storage classes!
    def old_to_new_extension_mapping_for_binary_files(self):
        endian = storage_file(None)._get_native_endian_file_extension_character()
            
        return {
        '.Bool': '.ib1',
        '.Int8': '.%si1' % endian,
        '.Int16': '.%si2' % endian,
        '.Int32': '.%si4' % endian,
        '.Int64': '.%si8' % endian,
        '.Float32': '.%sf4' % endian,
        '.Float64': '.%sf8' % endian,
        }
    
    def _convert_extension_to_new_extension(self, extension):
        """Convert old style file extensions, like '.Float32', to
        the new numpy style file extensions, like '.lf4'."""
            
        if extension in old_to_new_extension_mapping_for_binary_files:
            return self.old_to_new_extension_mapping_for_binary_files()[extension]
        else:
            return extension
    
    def execute(self, input_path, output_path):
        """
        Create a new cache where all numarray files are converted to numpy
        format and extensions, and all other files and directories are copied.
        Exclude directories named CVS or .svn.
        """
        excluded_directories = ['CVS', '.svn']
        mkpath (output_path) # does nothing if output_path already exists
        for file_or_dir_name in os.listdir(input_path):
            if file_or_dir_name not in excluded_directories:
                file_or_dir_path = os.path.join(input_path, file_or_dir_name)
                if os.path.isfile(file_or_dir_path):
                    self.convert_file (input_path, file_or_dir_name, output_path)
                else:
                    self.execute(file_or_dir_path, os.path.join(output_path, file_or_dir_name))

    def convert_file(self, file_directory, file_name, output_directory):
        file_path = os.path.join(file_directory, file_name)
        file_stem, extension = os.path.splitext(file_name)
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        if extension in self.old_to_new_extension_mapping_for_binary_files():
            # Copy file to name with new extension
            new_extension = self.old_to_new_extension_mapping_for_binary_files()[extension]
            new_file_path = os.path.join(output_directory, '%s%s' % (file_stem, new_extension))
            copyfile(file_path, new_file_path)
            
        elif extension == '.txt':
            data = load_from_text_file(file_path)
            numpy_array = numpy.array(data)
            storage = storage_file(None)
            storage._write_to_file(output_directory, file_stem, numpy_array)
            
        else:
            copyfile(file_path, os.path.join(output_directory, file_name))
            
        

if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option('-d', '--cache_files_directory', dest='cache_files_directory', type='string', 
        help='(required) The filesystem path (relative or absolute) to the directory that will be recursively traversed.'
            '  All applicable files will be saved to the output directory.  Non-applicable files will simply be'
            ' copied over unchanged to the output directory.  This tool does not change the files in cache_files_directory.')
    parser.add_option('-o', '--output_directory', dest='output_directory', 
        type='string', help='(required) The filesystem path (relative or absolute) of the directory to which '
            'output will be written.  If it does not exist it will be created.')

    (options, args) = parser.parse_args()
    
    convert = ConvertNumarrayCacheToNumpyCache()
    convert.execute(options.cache_files_directory,options.output_directory)
