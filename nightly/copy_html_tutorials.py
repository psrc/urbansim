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

import os
import sys

from optparse import OptionParser
from shutil import copytree

class CopyHtmlTutorials(object):
    """Copy the html versions of the tutorials to the given directory.
    """
    def run(self, from_dir, to_dir):
        """Copy the html versions of the tutorials from from_dir to to_dir.  The html versions are identified
        by looking for subdirectories of from_dir that contain an index.html file."""
        
        if not os.path.exists(to_dir):
            os.makedirs(to_dir)
            
        # Get list of directories in from_dir
        for name in os.listdir(from_dir):
            source_path = os.path.join(from_dir, name)
            if os.path.isdir(source_path):
                index_path = os.path.join(source_path, 'index.html')
                if os.path.exists(index_path):
                    dest_path = os.path.join(to_dir, name)
                    copytree(source_path, dest_path)


if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    
    parser = OptionParser()
    
    parser.add_option('-f', dest='from_path', 
                      help='path to existing tutorials directory')
    parser.add_option('-t', dest='to_path', 
                      help='path to directory for copies of tutorial html directories')
                      
    (options, args) = parser.parse_args()
                      
    if options.from_path is None or options.to_path is None:
        parser.print_help()
        sys.exit(1)
        
    copier = CopyHtmlTutorials()
    copier.run(options.from_path, options.to_path)
