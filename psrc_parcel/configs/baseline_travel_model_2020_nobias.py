# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline_travel_model_2020_biaspf_varpf import BaselineTravelModel2020BiaspfVarpf

class BaselineTravelModel2020Nobias(BaselineTravelModel2020BiaspfVarpf):
    
    
    def __init__(self):
        BaselineTravelModel2020BiaspfVarpf.__init__(self)
        self['travel_model_configuration']['bm_module_class_pair'] = ('inprocess.hana.uncertainty.bm_no_bias', 'BmNoBias')
        self['travel_model_configuration'][2020]['bank'] = [ '2020_nb', ]
