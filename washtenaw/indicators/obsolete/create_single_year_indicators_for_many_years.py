# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

def get_single_year_indicators(config):
    indicators = [
            {'dataset':'gridcell',
             'image_type':'map',
             'attribute':{'indicator_name':'urbansim.gridcell.population', 
             'scale':[0, 800]}
             },  
        ]

    return indicators

if __name__ == '__main__': 
    import os
    from indicator_config import config
    from urbansim.indicators.indicator_factory import IndicatorFactory
    
    years = [2000, 2030]            
    for year in years:
        config['year'] = year
        IndicatorFactory().create_indicators(config, get_single_year_indicators(config))