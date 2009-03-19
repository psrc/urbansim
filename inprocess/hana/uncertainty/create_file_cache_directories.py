# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from opus_core.misc import write_to_text_file
from opus_core.logger import logger

def create_file_cache_directories(directory, prefix='', file_name='cache_directories'):
    logger.start_block('Creating file %s in %s.' % (file_name, directory))
    base_dir = os.path.join(os.path.split(directory)[0:-1])[0]
    all_dirs = os.listdir(base_dir)
    all_dirs = [x for x in all_dirs if x.startswith(prefix)]

    for i in range(len(all_dirs)):
        all_dirs[i] = os.path.join(base_dir, all_dirs[i])
        
    write_to_text_file(os.path.join(directory, file_name), all_dirs)
    logger.end_block()

def check_if_directory_exists(base_directory, subdirectories=[], prefix=''):
    if len(subdirectories) == 0:
        return
    logger.start_block('Checking subdirectories in %s' % base_directory)
    all_dirs = os.listdir(base_directory)
    all_dirs = [x for x in all_dirs if x.startswith(prefix)]

    for i in range(len(all_dirs)):
        this_dir = os.path.join(base_directory, all_dirs[i])
        for subdir in subdirectories:
            if not os.path.exists(os.path.join(this_dir, subdir)):
                logger.log_warning("Directory %s does not exists." % os.path.join(this_dir, subdir))
    logger.end_block()
    
if __name__ == "__main__":
    directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/0416'
    #create_file_cache_directories(directory, prefix='run_')
    check_if_directory_exists(directory, subdirectories=['2005'], prefix='run_')