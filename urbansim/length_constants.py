# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# Transfered from the java source code UrbanSimLength.java

"""
  Encapsulates a measurement, with both the scalar quantity and the
  units of measurement.
"""

class UrbanSimLengthConstants(object):
    def __init__(self):
        """
        Symbolic constant for meters
        """
        self.units_meters = 0
        """
        Symbolic constant for feet
        """
        self.units_feet = 1
        """
        Symbolic constant for miles
        """
        self.units_miles = 2
        """ 
        Symbolic constant for km
        """
        self.units_kilometers = 3
        """
        Number of units declared as constants.
        """
        self.num_units = 4
        """
        Number of feet in a meter
        """
        self.feet_per_meter = 3.28084
        """
        Number of feet in a mile
        """
        self.feet_per_mile = 5280.0
        self.tolerance = .00001
        
    def get_units_constant(self, units):
        if units == "meters":
            return self.units_meters
        elif units == "feet":
            return self.units_feet
        elif units == "miles":
            return self.units_miles
        elif units == "kilometers":
            return self.units_kilometers
        return -1

class UrbanSimLength(object):
    def __init__(self, value=0, units=0):    
        self.constants = UrbanSimLengthConstants()    
        self.value = value
        # catch unit out of bounds errors before they happen
        if not(units < self.constants.num_units and units >= 0):
            raise StandardError, "Invalid units in UrbanSimLength"
        self.units = units

    def less_than(self, other):
        this_meters = self.convert_to_meters()
        other_meters = other.value_in_units(self.constants.units_meters)
        return this_meters < other_meters
    
    def convert_to_meters(self):
        converted = 0
        if self.units == self.constants.units_feet:
            converted = self.value / self.constants.feet_per_meter
        elif self.units == self.constants.units_meters:
            converted = self.value
        elif self.units == self.constants.units_kilometers:
            converted = self.value * 1000
        elif self.units == self.constants.units_miles:
            converted = (self.value * self.constants.feet_per_mile) / self.constants.feet_per_meter
        else:
            raise StandardError, "Error: invalid type of units in UrbanSimLength"
        return converted
        
    """
    Get the value of this length in the units specified
    """
    def value_in_units(self, units):
        converted = 0
        length_in_meters = self.convert_to_meters()
        if units == self.constants.units_feet :
            converted = length_in_meters * self.constants.feet_per_meter
        elif units == self.constants.units_meters :
            converted = length_in_meters;
        elif units == self.constants.units_kilometers :
            converted = length_in_meters / 1000;
        elif units == self.constants.units_miles :
            converted = length_in_meters * self.constants.feet_per_meter / self.constants.feet_per_mile
        else:
            raise StandardError, "Error: invalid type of units in UrbanSimLength"
        return converted

