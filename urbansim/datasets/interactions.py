# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.datasets.interaction_dataset import InteractionDataset as CoreInteractionDataset
from opus_core.misc import DebugPrinter
from opus_core.resources import Resources

class InteractionDataset(CoreInteractionDataset):
    def __init__(self, resources=None, dataset1=None, dataset2=None, index1 = None, index2 = None, 
                debuglevel=0):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating object %s.%s" % (self.__class__.__module__, self.__class__.__name__), 2)
        
        local_resources = Resources(resources)
        local_resources.merge_if_not_None({"dataset1":dataset1, 
            "dataset2":dataset2, "debug":debug, 
            "index1":index1, "index2":index2})
        CoreInteractionDataset.__init__(self, resources = local_resources)
        
        