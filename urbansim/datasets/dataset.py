# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset import Dataset as CoreDataset
from opus_core.variables.attribute_type import AttributeType
from opus_core.resource_factory import ResourceFactory
from opus_core.misc import DebugPrinter
from opus_core.store.storage import Storage
from opus_core.session_configuration import SessionConfiguration

class Dataset(CoreDataset):
    """Urbansim Dataset"""

    id_name_default = "id"
    in_table_name_default = "datasets"
    attributes_default = Storage.ALL_COLUMNS
    out_table_name_default = "datasets_out"
    dataset_name = "dataset"
    nchunks_default = 1
    
    def __init__(self, 
            resources=None, 
            in_storage=None,
            out_storage=None, 
            in_table_name=None, 
            out_table_name=None, 
            attributes=None, 
            id_name=None, 
            nchunks=None, 
            debuglevel=0
            ):
        try: 
            debug = SessionConfiguration().get('debuglevel', 0)
        except:
            debug = 0
        debug = DebugPrinter(debug)
        if debuglevel > debug.flag:
            debug.flag = debuglevel
            
        debug.print_debug("Creating object %s.%s" % (self.__class__.__module__, self.__class__.__name__), 2)
        
        resources = ResourceFactory().get_resources_for_dataset(
            self.dataset_name, 
            resources = resources, 
            in_storage = in_storage,
            in_table_name_pair = (in_table_name,self.in_table_name_default), 
            attributes_pair = (attributes,self.attributes_default),
            out_storage = out_storage,
            out_table_name_pair = (out_table_name, self.out_table_name_default), 
            id_name_pair = (id_name, self.id_name_default), 
            nchunks_pair = (nchunks,self.nchunks_default), 
            debug_pair = (debug,None),
            )

        CoreDataset.__init__(self,resources = resources)