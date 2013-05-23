# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.store.delimited_storage import delimited_storage


class dat_storage(delimited_storage):
    def __init__(self, storage_location, *args, **kwargs):
        delimited_storage.__init__(self, 
            storage_location,
            delimiter = ' ',
            file_extension = 'dat', 
            *args, **kwargs
            )
