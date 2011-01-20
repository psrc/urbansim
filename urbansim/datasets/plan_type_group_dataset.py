# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.dataset import Dataset
from urbansim.datasets.resource_creator_plantypegroups import ResourceCreatorPlanTypeGroups
from opus_core.misc import DebugPrinter

class PlanTypeGroupDataset(Dataset):
    """Set of plan type groups."""

    id_name_default = "group_id"

    def __init__(self,
            resources=None,
            in_storage=None,
            out_storage=None,
            in_table_name=None,
            out_table_name=None,
            attributes=None,
            id_name=None,
            nchunks=None,
            other_in_table_names=None,
            debuglevel=0
            ):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating PlanTypeGroupDataset object.",2)
        resources = ResourceCreatorPlanTypeGroups().get_resources_for_dataset(
            resources = resources,
            in_storage = in_storage,
            out_storage = out_storage,
            in_table_name = in_table_name,
            out_table_name = out_table_name,
            attributes = attributes,
            id_name = id_name,
            id_name_default = self.id_name_default,
            nchunks = nchunks,
            debug = debug,
            )

        Dataset.__init__(self,resources = resources)

        if isinstance(other_in_table_names,list):
            for place_name in other_in_table_names: #load other tables
                ds = Dataset(resources = resources)
                ds.load_dataset(in_table_name=place_name)
                self.connect_datasets(ds)
