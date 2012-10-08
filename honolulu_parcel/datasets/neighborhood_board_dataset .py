# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class NeighborhoodBoardDataset(UrbansimDataset):
    
    id_name_default = "neighborhood_board_id"
    in_table_name_default = "neighborhood_boards"
    out_table_name_default = "neighborhood_boards"
    dataset_name = "neighborhood_board"
