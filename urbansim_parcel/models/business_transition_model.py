# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter, unique
from opus_core.model import Model
from numpy import arange, array, where, int8, zeros, ones, compress, int32, concatenate
from numpy import logical_not
from scipy.ndimage import sum as ndimage_sum
from opus_core.sampling_toolbox import sample_noreplace, probsample_replace
from opus_core.logger import logger

class BusinessTransitionModel(Model):
    """Creates and removes businesses from business_set."""

    model_name = "Business Transition Model"
    location_id_name = "building_id"
    variable_package = "urbansim_parcel"

    def __init__(self, debuglevel=0):
        self.debug = DebugPrinter(debuglevel)

    def run(self, year, business_set,
            control_totals,
            data_objects=None,
            resources=None):
        business_id_name = business_set.get_id_name()[0]
        control_totals.get_attribute("total_number_of_businesses")
        idx = where(control_totals.get_attribute("year")==year)
        sectors = unique(control_totals.get_attribute_by_index("building_use_id", idx))
        max_id = business_set.get_id_attribute().max()
        business_size = business_set.size()
        new_businesses = {self.location_id_name:array([], dtype='int32'),
                          "building_use_id":array([], dtype='int32'),
                          business_id_name:array([], dtype='int32'),
                          "sqft":array([], dtype=int32),
                          "employees":array([], dtype=int32),}
        compute_resources = Resources(data_objects)
#        compute_resources.merge({job_building_types.get_dataset_name():job_building_types, "debug":self.debug})
        business_set.compute_variables(
            map(lambda x: "%s.%s.is_sector_%s"
                    % (self.variable_package, business_set.get_dataset_name(), x),
                sectors),
            resources = compute_resources)
        remove_businesses = array([], dtype='int32')

        for sector in sectors:
            total_businesses = control_totals.get_data_element_by_id((year,sector)).total_number_of_businesses
            is_in_sector = business_set.get_attribute("is_sector_%s" % sector)
            diff = int(total_businesses - is_in_sector.astype(int8).sum())

            if diff < 0: #
                w = where(is_in_sector == 1)[0]
                sample_array, non_placed, size_non_placed = \
                    get_array_without_non_placed_agents(business_set, w, -1*diff,
                                                         self.location_id_name)
                remove_businesses = concatenate((remove_businesses, non_placed,
                                           sample_noreplace(sample_array, max(0,abs(diff)-size_non_placed))))

            if diff > 0: #
                new_businesses[self.location_id_name]=concatenate((new_businesses[self.location_id_name],zeros((diff,), dtype="int32")))
                new_businesses["building_use_id"]=concatenate((new_businesses["building_use_id"],
                                                               sector*ones((diff,), dtype="int32")))

                available_business_index = where(is_in_sector)[0]
                sampled_business = probsample_replace(available_business_index, diff, None)

                new_businesses["sqft"] = concatenate((new_businesses["sqft"],
                                                     business_set.get_attribute("sqft")[sampled_business]))
                new_businesses["employees"] = concatenate((new_businesses["employees"],
                                                           business_set.get_attribute("employees")[sampled_business]))

                new_max_id = max_id+diff
                new_businesses[business_id_name]=concatenate((new_businesses[business_id_name], arange(max_id+1, new_max_id+1)))
                max_id = new_max_id

        business_set.remove_elements(remove_businesses)
        business_set.add_elements(new_businesses, require_all_attributes=False)
        difference = business_set.size()-business_size
        self.debug.print_debug("Difference in number of businesses: %s (original %s,"
            " new %s, created %s, deleted %s)"
                % (difference,
                   business_size,
                   business_set.size(),
                   new_businesses[business_id_name].size,
                   remove_businesses.size),
            3)
        self.debug.print_debug("Number of unplaced businesses: %s"
            % where(business_set.get_attribute(self.location_id_name) <=0)[0].size,
            3)
        return difference

    def prepare_for_run(self, storage, in_table_name, id_name, **kwargs):
        from urbansim.datasets.control_total_dataset import ControlTotalDataset
        control_totals = ControlTotalDataset(in_storage=storage,
                                             in_table_name=in_table_name,
                                             id_name=id_name
                                         )
#        sample_control_totals(storage, control_totals, **kwargs)
        return control_totals


def get_array_without_non_placed_agents(business_set, arr, max_value=None, location_id_name="grid_id"):
    if location_id_name in business_set.get_known_attribute_names():
        non_placed = where(business_set.get_attribute_by_index(location_id_name, arr) <= 0)[0]
    else:
        non_placed=array([], dtype='int32')
    size_non_placed = non_placed.size
    if size_non_placed <= 0:
        return (arr, non_placed, 0)
    if (max_value is not None) and (size_non_placed > max_value):
        non_placed = sample_noreplace(non_placed, max_value)
        size_non_placed = non_placed.size
    a = ones((arr.size,), dtype="int8")
    a[non_placed] = 0
    return (compress(a, arr), arr[non_placed], size_non_placed)

def sample_control_totals(storage, control_totals, sample_control_totals=False, variance=1, multiplicator=1,
                        base_year=None, flush_control_totals=True):
    if sample_control_totals:
        if flush_control_totals:
            cache_storage=storage
        else:
            cache_storage=None
        control_totals.sample_control_totals(variance, base_year, cache_storage=cache_storage,
                                    multiplicator=multiplicator)

