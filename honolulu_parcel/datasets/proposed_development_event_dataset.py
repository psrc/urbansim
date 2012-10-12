# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class ProposedDevelopmentEventDataset(UrbansimDataset):
    
    id_name_default = "proposed_development_event_id"
    in_table_name_default = "proposed_development_events"
    out_table_name_default = "proposed_development_events"
    dataset_name = "proposed_development_event"
