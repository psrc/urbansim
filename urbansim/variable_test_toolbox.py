# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.datasets.development_group_dataset import DevelopmentGroupDataset
from urbansim.datasets.employment_sector_group_dataset import EmploymentSectorGroupDataset
from urbansim.datasets.plan_type_group_dataset import PlanTypeGroupDataset
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from urbansim.datasets.faz_dataset import FazDataset
from urbansim.datasets.fazdistrict_dataset import FazdistrictDataset
from urbansim.datasets.household_x_gridcell_dataset import HouseholdXGridcellDataset
from urbansim.datasets.household_x_zone_dataset import HouseholdXZoneDataset
from urbansim.datasets.household_x_neighborhood_dataset import HouseholdXNeighborhoodDataset
from urbansim.datasets.development_project_x_gridcell_dataset import DevelopmentProjectXGridcellDataset
from urbansim.datasets.neighborhood_dataset import NeighborhoodDataset
from urbansim.datasets.race_dataset import RaceDataset
from urbansim.datasets.job_x_gridcell_dataset import JobXGridcellDataset
from urbansim.datasets.county_dataset import CountyDataset
from urbansim.datasets.large_area_dataset import LargeAreaDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from numpy import array, transpose, indices, ceil, sqrt, arange

class VariableTestToolbox(object):

    id_names = {
        "gridcell":"grid_id", 
        "household":"household_id", 
        "job":"job_id", 
        "development_project":"project_id", 
        "neighborhood":"neighborhood_id", 
        "zone":"zone_id", 
        "faz":"faz_id", 
        "fazdistrict":"fazdistrict_id", 
        "race":"race_id", 
        "travel_data":["from_zone_id", "to_zone_id"], 
        "development_event":["grid_id","scheduled_year"], 
        "county":"county_id", 
        "large_area":"large_area_id",
        "development_group":"group_id", 
        "employment_sector_group":"group_id", 
        "plan_type_group":"group_id",
        "building": "building_id",
    }
    datasets = list(id_names.keys())
    interactions = [
        "household_x_gridcell", 
        "job_x_gridcell", 
        "household_x_zone", 
        "household_x_neighborhood", 
        "development_project_x_gridcell",
    ]

    def get_resources(self, data_dictionary, dataset):
        """Create resources for computing a variable. """
        resources=Resources()
        
        for key in list(data_dictionary.keys()):
            if key in self.datasets:
                data = data_dictionary[key]
                
                storage = StorageFactory().get_storage('dict_storage')
                
                if self.id_names[key] not in list(data_dictionary[key].keys()) and not isinstance(self.id_names[key], list):
                    data[self.id_names[key]] = arange(1, len(data_dictionary[key][list(data_dictionary[key].keys())[0]])+1) # add id array
                
                id_name = self.id_names[key]
                storage.write_table(table_name = 'data', table_data = data)
                
                if key == "gridcell":
                    gc = GridcellDataset(in_storage=storage, in_table_name='data')
                    
                    # add relative_x and relative_y
                    gc.get_id_attribute()
                    n = int(ceil(sqrt(gc.size())))
                    if "relative_x" not in list(data.keys()):
                        x = (indices((n,n))+1)[1].ravel()
                        gc.add_attribute(x[0:gc.size()], "relative_x", metadata=1)
                    if "relative_y" not in list(data.keys()):
                        y = (indices((n,n))+1)[0].ravel()
                        gc.add_attribute(y[0:gc.size()], "relative_y", metadata=1)
                    resources.merge({key: gc})
                
                elif key == "household":
                    resources.merge({key: HouseholdDataset(in_storage=storage, in_table_name='data')})
                elif key == "development_project":
                    resources.merge({key: DevelopmentProjectDataset(in_storage=storage, in_table_name='data')})
                elif key == "development_event":
                    resources.merge({key: DevelopmentEventDataset(in_storage=storage, in_table_name='data')})   
                elif key == "neighborhood":
                    resources.merge({key: NeighborhoodDataset(in_storage=storage, in_table_name='data')})
                elif key == "job":
                    resources.merge({key: JobDataset(in_storage=storage, in_table_name='data')})                    
                elif key == "zone":
                    resources.merge({key: ZoneDataset(in_storage=storage, in_table_name='data')})
                elif key == "travel_data":
                    resources.merge({key: TravelDataDataset(in_storage=storage, in_table_name='data')})
                elif key == "faz":
                    resources.merge({key: FazDataset(in_storage=storage, in_table_name='data')})
                elif key == "fazdistrict":
                    resources.merge({key: FazdistrictDataset(in_storage=storage, in_table_name='data')})                    
                elif key == "race":
                    resources.merge({key: RaceDataset(in_storage=storage, in_table_name='data')})
                elif key == "county":
                    resources.merge({key: CountyDataset(in_storage=storage, in_table_name='data')})
                elif key == "large_area":
                    resources.merge({key: LargeAreaDataset(in_storage=storage, in_table_name='data')})
                elif key == "development_group":
                    resources.merge({key: DevelopmentGroupDataset(in_storage=storage, in_table_name='data')})
                elif key == "employment_sector_group":
                    resources.merge({key: EmploymentSectorGroupDataset(in_storage=storage, in_table_name='data')})        
                elif key == "plan_type_group":
                    resources.merge({key: PlanTypeGroupDataset(in_storage=storage, in_table_name='data')})
                elif key == "building":
                    resources.merge({key: BuildingDataset(in_storage=storage, in_table_name='data')})
                    
            else:
                resources.merge({key:data_dictionary[key]})

        if dataset in self.interactions:
            if dataset == "household_x_gridcell": 
                resources.merge({"dataset": HouseholdXGridcellDataset(dataset1=resources["household"], dataset2=resources["gridcell"])})
            if dataset == "job_x_gridcell":
                resources.merge({"dataset": JobXGridcellDataset(dataset1=resources["job"], dataset2=resources["gridcell"])})
            if dataset == "household_x_zone":
                resources.merge({"dataset": HouseholdXZoneDataset(dataset1=resources["household"], dataset2=resources["zone"])})
            if dataset == "household_x_neighborhood":
                resources.merge({"dataset": HouseholdXNeighborhoodDataset(dataset1=resources["household"], dataset2=resources["neighborhood"])})
            if dataset == "development_project_x_gridcell":
                resources.merge({"dataset": DevelopmentProjectXGridcellDataset(dataset1=resources["development_project"], dataset2=resources["gridcell"])})

        else:
            resources.merge({"dataset": resources[dataset]})
        resources.merge({"check_variables":'*', "debug":4})
        return resources

    def compute_variable(self, variable_name, data_dictionary, dataset, dataset_pool=None):
        """Compute variable 'variable_name' from fake data and return the computed values.
        Arguments:
            variable_name - name of variable to be computed
            data_dictionary - a dictionary where each key is either an item of the list self.datasets or the string 'urbansim_constant'.
                                Values of such entry are again dictionaries, where each key is
                                an attribute/variable/constant name and the value is a list of values for this attribute or a single
                                value in case of a constant.
            dataset - name of the dataset that the variable belongs to.
        """
        varname = VariableName(variable_name)
        resources = self.get_resources(data_dictionary, dataset)
        result = resources["dataset"].compute_variables(variable_name, 
                                               dataset_pool=dataset_pool, 
                                               resources=resources)
        return result