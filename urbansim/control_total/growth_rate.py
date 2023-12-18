# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .abstract_growth_rate import abstract_growth_rate

class growth_rate(abstract_growth_rate):
    """"""
    target_attribute_name = 'population'
    attr_names = ['subarea_id', 'male']