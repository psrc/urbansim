# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array

class WeatherDataset(UrbansimDataset):
    """Set of weather data."""

    id_name_default = "year_id"
    in_table_name_default = "weather"
    out_table_name_default = "weather"
    entity_name_default = "weather"
    
