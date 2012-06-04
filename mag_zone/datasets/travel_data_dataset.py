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
from urbansim.datasets.travel_data_dataset import TravelDataDataset

class TravelDataDataset(TravelDataDataset):
    """Set of travel data logsums."""
    
    id_name_default = []      # use _hidden_id
    origin_id_name = "from_tazi03_id"
    destination_id_name = "to_tazi03_id"
    in_table_name_default = "travel_data"
    out_table_name_default = "travel_data"
    dataset_name = "travel_data"