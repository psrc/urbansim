# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#DISCLAIMER: THIS FILE IS OUT OF DATE AND NEEDS SIGNIFICANT MODIFICATIONS 
#            TO MAKE IT WORK
print "Create MySQL connection"
from urbansim.store.scenario_database import ScenarioDatabase

dbcon = ScenarioDatabase(hostname = "trondheim.cs.washington.edu",
                         username = "waterdemand",
                         password = "wewantH2O",
                         database_name = "water_demand_seattle")

print "Create Storage object."
from urbansim.storage_creator import StorageCreator
storage = StorageCreator().build_storage(type="mysql", location=dbcon)

consumption_type = "WRSR"

print "Create ConsumptionDataset object"
from waterdemand.datasets.consumption_dataset import ConsumptionDataset
consumption = ConsumptionDataset(in_storage = storage, in_table_name=consumption_type + "_grid")

from urbansim.datasets.gridcells import GridcellSet
from numpy import array
from opus_core.miscellaneous import unique_values

consumption_grid_id = consumption.get_attribute("grid_id")
years = consumption.get_attribute("billyear")
distinct_years = unique_values(years)

import os
from numpy import where, zeros, arange
cache_directory = "D:/urbansim_cache/water_demand"
for year in arange(1991, 2001):
    print year
    flt_storage = StorageCreator().build_storage(type="flt", location=os.path.join(cache_directory, str(year)))
    gridcells = GridcellSet(in_storage=flt_storage)
    grid_id_idx = array(map(lambda x: gridcells.try_id_mapping(x, -1), consumption_grid_id))
    year_idx = where(years==year)[0]
    grid_id_idx_for_year = grid_id_idx[year_idx]
    for attr in gridcells.get_known_attribute_names():
        if attr not in consumption.get_known_attribute_names():
            ftype = gridcells.get_attribute(attr).type()
            consumption.add_attribute(name=attr, data=zeros(consumption.size(), dtype=ftype))
        consumption.modify_attribute(name=attr,
                                     data=gridcells.get_attribute_by_index(attr, grid_id_idx_for_year),
                                     index=year_idx)

# store consumption dataset
out_storage = StorageCreator().build_storage(type="flt", location=cache_directory)
consumption.write_dataset(attributes = consumption.get_known_attribute_names(),
                          out_storage=out_storage, out_table_name=consumption_type.lower())
