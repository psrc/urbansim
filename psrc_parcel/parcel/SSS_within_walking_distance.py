# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc.parcel.SSS_within_walking_distance import SSS_within_walking_distance as PSRC_SSS_within_walking_distance

class SSS_within_walking_distance(PSRC_SSS_within_walking_distance):
    """Sum over c in cell.walking_radius, c.residential_units."""
        
    def dependencies(self):
        return ['grid_id=household.disaggregate(parcel.grid_id, intermediates=[building])',
                'grid_id=job.disaggregate(parcel.grid_id, intermediates=[building])',
                'urbansim.gridcell.' + self.var_name,
                "gridcell.grid_id",
                'parcel.grid_id']
