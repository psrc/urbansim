# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, xlwt
from opus_core.logger import logger
from numpy import ndenumerate
from opus_core.resources import Resources
from opus_transcad.models.get_cache_data_into_transcad import GetCacheDataIntoTranscad \
     as ParentClass
from opus_transcad.models.run_transcad_macro import run_transcad_macro, run_get_file_location_macro

class GetCacheDataIntoTranscad(ParentClass):
    """Write urbansim simulation information into a (file) format 
    that the transcad travel model uses to update its tazdata. """
        
    def create_travel_model_input_file(self,
                                       tm_input_file_name="",
                                       *args,
                                       **kwargs
                                       ):
        """Writes to file tm_input.txt to os.path.join(config["travel_model_data_directory"], config[year]["data_exchange_dir"]).
        """
        tm_config = kwargs.get('config')['travel_model_configuration']
        if not tm_config.has_key('travel_model_base_directory') and \
           tm_config.has_key('scenario_directory'):
            tm_config['travel_model_base_directory'] = tm_config['scenario_directory']
        if not tm_input_file_name:
            year=kwargs.get('year')
            tm_input_file_name = 'y%stazdata.xls' % year

        ParentClass.create_travel_model_input_file(self, 
                                                 tm_input_file_name=tm_input_file_name,
                                                 *args,
                                                 **kwargs
                                                )

    def _update_travel_model_data_file(self, config, 
                                       data, 
                                       header, 
                                       filepath, 
                                       #datatable, #name of travel model TAZ Data Table
                                       #joinfield, 
                                       #delimiter='\t',
                                      *args, **kwargs):

        #self._write_to_xls_file(data, header, filepath)
        scenarioDirectory = config.get('scenario_directory')
        genericDirectory = config.get('generic_directory')
        exchangeDirectory = os.path.split(os.path.split(filepath)[0])[0]
        year=kwargs.get('year')

        macro_args = [["scenarioDirectory", scenarioDirectory],
                      ["genericDirectory", genericDirectory],
                      ["exchangeDirectory", exchangeDirectory],
                      ["year", year]
                  ]
        
        macroname, ui_db_file = config['macro']['get_cache_data_into_transcad'], config['ui_file']
        run_transcad_macro(macroname, ui_db_file, macro_args)
        
    def _write_to_xls_file(self, data, header, filepath):
        logger.start_block("Writing to transcad input file")
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('data')
        
        [worksheet.write(0, c, cname) for c, cname in enumerate(header)]
        [worksheet.write(rc[0]+1, rc[1], v) for rc, v in ndenumerate(data)]
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
