# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

def get_multiple_year_indicators(config):
    indicators = [
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'Residential_Units = alldata.aggregate_all(urbansim.gridcell.residential_units,function=sum)'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'Commercial_SQFT = alldata.aggregate_all(urbansim.gridcell.commercial_sqft,function=sum)'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'Industrial_SQFT = alldata.aggregate_all(urbansim.gridcell.industrial_sqft,function=sum)'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':'Developed_Cells = alldata.aggregate_all(urbansim.gridcell.is_developed,function=sum)'
              }, 
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'residential_vacancy_rate',
                           'operation':'divide',
                           'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_residential_units,function=sum)',
                                        'alldata.aggregate_all(urbansim.gridcell.residential_units,function=sum)']
                           }
              },             
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'commercial_vacancy_rate',
                           'operation':'divide',
                           'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_commercial_sqft,function=sum)',
                                        'alldata.aggregate_all(urbansim.gridcell.commercial_sqft,function=sum)']
                           }
              },             
             {'dataset':'alldata',
              'image_type':'table',
              'attribute':{'indicator_name':'industrial_vacancy_rate',
                           'operation':'divide',
                           'arguments':['alldata.aggregate_all(urbansim.gridcell.vacant_industrial_sqft,function=sum)',
                                        'alldata.aggregate_all(urbansim.gridcell.industrial_sqft,function=sum)']
                           }
              },             
             #{'dataset':'alldata',
              #'image_type':'table',
              #'attribute':'psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk'
              #}, 
             #{'dataset':'alldata',
              #'image_type':'table',
              #'attribute':'psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk'
              #}, 
             #{'dataset':'zone',
              #'image_type':'table',
              #'attribute':'psrc.county.number_of_jobs'
              #},  
        ]
    return indicators

if __name__ == '__main__': 
    import os
    from indicator_config import config
    from urbansim.indicators.indicator_factory import IndicatorFactory
    
    config['years'] = list(range(2000,2001))    
    IndicatorFactory().create_indicators(config, get_multiple_year_indicators(config))