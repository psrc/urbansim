# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from .developable_maximum_industrial_sqft import developable_maximum_industrial_sqft

class developable_maximum_commercial_sqft(developable_maximum_industrial_sqft):
    """How many commercial sqft are at most developable for each zone."""

    units = "buildings_commercial_sqft"
    total_maximum = "total_maximum_development_commercial"

