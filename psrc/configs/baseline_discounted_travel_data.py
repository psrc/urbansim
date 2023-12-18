# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from inprocess.psrc_zone.configs.create_post_year_configuration import create_post_year_configuration
from .baseline_copied_travel_data import BaselineCopiedTravelData

class BaselineDiscountedTravelData(BaselineCopiedTravelData):
    def __init__(self):
        BaselineCopiedTravelData.__init__(self)
        end_year = self['years'][1]
        self['post_year_configuration'] = create_post_year_configuration(end_year, travel_data_multiplication_factor=.50)
        