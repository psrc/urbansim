#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from numpy import sqrt, apply_along_axis, log, exp, maximum
from numpy.random import normal

from opus_core.misc import DebugPrinter
from opus_core.datasets.dataset import Dataset
from opus_core.resource_factory import ResourceFactory
from opus_core.variables.attribute_type import AttributeType

from urbansim.opus_package_info import package


class ControlTotalDataset(Dataset):
    id_name_default = {"household":["year"],
                        "employment":["year", "sector_id"]}

    def __init__(self, resources=None, what="household", in_storage=None,
            in_table_name=None, attributes=None, out_storage=None,
            out_table_name=None, id_name=None, nchunks=None, debuglevel=0):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating ControlTotalDataset object for "+what+".",2)

        in_table_name_default = "annual_" + what + "_control_totals"
        attributes_default = AttributeType.PRIMARY
        out_table_name_default = in_table_name_default
        dataset_name = "control_total"
        nchunks_default = 1

        resources = ResourceFactory().get_resources_for_dataset(
            dataset_name,
            resources=resources,
            in_storage=in_storage,
            out_storage=out_storage,
            in_table_name_pair=(in_table_name,in_table_name_default),
            attributes_pair=(attributes,attributes_default),
            out_table_name_pair=(out_table_name, out_table_name_default),
            id_name_pair=(id_name,self.id_name_default[what]),
            nchunks_pair=(nchunks,nchunks_default),
            debug_pair=(debug,None)
            )

        self.what = what
        if (id_name == None) and (what == "household"): # determine id_name depending on the columns in the table
            id_names = resources["in_storage"].determine_field_names(resources)
            if "year" in id_names:
                id_names.remove("year")
            if "total_number_of_households" in id_names:
                id_names.remove("total_number_of_households")
            resources.merge({"id_name":resources["id_name"] + id_names})

        Dataset.__init__(self,resources = resources)

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
            storage._write_dataset(
                    control_totals_table_name,
                    {
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

        # check if the means (on the log scale) are the control totals themselves
        expected_results = log(concatenate([household_totals, job_totals]))
        self.run_stochastic_test(__file__, run_model, expected_results, 20, type='normal',transformation=None,
                                 significance_level=0.01)

        # check if the variances correspond to variance * years
        def run_stochastic_test():
            self.compute_stochastic_test_normal(run_model, expected_results, 10, transformation=None)
            return self.variance
        expected_variance = concatenate((arange(1, 7) * array(6*[variance]), arange(1, 7) * array(6*[variance])))
        # The variance distribution (chi-squared with n-1 df) is approximated by the normal distr.
        # In this case n (number of replicates) should be more than 15.
        self.run_stochastic_test(__file__, run_stochastic_test, expected_variance, 20, type='normal',
                                 significance_level=0.01)

if __name__=='__main__':
    opus_unittest.main()