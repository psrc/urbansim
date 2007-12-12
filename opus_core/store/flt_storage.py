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