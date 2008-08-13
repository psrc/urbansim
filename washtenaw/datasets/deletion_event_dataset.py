#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DeletionEventDataset(UrbansimDataset):
    """Set of events that represent deletion of jobs and/or households from specific locations.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "deletion_events"
    out_table_name_default = "deletion_events"
    dataset_name = "deletion_event"
    