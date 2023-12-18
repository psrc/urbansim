# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import win32com.client as com

def load_version_file(visum_dir, version_filename, visum_version_number=10):

    #Start up Visum COM server - requires win32com library
    try:
        Visum = com.Dispatch("visum.visum." + str(visum_version_number)) #latest version of VISUM registered as COM server
    except Exception:
        error_msg = "Starting Visum COM Server Failed"
        raise Exception(error_msg)      

    #Set directories
    try:
        Visum.SetPath(2, visum_dir) #version file
        Visum.SetPath(3, visum_dir) #od matrix file
        Visum.SetPath(4, visum_dir) #skim matrix file
        Visum.SetPath(12,visum_dir) #procedure file
    except Exception:
        error_msg = "Setting Visum Directories failed"
        raise Exception(error_msg)      

    #Load version file
    try:
        Visum.LoadVersion(version_filename)
    except Exception:
        error_msg = "Loading Visum version file failed"
        raise Exception(error_msg)

    #Return Visum object
    return Visum
