# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from numpy import zeros, float32, exp, where, logical_or, compress, newaxis

class Abstract_Zone_Access_Variable(Variable):
    """Abstract superclass for the various zonal accessibility variables, for example
    home_access_to_employment_2 or work_access_to_population_2.  The actual OPUS
    variable name includes DDD, the number of cars per household (2 in the examples above).
    Thus, if the possibilities for number of cars per household are 0, 1, 2, or 3+ (3 or more),
    then DDD can be 0, 1, 2, or 3."""

    def __init__(self, ncars, attrname):
        """init method for zonal accessibility variables.  ncars is the number of cars per household,
        and attrname is the attribute (number_of_jobs or population) in the zones we range over to
        compute the accessibility.  For example, for home_access_to_employment_2, ncars is 2, and
        attrname is 'number_of_jobs'.  For work_access_to_population_2, ncars is again 2, and
        attrname is 'population'.   """
        self.num_cars = ncars
        self.attribute_name = attrname
        self.logsum_n = "logsum" + str(self.num_cars)
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data",self.logsum_n), my_attribute_label(self.attribute_name)]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        zone_ids = dataset.get_attribute("zone_id")
        attribute_value = dataset.get_attribute(self.attribute_name)
        travel_data = dataset_pool.get_dataset('travel_data')
        logsums = travel_data.get_attribute_as_matrix(self.logsum_n, fill=0)

        if self.access_is_from_origin():
            attribute_value = attribute_value[newaxis, :]
            axis=1    #sum by row
        else:
            attribute_value = attribute_value[:, newaxis]
            axis=0    #sum by column
        results = (attribute_value * exp(logsums[zone_ids,:][:,zone_ids])).sum(axis=axis)
        return results
    
    ##The original compute method is replaced by the current method above, which is faster and uses less memory
    ##The original compute method is commented out but kept below because of its better comments
    #def compute(self, dataset_pool):
        #zones = self.get_dataset()
        #attribute_value = zones.get_attribute(self.attribute_name)
        ## travel_data holds the logsums from the travel model
        #travel_data = dataset_pool.get_dataset('travel_data')
        ## pick out the logsums from the travel data for the given number of cars num_cars (this will be a 1-d array)
        #logsums = travel_data.get_attribute(self.logsum_n)
        ## get arrays of the from_zone_ids and to_zone_ids -- these will be in travel_data order
        #from_zone_ids = travel_data.get_attribute('from_zone_id')
        #to_zone_ids = travel_data.get_attribute('to_zone_id')
        ## Find the correponding from_zone and to_zone indices, but in the order used by zones.
        ## This is the order used for attribute_value, and also for the result we return.
        ## The travel data may have data for additional zones, so we need to use try_get_id_index
        ## rather than get_id_index to convert the from_zone_ids into indices into zones.  The
        ## default value returned by try_get_id_index if not found is -1.
        #from_indices = zones.try_get_id_index(from_zone_ids)   #these two lines are very slow with large memory footprints
        #to_indices = zones.try_get_id_index(to_zone_ids)
        ## zone_filter is an array of 0s and 1s ... a 1 value indicates that the corresponding element in the travel
        ## data is for a zone in the zones table, a 0 value indicates that it is for a zone that isn't in the zones
        ## table (and hence should be ignored).  The arrays from_indices, to_indices, and logsums are parallel, so
        ## zone_filter applies to all of them.  Note that if we have a -1 in EITHER the from_indices or to_indices
        ## we throw that out (i.e. assign 0 to the corresponding element in zone_filter).
        #zone_filter = where( logical_or(from_indices<0, to_indices<0), 0, 1)
        #filtered_from_indices = compress(zone_filter,from_indices)
        #filtered_to_indices = compress(zone_filter,to_indices)
        ## filtered_logsums is the 1-d array of logsum values for just the zones in the zone table
        #filtered_logsums = compress(zone_filter,logsums)
        ## now convert filtered_logsums into a 2-d array of the proper shape
        #logsum_2d = zeros((zones.size(),zones.size()),dtype=float32)
        ## choose the proper axis for the logsum_2d array depending on whether the access is for the origin (from) zone
        ## or for the destination (to) zone.
        #if self.access_is_from_origin():
            #logsum_2d[filtered_from_indices,filtered_to_indices] = filtered_logsums
        #else:
            #logsum_2d[filtered_to_indices, filtered_from_indices] = filtered_logsums

        ## multiply by the attribute value (number of jobs or population), and sum the elements in each row
        #return (attribute_value*exp(logsum_2d)).sum(axis=1)

    def access_is_from_origin(self):
        """return True if the access is for the origin (from) zone, and False if the access is for the destination zone.
        home_access_to* variables will return True, and work_access_to_* variables will return False."""
        raise NotImplementedError("subclass responsibility")

# the unit tests are in the concrete subclasses of this class
