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
    at this directory.
    
    scenario_dir_name - is the absolute directory name to the data 
      directory of the travel model scenario
    years_to_run, if specified, indicates what directory to use
      for which year.  It is a dictionary with key=year and value=directory name,
      directory name is relative to scenario_dir_name
    """
    
    travel_model_configuration = {}
    travel_model_configuration['transcad_binary'] = r"C:\Program Files\TransCAD\tcw.exe"
    travel_model_configuration['project_ini'] = r"C:\Program Files\TransCAD\semcog.ini"
    travel_model_configuration['ui_file'] = os.path.join(scenario_dir_name, r'macros\semcog_ui')  
    #the ui file that conatins the macros; it will be used to overwrite section [UI File] in project_ini file
    #config['ui_file'] must be ui_file without extension
    
    ### mapping from urbansim zone variable name to transcad TAZ attribute name 
    urbansim_to_tm_variable_mapping = [
#        ('zone.zone_id', 'ID'),   #normally use zone_id as join field
        ('zone.seq_taz', 'ID'),    #for SEMCOG, use seq_taz
        ('urbansim.zone.population', 'Population'),
        ('urbansim.zone.number_of_households', 'Households'),
        ('urbansim.zone.number_of_jobs', 'Total_Emp'),
        ('zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_basic)', 'Basic'),
        ('zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_nonbasic)', 'NonBasic'),
        ('urbansim.zone.number_of_jobs_of_sector_4', 'WholeSale'),
        ('urbansim.zone.number_of_jobs_of_sector_5', 'Retail')
        ]

    ### mapping from transcad matrice name to urbansim travel_data variable name
    tm_to_urbansim_variable_mapping = [
        ('HWY Core','Trav_Time'),
        ('Transit Core','Fare')
        ]
                                
    travel_model_configuration.update( {
        "urbansim_to_tm_variable_mapping":urbansim_to_tm_variable_mapping,
        "tm_to_urbansim_variable_mapping":tm_to_urbansim_variable_mapping,
        } )
    travel_model_configuration['directory'] = scenario_dir_name
    travel_model_configuration['macro'] = {
        #macros are dictionary indicating macroname and ui_database file (without file extension)
       'get_cache_data_into_transcad': {'SEMCOGImportTabFile': travel_model_configuration['ui_file']},
       'get_transcad_data_into_cache': {'SEMCOGExportMatrices': travel_model_configuration['ui_file']},
       'run_semcog_travel_model':{'SEMCOG Run Loops': travel_model_configuration['ui_file']}
    }
    _add_models(travel_model_configuration, mode)
    _add_years(travel_model_configuration, years_to_run)
    return travel_model_configuration

def _add_models(travel_model_configuration, mode):
    if mode == 'full':
        models = [
            'washtenaw.transcad.get_cache_data_into_transcad',
            'washtenaw.transcad.run_semcog_travel_model',
            'washtenaw.transcad.get_transcad_data_into_cache',
            ]
    travel_model_configuration['models'] = models
        
def _add_years(travel_model_configuration, years_to_run):
    if years_to_run is None:
        years_to_run = {
            2001:'CoreEA05\\urbansim\\2001',
            2002:'CoreEA10\\urbansim\\2002',
            2005:'CoreEA05\\urbansim\\2005',   #path to save interchanging files between urbansim and travel model
            2010:'CoreEA10\\urbansim\\2010',   #path relative to scenario_dir_name
            2015:'CoreEA10\\urbansim\\2015',
            2020:'CoreEA20\\urbansim\\2020',
            2025:'CoreEA20\\urbansim\\2025',
            }
    for year, year_dir in years_to_run.iteritems():
        travel_model_configuration[year] = year_dir
        
