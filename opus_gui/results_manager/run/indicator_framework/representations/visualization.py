# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

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