# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, xlwt
from opus_core.logger import logger
from numpy import logical_or, logical_and, array, where, zeros, ndenumerate
from opus_core.resources import Resources
from opus_transcad.models.get_cache_data_into_transcad import GetCacheDataIntoTranscad \
     as ParentClass
from opus_transcad.models.run_transcad_macro import run_transcad_macro, run_get_file_location_macro
from opus_core.variables.variable_name import VariableName

class GetCacheDataIntoTranscad(ParentClass):
    """Write urbansim simulation information into a (file) format 
    that the transcad travel model uses to update its tazdata. """
        
    def create_travel_model_input_file(self,
                                       config,
                                       year,
                                       zone_set,
                                       datasets,
                                       tm_input_file_name="tm_input.txt",
                                       delimiter = '\t',
                                       ):
        """Writes to file tm_input.txt to os.path.join(config["travel_model_data_directory"], config[year]["data_exchange_dir"]).
        """
        tm_config = config['travel_model_configuration']
        if 'travel_model_base_directory' not in tm_config and \
           'generic_directory' in tm_config:
            tm_config['travel_model_base_directory'] = tm_config['generic_directory']
        tm_input_file_name = 'y%stazdata.xls' % year

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
        for variable in variable_mapping:
            variable_list.append(variable[0])
            column_name.append(variable[1])
            
        logger.log_status('variable_list: %s' % variable_list)
        logger.log_status('column_name: %s' % column_name)

        zone_set.compute_variables(variable_list)
        variable_short_name = [VariableName(x).get_alias() for x in variable_list]
        
        tm_input_data_dir = os.path.join(tm_config['travel_model_base_directory'], tm_config[year]['data_exchange_dir'])
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
        self._update_travel_model_data_file(config=tm_config, 
                                            data=data, 
                                            header=header, 
                                            filepath=input_file, 
                                            datatable=datatable, 
                                            joinfield=joinfield, 
                                            delimiter=delimiter,
                                            year=year,
                                            zone_set=zone_set
                                           )

    def _update_travel_model_data_file(self, config, 
                                       data, 
                                       header, 
                                       filepath, 
                                       #datatable, #name of travel model TAZ Data Table
                                       #joinfield, 
                                       #delimiter='\t',
                                      *args, **kwargs):

        self._write_to_xls_file(data, header, filepath)
        scenarioDirectory = config.get('scenario_directory')
        genericDirectory = config.get('generic_directory')
        exchangeDirectory = os.path.split(os.path.split(filepath)[0])[0]
        year=kwargs.get('year')

        macro_args = [["scenarioDirectory", scenarioDirectory],
                      ["genericDirectory", genericDirectory],
                      ["exchangeDirectory", exchangeDirectory],
                      ["year", year]
                  ]

        logger.log_status('macro_args: %s' % macro_args)

        #macroname, ui_db_file = config['macro']['get_cache_data_into_transcad'], config['ui_file']
        ##################run_transcad_macro(macroname, ui_db_file, macro_args)
        
    def _write_to_xls_file(self, data, header, filepath):
        logger.start_block("Writing to transcad input file")
        logger.log_status('data: %s' % data)
        logger.log_status('header: %s' % header)
        logger.log_status('filepath: %s' % filepath)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('data')
        
        [worksheet.write(0, c, cname) for c, cname in enumerate(header)]
        [worksheet.write(int(rc[0])+1, int(rc[1]), v) for rc, v in ndenumerate(data)]
        workbook.save(filepath)
        logger.end_block()

            
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
