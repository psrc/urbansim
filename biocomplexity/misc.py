# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

""" Collection of useful miscellaneous classes / functions"""

import os
import glob
import shutil


def get_distinct_list(list):
    """Returns a list of distinct elements of the argument list."""
    newlist = []
    for item in list:
        if not(item in newlist):
            newlist = newlist + [item]
    return newlist
    
def create_folder(base_dir, new_dir):
    if not os.path.exists(base_dir):
        print "base directory " + base_dir + " does not exist"
    else:
        dir_path = os.path.join(base_dir,new_dir)
        if not os.path.exists(dir_path):
            print "creating directory " + new_dir
            os.mkdir(dir_path)

def _create_folders_for_one_running_year(base_dir, year):
    dir_path = os.path.join(base_dir, str(year))
    create_folder(base_dir, str(year))
    create_folder(dir_path, 'land_covers')
    #create_folder(dir_path, 'output')
    #create_folder(dir_path, 'input')
    #create_folder(dir_path, 'equations')

def clean_up_files_in_folder(dir):
    if os.path.exists(dir):
        print 'removing all files in ' + dir
        for file in glob.glob(os.path.join(dir,'*.*')):
            os.remove(file)
            
def initialize_years_folders(base_dir, years_list, urbansim_mapping_path, start_lct_path):
    """Create the appropiated input/output folder structure for lccm """
    for i in range(len(years_list)):
        _create_folders_for_one_running_year(base_dir, years_list[i])
        #clean_up_files_in_folder(os.path.join(base_dir, str(years_list[i]), 'output'))
        land_cover_folder = os.path.join(base_dir, str(years_list[i]), 'land_covers')
        clean_up_files_in_folder(land_cover_folder)
        _copy_file_to_input_folder(urbansim_mapping_path, land_cover_folder)
        if i == 0:
            _copy_file_to_input_folder(start_lct_path, land_cover_folder)

def _copy_file_to_input_folder(file_path, input_folder):
    for file in glob.glob(file_path + ".*"):
        shutil.copy(file, input_folder)
