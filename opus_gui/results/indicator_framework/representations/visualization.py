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

import os

class Visualization(object):
    def __init__(self, 
                 indicators, 
                 visualization_type, 
                 name,
                 years,
                 table_name,
                 storage_location, #either a file path or a DatabaseConfiguration
                 file_extension,
                 **kwargs):
        self.indicators = indicators
        self.visualization_type = visualization_type
        self.storage_location = storage_location
        self.name = name
        self.years = years
        self.table_name = table_name
        self.file_extension = file_extension
        for k,v in kwargs.items():
            self.__setattr__(k,v)
    
    def get_file_path(self):
        try:
            return os.path.join(self.storage_location,
                                self.table_name + '.' + self.file_extension)
        except:
            if not isinstance(self.storage_location, str):
                raise Exception('get_file_path() only works for visualizations with results output to file system.')