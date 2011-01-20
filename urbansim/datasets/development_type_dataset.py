# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.abstract_group_dataset import AbstractGroupDataset
from opus_core.misc import DebugPrinter

class DevelopmentTypeDataset(AbstractGroupDataset):
    """Set of development types."""

    id_name_default = "development_type_id"
    group_id_name = "group_id"

    def __init__(self,
            resources=None,
            in_storage=None,
            out_storage=None,
            in_table_name=None,
            out_table_name=None,
            in_table_name_groups=None,
            other_in_table_names=None,
            attributes=None,
            use_groups=True,
            id_name=None,
            nchunks=None,
            debuglevel=0
            ):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating DevelopmentTypeDataset object.",2)
        resources = self._get_resources_for_dataset(
            in_table_name_default="development_types",
            in_table_name_groups_default="development_type_group_definitions",
            out_table_name_default="development_types",
            dataset_name="development_type",                                        
            resources = resources,
            in_storage = in_storage,
            out_storage = out_storage,
            in_table_name = in_table_name,
            out_table_name = out_table_name,
            in_table_name_groups = in_table_name_groups,
            attributes = attributes,
            id_name = id_name,
            id_name_default = self.id_name_default,
            debug = debug,
            )

        AbstractGroupDataset.__init__(self,
            resources=resources,
            other_in_table_names=other_in_table_names, 
            use_groups=use_groups
            )
