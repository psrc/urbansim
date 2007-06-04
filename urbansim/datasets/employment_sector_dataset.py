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

from urbansim.datasets.abstract_group_dataset import AbstractGroupDataset
from opus_core.misc import DebugPrinter


class EmploymentSectorDataset(AbstractGroupDataset):
    """Set of employment sectors."""

    id_name_default = "sector_id"
    group_id_name = "group_id"

    def __init__(self,
            resources=None,
            in_storage=None,
            out_storage=None,
            in_table_name=None,
            out_table_name=None,
            attributes=None,
            id_name=None,
            nchunks=None,
            other_in_table_names=[],
            debuglevel=0
            ):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating EmploymentSectorDataset object.",2)
        resources = self._get_resources_for_dataset(
            in_table_name_default="employment_sectors",
            in_table_name_groups_default="employment_adhoc_sector_group_definitions",
            out_table_name_default="employment_sectors",
            dataset_name="employment_sector",
            resources = resources,
            in_storage = in_storage,
            out_storage = out_storage,
            in_table_name = in_table_name,
            out_table_name = out_table_name,
            attributes = attributes,
            id_name = id_name,
            id_name_default = self.id_name_default,
            debug = debug,
            )

        AbstractGroupDataset.__init__(self,
            resources=resources,
            other_in_table_names=other_in_table_names, 
            use_groups=True
            )
