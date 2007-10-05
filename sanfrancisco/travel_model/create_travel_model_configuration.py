#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
import os

def create_travel_model_configuration(scenario_dir_name,
                                      mode='full',
                                      years_to_run=None):
    """Returns a travel model configuration for a travel model located
    at the same directory as this script.
    
    scenario_dir_name - is the absolute directory name to the data 
      directory of the travel model scenario
    years_to_run, if specified, indicates what directory to use
      for which year.  It is a dictionary with key=year and value=directory name,
      directory name is relative to scenario_dir_name
    """
    
    travel_model_configuration = {}
    travel_model_configuration['travel_model_command'] = os.path.join(scenario_dir_name, "tm.cmd")
    
    ### mapping from urbansim zone variable name to travel model TAZ attribute name 
    urbansim_to_tm_variable_mapping = [
#        ('zone.zone_id', 'SFTAZ'),   #normally use zone_id as join field
#        ('zone.seq_taz', 'ID'),    #alternatively id field
        ('sanfrancisco.zone.number_of_households', 'HHLDS'),
        ('sanfrancisco.zone.population', 'POP'),
        ('sanfrancisco.zone.employment', 'EMPLOYMENT'),
#        ('?', 'EMPLOYEDRESIDENTS'),        
        ('sanfrancisco.zone.employment_of_sector_cie', 'EMP-CIE'),
        ('sanfrancisco.zone.employment_of_sector_med', 'EMP-MED'),
        ('sanfrancisco.zone.employment_of_sector_mips', 'EMP-MIPS'),
        ('sanfrancisco.zone.employment_of_sector_pdr', 'EMP-PDR'),
        ('sanfrancisco.zone.employment_of_sector_visitor', 'EMP-VISITOR'),
        ]

    ### file containing the output of travel_data table from travel model, including header in csv format
    ###
    tm_to_urbansim_variable_file = r"tm_output.txt"  # relative to os.path.join(scenario_dir_name, year_dir)
                                
    travel_model_configuration.update( {
        "urbansim_to_tm_variable_mapping":urbansim_to_tm_variable_mapping,
        "tm_to_urbansim_variable_file":tm_to_urbansim_variable_file,
        } )
    travel_model_configuration['directory'] = scenario_dir_name

    _add_models(travel_model_configuration, mode)
    _add_years(travel_model_configuration, years_to_run)
    return travel_model_configuration

def _add_models(travel_model_configuration, mode):
    if mode == 'full':
        models = [
            'sanfrancisco.travel_model.get_cache_data_into_travel_model',
            'sanfrancisco.travel_model.run_sanfrancisco_travel_model',
            'sanfrancisco.travel_model.get_travel_model_data_into_cache',
            ]
    travel_model_configuration['models'] = models
        
def _add_years(travel_model_configuration, years_to_run):
    if years_to_run is None:
        years_to_run = {
            2001:r'2001/urbansim',
            2002:r'2002/urbansim',
            2005:r'2005/urbansim',   #path to save interchanging files between urbansim and travel model
            2010:r'2010/urbansim',   #path relative to scenario_dir_name
            2015:r'2015/urbansim',
            2020:r'2020/urbansim',
            2025:r'2025/urbansim',
            }
    for year, year_dir in years_to_run.iteritems():
        travel_model_configuration[year] = year_dir
        
