# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
import zipfile

class ExtractZipFile(object):
    ''' Extracts a zip file (source) to destination
    '''


    def __init__(self, source, destination):
        '''
        Constructor
        '''
        self.source = source
        self.destination = destination
        self.zip_file = zipfile.ZipFile(self.source)
        self.number_of_items = 0
        
    def extract(self):
        logger.log_status("Extracting files:")
        logger.log_status("From: %s" % self.source)
        logger.log_status("To: %s" % self.destination)
        
        self._createstructure(self.source, self.destination)
        
        # extract files to directory structure
        for i, name in enumerate(self.zip_file.namelist()):

            if not name.endswith('/'):
                outfile = open(os.path.join(self.destination, name), 'wb')
                outfile.write(self.zip_file.read(name))
                outfile.flush()
                outfile.close()
                
            self.number_of_items = i
            
        logger.log_status("Extracting (of %i files) finished..." % self.number_of_items)

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)


    def _makedirs(self, directories, basedir):
        """ Create any directories that don't currently exist """
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)
                
    def _listdirs(self, file):
        """ Grabs all the directories in the zip structure
        This is necessary to create the structure before trying
        to extract the file to it. """
        zf = zipfile.ZipFile(file)

        dirs = []

        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs