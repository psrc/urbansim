# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
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
    #this specifies data from urbansim to transcad
    #DataTable is the name for table to be updated, defined in SEMCOG_MOD.bin, and will be replaced by its value;
    #   refer to run_get_file_location_macro in run_transcad_macro.py; it is case sensitive.
    #JoinField specifies which field to use to join urbansim output with data table
    #varialbe_mapping specifies the mapping from urbansim variables to transcad column in in DataTable
    #in format of (full qualified urbansim variable name, transcad column name)
    #urbansim variable name is the full qualified urbansim variable name, most likely for taz
    #transcad column name is the column name in transcad data table, which are updated

    urbansim_to_tm_variable_mapping = {
        "DataTable":"TAZ Data Table",
        "JoinField":"ID",
        "variable_mapping":[
        ('zone.zone_id', 'ID'),
#        ('zone.seq_taz', 'ID'),   #JoinField
        ('urbansim.zone.population', 'Population'),
        ('urbansim.zone.number_of_households', 'Households'),
        ('urbansim.zone.number_of_jobs', 'Total_Emp'),
        ('zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_basic)', 'Basic'),
        #('zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_nonbasic)', 'NonBasic'),
        ('urbansim.zone.number_of_jobs_of_sector_4', 'WholeSale'),
        ('urbansim.zone.number_of_jobs_of_sector_5', 'Retail')
        ]
    }
    ### mapping from transcad matrice name to urbansim travel_data variable name
    #this specifies data from transcad to urbansim
    #format: [matrix name, row_index name, column_index name, [(transcad variable name, urbansim variable name)]]
    #matrix name is a name defined in SEMCOG_MOD.bin, and will be replaced by its value;
    #   refer to run_get_file_location_macro in run_transcad_macro.py; it is case sensitive.
    #transcad variable name is the column name in the matrix specified
    #urbansim variable name is the name to use in the exported travel data
    tm_to_urbansim_variable_mapping = [
         ["AMHwySkims","ZoneID", "ZoneID",
            [("Miles", "highway_distance"),
             ("Trav_Time","highway_travel_time"),
             ]
         ],
         ["AMTransitSkim","ZoneID", "ZoneID",
             [("Generalized Cost", "generalized_cost"),
              ("Fare","am_transit_fare"),
              ]
        ],
    ]                  
    travel_model_configuration.update( {
        "urbansim_to_tm_variable_mapping":urbansim_to_tm_variable_mapping,
        "tm_to_urbansim_variable_mapping":tm_to_urbansim_variable_mapping,
        } )
    
    travel_model_configuration['directory'] = scenario_dir_name
    travel_model_configuration['macro'] = {
        #macros are dictionaries indicating macroname and ui_database file (without file extension)
       'get_cache_data_into_transcad': ('SEMCOGImportTabFile', travel_model_configuration['ui_file']),
       'get_transcad_data_into_cache': ('SEMCOGExportMatrices', travel_model_configuration['ui_file']),
       'run_semcog_travel_model':('SEMCOG Run Loops', travel_model_configuration['ui_file']),
       'get_file_location':('SEMCOGGetFileLocation', travel_model_configuration['ui_file'])
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
    if mode == 'skims':
        models = [
            'washtenaw.transcad.get_cache_data_into_transcad',
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
        
