#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

import sys, os.path, string
import time

class ConfigurePath:
    """
    Add to the code's search path (sys.path) all directories whose names are in
    the directories_to_add list and that reside in the named directory (project_name).
    
    The path to this directory has to be in your PYTHONPATH, since most UrbanSim python 
    code files import it by including the line:
        import configure_path
    """

    def __init__(self, dir_pattern=['python_src'], dir_filters=['CVS']):
        self.dir_pattern = dir_pattern
        self.dir_filters = dir_filters
        self.dirname = os.path.dirname(os.path.abspath(__file__))

    def get_directories_to_add(self):
        """Get directories to add either from .modulepath file or from the directory
        this file locates (and all its subdirectories)"""
        directories_to_add = entries = []
        entries = os.listdir(self.dirname)
        entries = [os.path.join(self.dirname,entry) for entry in entries]
        entries = filter(lambda x: os.path.isdir(x),entries)
        #normalize relative path such as ".."
        #entries = map(os.path.normpath, entries)
        
        directories_to_add.extend(entries)    

        #recusively walk through sub-directories searching for match dir_pattern
        for entry in entries:
             for root, subdirs, files in os.walk(entry):
                 for subdir in subdirs:
                     if subdir in self.dir_pattern:
                         directories_to_add.append(os.path.join(root,subdir))

        directories_to_add = self.filter_directories_by_dir_filters(directories_to_add)
        return directories_to_add

    def filter_directories_by_dir_filters(self,dirs):
        """remove directories that appear at dir_filters list"""

        for dir in dirs[:]:
            if os.path.basename(dir) in self.dir_filters:
                dirs.remove(dir)
        return dirs
    

    def append_path_to_syspath(self,directories_to_add):
        """append directories to sys.path if
        directory isn't in sys.path yet and
        os.path.isdir(dir) is True"""
        for dir in directories_to_add:
            if dir not in sys.path and os.path.isdir(dir):
                #sys.path.append(dir)
                sys.path.insert(0, dir)
    
    def run(self):
        """entry point for ConfigurePath class"""
        start_time = time.time()
        directories_to_add = self.get_directories_to_add()
        self.append_path_to_syspath(directories_to_add)

        print "Elapsed time = " + str(time.time() - start_time)

print "\n".join(sys.path)    
ConfigurePath().run()
print "\n".join(sys.path)
