# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
        "is_residential = development_project.disaggregate(building_type.is_residential)",
        "is_non_residential = numpy.logical_not(urbansim_zone.development_project.is_residential)",
           ]
