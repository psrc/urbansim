# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.model import Model
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.logger import logger
from numpy import where, ones, zeros, logical_and, clip, round_

class AllocationModel(Model):
    """ Model allocates given quantity according to weights while meeting capacity restrictions.
    """
    model_name = "Allocation Model"

    def run(self, dataset, outcome_attribute, weight_attribute, 
                 control_totals, current_year, control_total_attribute=None, 
                 year_attribute='year', capacity_attribute=None, add_quantity=False, dataset_pool=None):
        """'dataset' is a Dataset for which a quantity 'outcome_attribute' is created. The total amount of the quantity is 
        given by the attribute 'control_total_attribute' of the 'control_totals' Dataset. If it is not given, it is assumed 
        to have the same name as 'outcome_attribute'. The 'weight_attribute' of 'dataset' determines the allocation weights.
        The 'control_totals' Dataset contains an attribute 'year' (or alternatively, an attribute given by the 'year_attribute' argument)
        and optionally other attributes that must be known to the 'dataset' (such as a geography). For each row of the control_totals dataset
        for which year matches the 'current_year', the total amount is distributed among the corresponding members of 'dataset' according to weights.
        If a 'capacity_attribute' is given (attribute of 'dataset'), the algorithm removes any allocations that exceeds the capacity and 
        redistributes it among remaining members. The resulting values are appended to 'dataset' as 'outcome_attribute' (as primary attribute).
        If add_quantity is True and the 'outcome_attribute' exists in dataset, the resulting values are added to the current values of 
        'outcome_attribute'.
        """
        ct_attr = control_totals.get_known_attribute_names()
        if year_attribute not in ct_attr:
            raise StandardError, "Year attribute '%s' must be a known attribute of the control totals dataset." % year_attribute
        ct_attr.remove(year_attribute)
        if control_total_attribute is None:
            control_total_attribute = outcome_attribute
        if control_total_attribute not in ct_attr:
            raise StandardError, "Attribute '%s' must be a known attribute of the control totals dataset." % control_total_attribute
        ct_attr.remove(control_total_attribute)
        if control_totals._is_hidden_id():
            ct_attr.remove(control_totals.id_name()[0])
            
        # compute weights and other attributes necessary for allocation
        attrs_to_compute = [weight_attribute] + ct_attr
        if capacity_attribute is not None:
            attrs_to_compute.append(capacity_attribute)
        for attr in attrs_to_compute:
            try:
                dataset.compute_variables(attr, dataset_pool=dataset_pool)
            except:
                dataset.compute_one_variable_with_unknown_package(attr, dataset_pool=dataset_pool)
        
        # create subset of control totals for the current year
        year_index = where(control_totals.get_attribute(year_attribute) == current_year)[0]
        if year_index.size <= 0:
            logger.log_warning("No control total for year %s" % current_year)
            return None
        control_totals_for_this_year = DatasetSubset(control_totals, year_index)
        
        # check capacity
        if capacity_attribute is not None:
            if dataset.get_attribute(capacity_attribute).sum() < control_totals_for_this_year.get_attribute(control_total_attribute).sum():
                logger.log_warning("Capacity (%s) is smaller than the amount to allocate (%s)." % (dataset.get_attribute(capacity_attribute).sum(), 
                                                                                                  control_totals_for_this_year.get_attribute(control_total_attribute).sum()))
            C = dataset.get_attribute(capacity_attribute).astype('int32')
            
        all_weights = dataset.get_attribute(weight_attribute)
        outcome = zeros(dataset.size(), dtype='int32')
        for ct_row in range(control_totals_for_this_year.size()):
            is_considered = ones(dataset.size(), dtype='bool8')
            for characteristics in ct_attr:
                is_considered = logical_and(is_considered, dataset.get_attribute(characteristics) == control_totals_for_this_year.get_attribute(characteristics)[ct_row])
            T = control_totals_for_this_year.get_attribute(control_total_attribute)[ct_row]
            it = 1
            while True:
                is_considered_idx = where(is_considered)[0]
                weights = all_weights[is_considered_idx]
                weights_sum = float(weights.sum())
                outcome[is_considered_idx] = round_(outcome[is_considered_idx] + T * weights/weights_sum).astype('int32')
                if capacity_attribute is None:
                    break
                diff = outcome[is_considered_idx] - C[is_considered_idx]
                outcome[is_considered_idx] = clip(outcome[is_considered_idx], 0, C[is_considered_idx])
                if it == 1 and C[is_considered_idx].sum() < T:
                    logger.log_warning("Control total %s cannot be met due to a capacity restriction of %s" % (T, C[is_considered_idx].sum()))
                T = where(diff < 0, 0, diff).sum()
                if T <= 0:
                    break
                is_considered = logical_and(is_considered, outcome < C)
                it += 1
        if add_quantity and (outcome_attribute in dataset.get_known_attribute_names()):
            dataset.modify_attribute(name=outcome_attribute, data=outcome+dataset.get_attribute(outcome_attribute))
            logger.log_status('New values added to the attribute %s of dataset %s.' % (outcome_attribute, dataset.get_dataset_name()))
        else:
            dataset.add_primary_attribute(name=outcome_attribute, data=outcome)
            logger.log_status('New values stored into attribute %s of dataset %s.' % (outcome_attribute, dataset.get_dataset_name()))
        dataset.flush_attribute(outcome_attribute)
        return outcome
    
    def prepare_for_run(self, storage, control_totals_table_name, control_totals_id_name, control_totals_dataset_name='control_totals'):
        control_totals = Dataset(in_storage=storage, in_table_name=control_totals_table_name, id_name=control_totals_id_name, 
                                 dataset_name=control_totals_dataset_name)
        return control_totals
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma

class AllocationModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        zone_data = {
            'zone_id': arange(3)+1,
            }
        job_data = {
            'job_id': arange(10)+1,
             'zone_id': array([          2,    3,   2,   1,  1,   1,  3,  2,  2,  3]),
            'allocation_weights': array([1,    3,   5,   2,  1,   4,  7,  9,  8,  2]),
            'job_sqft_capacity':  array([3000,2800,1000,550,600,1000,2000,500,100,1000])
        }
        control_total_data = {
            'year': array([2005,2005,2005,2006, 2006, 2006]),
            'zone_id':  array([1,      2,    3,    1,   2,    3]),
            'job_sqft': array([2000, 5500, 1000, 3000, 6000, 2000]),           
                          }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'zones', table_data = zone_data)
        storage.write_table(table_name = 'jobs', table_data = job_data)
        storage.write_table(table_name = 'control_totals', table_data = control_total_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['opus_core'])
        self.ct = Dataset(in_storage=storage, in_table_name='control_totals', id_name=['year', 'zone_id'], dataset_name='control_total')
        self.jobs = self.dataset_pool.get_dataset('job')
        
    def test_allocation_without_capacity(self):
        model = AllocationModel()
        model.run(self.jobs, outcome_attribute='job_sqft', weight_attribute='allocation_weights',
                  control_totals=self.ct, current_year=2005, dataset_pool=self.dataset_pool)
        result = self.jobs.get_attribute('job_sqft')
        #check total sums
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==1].sum() == 2000, True)
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==2].sum() == 5500, True)
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==3].sum() == 1000, True)
        #check if resulting proportions correspond to weights
        res = result[self.jobs.get_attribute('zone_id')==1]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([2, 1, 4])/7.0, rtol=0.01), True)
        res = result[self.jobs.get_attribute('zone_id')==2]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([1, 5, 9, 8])/23.0, rtol=0.01), True)
        res = result[self.jobs.get_attribute('zone_id')==3]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([3, 7, 2])/12.0, rtol=0.01), True)
        
        # add quantity to results from previous year
        result_2005 = result.copy()
        model.run(self.jobs, outcome_attribute='job_sqft', weight_attribute='allocation_weights',
                  control_totals=self.ct, current_year=2006, add_quantity=True, dataset_pool=self.dataset_pool)
        result = self.jobs.get_attribute('job_sqft') - result_2005
        #check total sums
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==1].sum() == 3000, True)
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==2].sum() == 6000, True)
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==3].sum() == 2000, True)
        #check if resulting proportions correspond to weights
        res = result[self.jobs.get_attribute('zone_id')==1]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([2, 1, 4])/7.0, rtol=0.01), True)
        res = result[self.jobs.get_attribute('zone_id')==2]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([1, 5, 9, 8])/23.0, rtol=0.01), True)
        res = result[self.jobs.get_attribute('zone_id')==3]
        self.assertEqual(ma.allclose(res/float(res.sum()), array([3, 7, 2])/12.0, rtol=0.01), True)
        
    def test_allocation_with_capacity(self):
        model = AllocationModel()
        model.run(self.jobs, outcome_attribute='job_sqft', weight_attribute='allocation_weights',
                  control_totals=self.ct, current_year=2005, capacity_attribute='job_sqft_capacity', dataset_pool=self.dataset_pool)
        result = self.jobs.get_attribute('job_sqft')
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==1].sum() == 2000, True)
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==2].sum() == 4600, True) # due to capacity restrictions
        self.assertEqual(result[self.jobs.get_attribute('zone_id')==3].sum() == 1000, True)
        
if __name__=="__main__":
    opus_unittest.main()