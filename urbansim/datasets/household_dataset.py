# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array

class HouseholdDataset(UrbansimDataset):
    """Set of households."""

    id_name_default = "household_id"
    in_table_name_default = "households"
    out_table_name_default = "households"
    dataset_name = "household"
    
    def __init__(self, *args, **kwargs):
        UrbansimDataset.__init__(self, *args, **kwargs)               
        
        self.low_income_level = -1
        self.mid_income_level = -1

    def add_submodel_categories(self, categorize_attribute, submodel_categories, 
                                submodel_string="submodel_id"):
        """categorize household attribute into submodels
        categorize_attribute - the attribute used to categorize, for example, categorize_attribute = "workers";
        submodel_categories - category bins, for example, submodel_categories = array([0,1,2,5]),
                              the first category includes values less than or equal to the first bin,
                              while the last category includes only value larger than the last bin;
        submodel_string - the variable name identifying submodel_id
        """
        self.add_attribute(self.categorize(attribute_name=categorize_attribute, 
                bins=submodel_categories)+1, submodel_string)
                
    def calculate_income_levels(self, urbansim_constant):
        sortedincome = sort(self.get_attribute("income"))
        low_index = int(urbansim_constant["low_income_fraction"] * self.size())
        high_index =int((urbansim_constant["low_income_fraction"] + urbansim_constant["mid_income_fraction"]) \
                         * self.size())
        self.low_income_level = sortedincome[low_index]
        self.mid_income_level = sortedincome[high_index]
   

    def determine_movers(self):
        """Look for unplaced households (where grid_id < 0)"""
        return where(self.get_attribute("grid_id") < 0)[0]

        