# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import pandas as pd
from numpy import array, where, ones, zeros 
from numpy import arange, int32, float64
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import DatasetSubset
from urbansim.models.transition_model import TransitionModel

class CapDevelopmentModel(TransitionModel):
    """ 
    Model can be used to cap development if a geography-based growth rate is achieved.
    It compares the actual growth rate to the one derived from the control totals table.
    It adds a logical attribute to the dataset (e.g. parcels) with True for records where the growth rate
    has been achieved and thus the development should be capped. 
    Existing values are not overwritten be False, so that the model can be called multiple times with a cummulative effect.
        
    """
    
    model_name = "Cap Development Model"
    model_short_name = "CapDM"
    
    
    def run(self, target_attribute_name, year=None, ct_growth_attribute_name="control_total.growth_rate", 
            ct_geo_id_name='city_id', geo_id_name='faz_id', 
            cap_attribute_name="cap_development", annual=True, growth_rate=True, dataset_pool=None
            ):
        """ 

        **Parameters**
    
                **target_attribute_name** : string
                
                        Fully qualified name of dataset attribute that contains current level of growth, 
                        e.g. urbansim_parcel.parcel.number_of_households (or jobs). 
                        Corresponding lag attributes should be computable, 
                        e.g. urbansim_parcel.parcel.number_of_households_lag1.
                        Note that the dataset (here parcels) is passed to the init method.
                        
                **year** : int, optional
                
                        Simulation year. If unspecified, gets value from SimulationState

                **ct_growth_attribute_name**: string, optional
                        Fully qualified name of control totals attribute that gives the target growth 
                        (either as a rate or total value).
                        The control totals dataset is passed to the init method.
                        
                
                **ct_geo_id_name** : string, optional
                        Geography id name contained in the control totals dataset.
                        
                **geo_id_name** : string, optional
                        Geography id name for which the actual growth rate is computed.
                        
                **cap_attribute_name** : string, optional
                        Attribute name of the final results. It is attached/modified to the main dataset.
                        
                **annual** : Logical specifying if the growth should be annually prorated.
                
                **growth_rate** : Logical specifying if the ct_growth_attribute_name is a rate or total value.
                
                **dataset_pool** : OPUS DatasetPool object, optional                                                        
        
        """
        
        ## NOTE: always call compute_variables method on self.control_total_all instead of
        ## self.control_total, because there is a problem with DataSubset to handle index
        
        ct_growth = self.control_totals_all.compute_variables(ct_growth_attribute_name, dataset_pool=dataset_pool)
        
        if year is None:
            year = SimulationState().get_current_time()
        
        ctyear = self.control_totals_all['year'][(self.control_totals_all['year']<=year)*(self.control_totals_all[ct_geo_id_name]>0)].max()
        ctyear_next = self.control_totals_all['year'][(self.control_totals_all['year']>year)*(self.control_totals_all[ct_geo_id_name]>0)].min()
        ctyear_dif = ctyear_next - ctyear
        lag = year-ctyear
        
        ct_year_index = where((self.control_totals_all['year']==ctyear)*(self.control_totals_all[ct_geo_id_name]>0))[0]
        self.control_totals = DatasetSubset(self.control_totals_all, ct_year_index)        

        self.dataset.compute_one_variable_with_unknown_package(geo_id_name, dataset_pool=dataset_pool)
        self.dataset.compute_one_variable_with_unknown_package(ct_geo_id_name, dataset_pool=dataset_pool)
        target_values = self.dataset.compute_variables(target_attribute_name, dataset_pool=dataset_pool)
        target_values_lag = self.dataset.compute_variables("%s_lag%s" %(target_attribute_name, lag), dataset_pool=dataset_pool)
        
        data_df = {
            ct_geo_id_name: self.dataset[ct_geo_id_name],
            geo_id_name: self.dataset[geo_id_name],
            "target_attribute": target_values,
            "target_attribute_lag": target_values_lag  
        }
        df = pd.DataFrame(data_df, index=self.dataset.get_id_attribute())
        group_geo = df.groupby(geo_id_name).sum()
        group_geo['geo_growth'] = group_geo["target_attribute"]-group_geo["target_attribute_lag"]
        if growth_rate:
            group_geo['geo_growth'] = group_geo['geo_growth']/group_geo["target_attribute_lag"].astype('float32')
        should_grow = self.control_totals[ct_growth_attribute_name]
        if annual:
            should_grow = lag*should_grow/float(ctyear_dif)

        ctdf = pd.DataFrame({ct_growth_attribute_name: should_grow}, 
                            index=self.control_totals[ct_geo_id_name])
        
        df = df.merge(ctdf, how='left', left_on=ct_geo_id_name, right_index=True)
        df = df.merge(pd.DataFrame(group_geo['geo_growth']), how='left', left_on=geo_id_name, right_index=True)
        
        cap_pcl = df.index[df[ct_growth_attribute_name] < df['geo_growth']]
        dataset_idx = self.dataset.get_id_index(cap_pcl)
        if cap_attribute_name not in self.dataset.get_known_attribute_names():
            self.dataset.add_attribute(name=cap_attribute_name, data=zeros(self.dataset.size(), dtype='bool8'))
        self.dataset.modify_attribute(cap_attribute_name, ones(dataset_idx.size, dtype='bool8'), index=dataset_idx)
            
        return self.dataset



