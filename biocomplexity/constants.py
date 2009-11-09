# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import ones

class Constants(dict):
    """ Sets some internal constants."""
    def __init__(self):
        self.set_internal_constants()

    def set_internal_constants(self):
        """ The maximum possible value for all dollar values (land, improvement,
        and total value) for a cell = 2,000,000,000
        """
        self["CELLSIZE"] = 30
        self["FOOTPRINT"] = ones(shape=(5,5), dtype="int8")
        # Land covers types
        self["HU"] = 1            # heavy urban
        self["MU"] = 2            # medium urban
        self["LU"] = 3            # light urban
        self["CDEV"] = 4          # cleared for development
        self["GR"] = 5            # grass
        self["MF"] = 6            # deciduous and mixed forest
        self["CF"] = 7            # coniferous forest
        self["CC"] = 8            # clearcut
        self["REGEN"] = 9         # regenerating forest
        self["AG"] = 10           # agriculture
        self["NFW"] = 11          # non-forested wetlands
        self["OW"] = 12           # open water
        self["BR"] = 13           # bare rock/ice/snow
        self["SH"] = 14           # shoreline
        self["ALL_URBAN"] = ["HU","MU","LU"]
        self["MED_LIGHT_URBAN"] = ["MU", "LU"]
        self["MED_HIGH_URBAN"] = ["MU", "HU"]
        self["FOREST"] = ["MF", "CF"]
        self["GRASS_AND_AG"] = ["GR", "AG"]





