# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.length_constants import UrbanSimLengthConstants, UrbanSimLength
from numpy import ones, where, float32
from scipy.ndimage import distance_transform_edt
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

class Constants(dict):
    """ Load constants and sets some internal constants."""
    def __init__(self, in_storage=None, in_table_name='urbansim_constants', set_values=True):
        self.set_internal_constants()
        if set_values:
            self.load_constants(in_storage, in_table_name)
            self.set_computed_constants()

    _commercial_code = 1
    _governmental_code = 2
    _industrial_code = 3
    _residential_code = 4

    def load_constants(self, in_storage, in_table_name):
        """Some of the constants are loaded from in_storage.
        """
        result = in_storage.load_table(table_name=in_table_name)
        if result is None:
            logger.log_warning("No data in table '%s'" % in_table_name)
        else:
            for name in result:
                self[name] = result[name][0]

    def set_computed_constants(self):
        try:
            self.set_near_arterial_threshold()
        except:
            pass
        try:
            self.set_near_highway_threshold()
        except:
            pass
        try:
            self.set_walking_distance_footprint()
        except:
            pass
        try:
            self.set_gridcell_width_and_height()
        except:
            pass
        try:
            self.set_acres()
        except:
            pass

    def get_income_range_for_type(self, income_type):
        """For the given type, return a range of incomes
        corresponding to the min and max incomes for this range.
        The min income is inclusive and the max income is exclusive. 
        Either user-specific ranges are taken defined in constants called
        'income_category_{income_type}_min' and 'income_category_{income_type}_max',
        or internal ranges are returned, if the user-specific ones are not set.
        """
        all_consts = self.keys()
        if "income_category_%s_min" % income_type in all_consts and "income_category_%s_max" % income_type in all_consts:
            return (self["income_category_%s_min" % income_type], self["income_category_%s_max" % income_type])
        if income_type == 1: return (0, 25000)
        if income_type == 2: return (25000, 45000)
        if income_type == 3: return (45000, 75000)
        if income_type == 4: return (75000, self["absolute_max_income"])
        raise StandardError("No range for income type: %s" % str(income_type))

    def set_near_arterial_threshold(self):
        self["near_arterial_threshold_unit"] = UrbanSimLength(self["near_arterial_threshold"],
                UrbanSimLengthConstants().get_units_constant(self["units"]))

    def set_near_highway_threshold(self):
        self["near_highway_threshold_unit"] = UrbanSimLength(self["near_highway_threshold"],
                UrbanSimLengthConstants().get_units_constant(self["units"]))

    def set_walking_distance_footprint(self):
        wd_gc = int(2*self["walking_distance_circle_radius"]/self["cell_size"]+1)
        center = (wd_gc-1)/2
        distance = ones((wd_gc,wd_gc), dtype=float32)
        distance[center,center]=0.0
        distance = distance_transform_edt(distance)
        self["walking_distance_footprint"] = where(distance*self["cell_size"] <= self["walking_distance_circle_radius"], 1, 0)

    def set_gridcell_width_and_height(self):
        self["gridcell_width"] = UrbanSimLength(self["cell_size"], UrbanSimLengthConstants().units_meters)
        self["gridcell_height"]= UrbanSimLength(self["cell_size"], UrbanSimLengthConstants().units_meters)

    def set_acres(self):
        if 'acres' not in self:
            self["acres"] = self["gridcell_width"].value_in_units(UrbanSimLengthConstants().units_meters) \
                * self["gridcell_height"].value_in_units(UrbanSimLengthConstants().units_meters) * 0.0002471 # acres/sq m

    def set_internal_constants(self):
        """ Maximum possible value for income = 2,000,000,000
        """
        self["absolute_max_income"] = 2000000000
        """ Minimum possible value for year = 0
        """
        self["absolute_min_year"] = 1800
        """ Maximum travel time = 1440
        """
        self["absolute_max_travel_time"] = 60 * 24
        """ Maximum population we might be interested in = 50,000,000
        """
        self["absolute_max_population"] = 50000000
        """ The maximum number of subcells in a grid cell = 121
        """
        self["absolute_max_subcells"] = 121

        self["industrial_code"] = self._industrial_code
        self.industrial_code = self["industrial_code"]
        self["commercial_code"] = self._commercial_code
        self.commercial_code = self["commercial_code"]
        self["governmental_code"] = self._governmental_code
        self.governmental_code = self["governmental_code"]
        self["residential_code"] = self._residential_code
        self.residential_code = self["residential_code"]

    def uppercase(self):
        for key in self.keys():
            self[key.upper()]=self[key]

