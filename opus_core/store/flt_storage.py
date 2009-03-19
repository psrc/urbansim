# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import re
from types import StringType
from file_flt_storage import file_flt_storage
from sftp_flt_storage import sftp_flt_storage
        
def flt_storage(storage_location):
    """
    returns file_flt_storage or sftp_flt_storage according to storage_location
    """
    ## TODO: this should be merged to storage_factory class, but it requires to refactor
    ## all direct references to flt_storage to use storage_factory instead 
    if type(storage_location) is StringType and re.search("^sftp://", storage_location):
        return sftp_flt_storage(storage_location)
    else:
        return file_flt_storage(storage_location)