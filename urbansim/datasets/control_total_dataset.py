# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from numpy import sqrt, apply_along_axis, log, exp, maximum
from numpy.random import normal

from opus_core.misc import DebugPrinter
from opus_core.datasets.dataset import Dataset
from opus_core.resource_factory import ResourceFactory
from opus_core.variables.attribute_type import AttributeType

class ControlTotalDataset(Dataset):
    in_table_name_default = ""
    out_table_name_default = ""
    id_name_default = []
    dataset_name = "control_total"

    def __init__(self, resources=None, what="household", in_storage=None,
                 in_table_name=None, out_storage=None, out_table_name=None, 
                 id_name=None, nchunks=None, debuglevel=0):
        ## TODO remove "what" arguement
        
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating ControlTotalDataset object for "+what+".",2)
        
        if not self.in_table_name_default:
            self.in_table_name_default = "annual_" + what + "_control_totals"
        if not self.out_table_name_default:         
            self.out_table_name_default = "annual_" + what + "_control_totals"
            
        attributes_default = AttributeType.PRIMARY
        #dataset_name = "control_total"
        nchunks_default = 1

        resources = ResourceFactory().get_resources_for_dataset(
            self.dataset_name,
            resources=resources,
            in_storage=in_storage,
            out_storage=out_storage,
            in_table_name_pair=(in_table_name,self.in_table_name_default),
            attributes_pair=(None, attributes_default),
            out_table_name_pair=(out_table_name, self.out_table_name_default),
            id_name_pair=(id_name,self.id_name_default),
            nchunks_pair=(nchunks,nchunks_default),
            debug_pair=(debug,None)
            )
        
        table_name = resources["in_table_name"]
        if resources['id_name'] is None or len(resources['id_name'])== 0:
            #if both self.id_name_default and id_name argument in __init__ is unspecified, 
            #ControlTotalDataset would use all attributes not beginning with "total"
            #as id_name
            id_names = []
            column_names = resources["in_storage"].get_column_names(table_name)
            for column_name in column_names:
                if not re.search('^total', column_name):
                    id_names.append(column_name)
            resources.merge({"id_name":resources["id_name"] + id_names})

        Dataset.__init__(self, resources = resources)

    def sample_control_totals(self, variance, base_year=None, cache_storage=None, multiplicator=1):
        """ Sample control totals with given variance (multiplied by the given multiplicator)
            and cache results if cache_storage is given. The variance is meant as variance (on the log scale) per year,
            therefore it is multiplied by the difference between base year and the particular year.
            The smapling is done on the log scale and then transformed back.
        """
        years = self.get_attribute("year")
        attr_names = self.get_known_attribute_names()
        if base_year is None:
            base_year = years.min()-1
        for attr in attr_names:
            if (attr in self.get_id_name()) or (attr == "year"):
                continue
            raw_values = self.get_attribute(attr)
            values = log(raw_values)

            sd = sqrt(maximum(years - base_year, 1)*variance)
            def draw_rn (mean_var, n):
                return normal(mean_var[0], mean_var[1], size=n)
            sampled_values = apply_along_axis(draw_rn, 0, (values, multiplicator*sd), 1).reshape((values.size,))
            self.add_primary_attribute(name=attr, data=exp(sampled_values).round().astype(raw_values.dtype))
        if cache_storage is not None:
            self.write_dataset(out_storage=cache_storage)

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory
from numpy import array, arange, concatenate

class Tests(StochasticTestCase):
    def test_sampling_control_totals(self):
        household_totals = array([250, 1000, 1500, 1300, 2000, 1500])
        job_totals = array([20, 54, 10, 32, 43, 30])
        variance = 0.001
        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            control_totals_table_name = 'control_totals'
            storage.write_table(
                    table_name=control_totals_table_name,
                    table_data={
                        'year': arange(1980, 1986),
                        'totals_for_households': household_totals,
                        'totals_for_jobs': job_totals,
                        'sector_id': array([1,1,1,2,2,2])
                        }
                    )

            control_totals = ControlTotalDataset(in_storage=storage, in_table_name=control_totals_table_name,
                                                 what='employment')

            control_totals.sample_control_totals(variance)
            result = concatenate((control_totals.get_attribute('totals_for_households'),
                                control_totals.get_attribute('totals_for_jobs')))
            return log(result)

        # Test the variance using Chi^2 hypothesis test with known means. These are the log of control totals.
        expected_results = log(concatenate([household_totals, job_totals]))
        self.chi_square_test_with_known_mean(run_model, expected_results, array(2*job_totals.size*[5*variance]), 10, significance_level=0.0001)


if __name__=='__main__':
    opus_unittest.main()