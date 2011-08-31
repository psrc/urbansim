# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc.parcel.SSS_within_walking_distance import SSS_within_walking_distance as PSRC_SSS_within_walking_distance

class SSS_package_SSS_wwd(PSRC_SSS_within_walking_distance):
    """Sum of a variable (given by the second SSS, defined in a package given by the first SSS) 
        over parcels connected to gridcells located within walking distance. If the variable is a primary attribute,
        the package is not used (but must be given).
        E.g. psrc_parcel.parcel.urbansim_parcel_package_population_wwd
        computes variable population urbansim_parcel.parcel.population and sums it over gridcells within walking distance.
    """
        
        
    def __init__(self, package, name):
        self.varpackage = package
        self.origname = name
        PSRC_SSS_within_walking_distance.__init__(self, name)
        
    def dependencies(self):
        return ['%s = gridcell.aggregate(%s.parcel.%s)' % (self.var_name, self.varpackage, self.origname),
                "gridcell.grid_id", 'parcel.grid_id']
