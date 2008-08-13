#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

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
    
    config['years'] = range(2000,2001)    
    IndicatorFactory().create_indicators(config, get_multiple_year_indicators(config))