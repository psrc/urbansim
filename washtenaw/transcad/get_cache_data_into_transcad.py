# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from opus_core.logger import logger
from numpy import logical_or, logical_and, array, where, zeros
from opus_core.variables.variable_name import VariableName
from opus_core.resources import Resources
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
from opus_core.session_configuration import SessionConfiguration
from run_transcad_macro import run_transcad_macro, run_get_file_location_macro
from opus_core.store.attribute_cache import AttributeCache
from washtenaw.transcad.set_project_ini_file import set_project_ini_file, get_project_year_dir

class GetCacheDataIntoTranscad(GetCacheDataIntoTravelModel):
    """Write urbansim simulation information into a (file) format 
    that the transcad travel model uses to update its tazdata. """
        
    def create_travel_model_input_file(self,
                                       config,
                                       year,
                                       zone_set,
                                       datasets,
                                       tm_input_file_name="tm_input.txt",
                                       delimiter = '\t'):
        """Writes to file tm_input.txt in [travel_model_data_directory]/urbansim/[year].
        """

        tm_config = config['travel_model_configuration']
        project_year_dir = get_project_year_dir(tm_config, year)
        urbansim_to_tm = tm_config['urbansim_to_tm_variable_mapping']
        if 'DataTable' in urbansim_to_tm:
            datatable = urbansim_to_tm['DataTable']
        else:
            datatable = "TAZ Data Table"
        if 'JoinField' in urbansim_to_tm:
            joinfield = urbansim_to_tm['JoinField']
        else:
            joinfield = 'ID'
        
        variable_mapping = urbansim_to_tm['variable_mapping']
        
        variable_list = []
        column_name = []
        for variable_pair in variable_mapping:
            urbansim_var, transcad_var = variable_pair
            variable_list.append(urbansim_var)
            column_name.append(transcad_var)

        zone_set.compute_variables(variable_list)
        variable_short_name = [VariableName(x).get_alias() for x in variable_list]
        
        tm_input_data_dir = os.path.join(tm_config['directory'], tm_config[year])
        if not os.path.exists(tm_input_data_dir):
            os.makedirs(tm_input_data_dir)

        input_file = os.path.join(tm_input_data_dir, tm_input_file_name)

        logger.log_status('write travel model input file to directory: %s' % tm_input_data_dir)
        rows = zone_set.size()
        cols = len(variable_short_name)
        data = zeros(shape=(rows,cols))
        for i in range(cols):
            this_column=zone_set.get_attribute(variable_short_name[i])
            data[:,i] = this_column
            
        header = column_name
        self._update_travel_model_data_file(tm_config, data, header, input_file, datatable, joinfield, delimiter)
        
    def prepare_for_run(self, config, year):
        set_project_ini_file(config, year)
        
    def _update_travel_model_data_file(self, tm_config, data, header, input_file, datatable, joinfield, delimiter):
        self._delete_dcc_file( os.path.splitext(input_file)[0] + '.dcc' )
        self._write_to_txt_file(data, header, input_file, delimiter)

        transcad_file_location = run_get_file_location_macro(tm_config)
        datatable = transcad_file_location[datatable] #replace internal matrix name with absolute file name

        macro_args = [["InputFile", input_file],
                      ["DataTable", datatable],
                      ["JoinField", joinfield]
                  ]
        
        #for macroname in tm_config['macro']['get_cache_data_into_transcad'].keys():
            #ui_db_file = tm_config['macro']['get_cache_data_into_transcad'][macroname]
            #ui_db_file = os.path.join(tm_config['directory'], ui_db_file)
        macroname, ui_db_file = tm_config['macro']['get_cache_data_into_transcad']
        run_transcad_macro(macroname, ui_db_file, macro_args)
        
    def _write_to_txt_file(self, data, header, input_file, delimiter='\t'):
        logger.start_block("Writing to transcad input file")
        newfile = open(input_file, 'w')
        newfile.write(delimiter.join(header) + "\n")
        rows, cols = data.shape
        for n in range(rows):
            newfile.write(delimiter.join([str(x) for x in data[n,]]) + "\n")
                                          
        newfile.close()
        logger.end_block()

    def _delete_dcc_file(self, dcc_file):
        if os.path.exists(dcc_file):
            os.remove(dcc_file)
            
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
#    options.resources_file_name = "c:\urbansim_cache\semcog_test_tm.pickle"
#    options.year = 2001
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetCacheDataIntoTranscad().run(resources, options.year)
