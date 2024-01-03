# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import arange, logical_and, where
from opus_core.model import Model

class CorrectLandValue(Model):
    """ Corrects land value to avoid land value decline with dev type change.
    """
    
    model_name = "Correct Land Value"
    model_short_name = "Correct LV"
                        
    def run(self, dataset, index=None, submodel_string="development_type_id", debuglevel=0):
        if index == None:
            index = arange(dataset.size())
        residential_land_value = dataset.get_attribute_by_index("residential_land_value", index)
        nonresidential_land_value = dataset.get_attribute_by_index("nonresidential_land_value", index)
        total_land_value = residential_land_value + nonresidential_land_value

        dataset.compute_variables(["urbansim.%s.%s_lag2" % (dataset.get_dataset_name(),submodel_string),
                                   "urbansim.%s.residential_land_value_lag1" % dataset.get_dataset_name(),                                                                       
                                   "urbansim.%s.nonresidential_land_value_lag1" % dataset.get_dataset_name()                                                                        ])
            
        previous_dev_type = dataset.get_attribute_by_index("%s_lag2" % submodel_string, index)
        current_dev_type = dataset.get_attribute_by_index(submodel_string, index)
        change_indicator = (previous_dev_type != current_dev_type)
            
        previous_residential_land_value = dataset.get_attribute_by_index("residential_land_value_lag1", index) 
        previous_nonresidential_land_value = dataset.get_attribute_by_index("nonresidential_land_value_lag1", index)    
        previous_total_land_value = previous_residential_land_value + previous_nonresidential_land_value
        reduction_indicator = (total_land_value < previous_total_land_value)
            
        #replace those cells with previous value where a dev type change and land value reduction
        replace_idx = where(logical_and(change_indicator, reduction_indicator))
        new_residential_land_value = previous_residential_land_value[replace_idx]
        new_nonresidential_land_value = previous_nonresidential_land_value[replace_idx]
        dataset.modify_attribute("residential_land_value", new_residential_land_value, index[replace_idx])
        dataset.modify_attribute("nonresidential_land_value", new_nonresidential_land_value, index[replace_idx])
        return replace_idx
    

from opus_core.tests import opus_unittest
from numpy import array, ma
from urbansim.datasets.gridcell_dataset import GridcellDataset
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification 
from urbansim.models.land_price_model import LandPriceModel
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
        
    def test_correct_land_value(self):
        #TODO: need to remove this when fixed LP correction only working when year >= 2002
        from opus_core.simulation_state import SimulationState
        SimulationState().set_current_time(2002)
        
        storage = StorageFactory().get_storage('dict_storage')

        gridcell_set_table_name = 'gridcell_set'        
        storage.write_table(
            table_name=gridcell_set_table_name,
            table_data={
                "percent_residential_within_walking_distance":array([30, 0, 90, 100]),
                "gridcell_year_built":array([2002, 1968, 1880, 1921]),
                "fraction_residential_land":array([0.5, 0.1, 0.3, 0.9]),
                "residential_land_value":array([0, 0, 0, 0]),                          
                "residential_land_value_lag1":array([15000, 0, 7500, 0]),
                "nonresidential_land_value":array([0, 0, 0, 0]),  
                "nonresidential_land_value_lag1":array([15000, 0, 17500, 0]),                                                                    
                "development_type_id":array(  [2, 1, 1, 1]),
                "development_type_id_lag2":array(  [1, 1, 1, 1]),
                "grid_id": array([1,2,3,4])
                }
            )

        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        specification = EquationSpecification(variables=(
            "percent_residential_within_walking_distance", 
            "gridcell_year_built", "constant"), 
            coefficients=("PRWWD", "YB", "constant"))
        coefficients = Coefficients(names=("constant", "PRWWD", "YB"), values=(10.0, -0.0025, 0.0001))
        lp = LandPriceModel(filter=None, debuglevel=3)
        lp.run(specification, coefficients, gridcell_set)
        correctmodel = CorrectLandValue()
        correctmodel.run(gridcell_set)
        result1 = gridcell_set.get_attribute("residential_land_value")
        result2 = gridcell_set.get_attribute("nonresidential_land_value")
        self.assertEqual(ma.allclose(result1, array([15000.0,  2681.723,  6367.914, 18708.617]), rtol=1e-3), True)
        self.assertEqual(ma.allclose(result2, array([15000.0,  24135.510, 14858.466,  2078.735]), rtol=1e-3), True)
    

if __name__=="__main__":
    opus_unittest.main()