from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import all
from urbansim_parcel.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.control_total_dataset import ControlTotalDataset


class Tests(opus_unittest.OpusTestCase):

    def setUp(self):

        self.parcels_data = {
            "parcel_id": arange(7)+1,
            "faz_id": array(5*[1]+[2,2], dtype=int32),
            "number_of_households":      array([5, 10,1, 9, 7, 23, 20], dtype=int32),
            "number_of_households_lag1": array([4, 8, 1, 8, 7, 27, 18], dtype=int32),
            "city_id":                   array([1, 1, 2, 2, 2,  1,  1])
            }
        #                                                                 city 1: city 2:
        # total growth                          1  2  0  1   0  -4   2     1        1
        # growth rate                         .25 .25 0 .125 0  -.15 .11   0.02    0.06
        
        # after setting # HHs in the first parcel to 20:
        #                                                                 city 1: city 2:
        # total growth                         16  2  0  1   0  -4   2      16       1
        # growth rate                           4 .25 0 .125 0  -.15 .11   0.28    0.06

        self.annual_household_control_totals_data = {
            'year':                        array([2014, 2014, 2015,  2015, 2016, 2020, 2020,  2021, 2021]),
            'city_id':                     array([  -1,   -1,    1,     2,   -1,    2,    1,    -1,   -1]),
            'total_number_of_households':  array([  10,   20,    5,     6,   35,   11,    7,    17,   25]),
            "income":                      array([ 100,  200,   -1,    -1,   -1,   -1,   -1,   100,  200]),
        }
        # 2015-2020                       annual
        # city_id        1       2        1    2
        # growth rate    0.4    0.833   0.08  0.17
        # tot growth     2       5      0.4    1
        
        
    def test_cap_development_faz_growth_rate(self):
        """ Test using faz  and growth rate for controlling the growth.
        """
        
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='parcels', table_data=self.parcels_data)
        pcl = ParcelDataset(in_storage=storage, in_table_name='parcels')
        
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
                                   datasets_dict={'parcel': pcl})
        storage.write_table(table_name='ct', table_data=self.annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='ct', what='household',
                                      id_name=[])
        
        model = CapDevelopmentModel(pcl, control_total_dataset=hct_set)
        model.run(year=2016, ct_growth_attribute_name='psrc_parcel.control_total.household_growth_rate_luv', 
                  target_attribute_name="urbansim_parcel.parcel.number_of_households",
                  geo_id_name='faz_id', cap_attribute_name="target_achieved", dataset_pool=dataset_pool                
                  )
        # Only two parcels from faz 1 and city 1 exceeded the growth rate
        should_be = array([True, True] + 5*[False])
        self.assertEqual(all(should_be == pcl["target_achieved"]), True, "Error, should_be: %s, but result: %s" % (should_be, pcl["target_achieved"]))
        
    def test_cap_development_city_growth_rate(self):
        """ Test using city and growth rate for controlling the growth.
        """
                
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='parcels', table_data=self.parcels_data)
        pcl = ParcelDataset(in_storage=storage, in_table_name='parcels')
        pcl.modify_attribute("number_of_households", 20, index=0)
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
                                   datasets_dict={'parcel': pcl})
        storage.write_table(table_name='ct', table_data=self.annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='ct', what='household',
                                      id_name=[])
        
        model = CapDevelopmentModel(pcl, control_total_dataset=hct_set)
        model.run(year=2016, ct_growth_attribute_name='psrc_parcel.control_total.household_growth_rate_luv', 
                  target_attribute_name="urbansim_parcel.parcel.number_of_households",
                  geo_id_name='city_id', cap_attribute_name="target_achieved", dataset_pool=dataset_pool                
                  )
        # All parcels from city 1 exceeded the growth rate
        should_be = array([True, True, False, False, False, True, True])
        self.assertEqual(all(should_be == pcl["target_achieved"]), True, "Error, should_be: %s, but result: %s" % (should_be, pcl["target_achieved"]))  
        
    def test_cap_development_city_total_growth(self):
        """ Test using city and total growth for controlling the growth.
        """
                
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='parcels', table_data=self.parcels_data)
        pcl = ParcelDataset(in_storage=storage, in_table_name='parcels')
        pcl.modify_attribute("number_of_households", 20, index=0)
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
                                   datasets_dict={'parcel': pcl})
        storage.write_table(table_name='ct', table_data=self.annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='ct', what='household',
                                      id_name=[])
        
        model = CapDevelopmentModel(pcl, control_total_dataset=hct_set)
        model.run(year=2016, ct_growth_attribute_name='total_growth=0.95*psrc_parcel.control_total.household_total_growth_luv', 
                  target_attribute_name="urbansim_parcel.parcel.number_of_households", annual=False, growth_rate=False,
                  geo_id_name='city_id', cap_attribute_name="target_achieved", dataset_pool=dataset_pool                
                  )
        # All parcels from city 1 exceeded the growth
        should_be = array([True, True, False, False, False, True, True])
        self.assertEqual(all(should_be == pcl["target_achieved"]), True, "Error, should_be: %s, but result: %s" % (should_be, pcl["target_achieved"]))       

        
if __name__=='__main__':
    opus_unittest.main()
