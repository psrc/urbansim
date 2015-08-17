# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
import os, re, pickle, tempfile
from opus_emme2.models.run_export_macros import RunExportMacros
from psrc_parcel.emme.models.abstract_emme4_travel_model import AbstractEmme4TravelModel

class RunExportSkims(RunExportMacros, AbstractEmme4TravelModel):
    
    """Export Emme4 skims into an hdf5 file. 
    
    It should run before psrc_parcel.emme.models.get_emme4_data_from_h5_into_cache. 
    The skims should be defined in matrix_variable_map of the travel_model_configuration.
    The skim names are put into a pickle file and passed to a batch file
    defined by 'export_skims_batch_file_name', which is 'skims2h5.bat' by default.
    That script invokes a python script that handles the export.
    """

    def run(self, year):
        """Export Emme4 skims into an hdf5 file. 
        
        Arguments:
        year -- year of the urbansim run. Used to extract the TM year from the bank configuration.
        
        Configuration entries (in travel_model_configuration) used:
        matrix_variable_map -- dictionary of bank names and corresponding skim names.
                Bank names are the path where (back-)slashes are replaced by dots, e.g. skims.auto.am.
                A value for each of such bank name is a dictionary with keys being skim names and 
                values being the desired urbansim attribute name. E.g.
                {'skims.nonmotorized.am':
                      {'abketm': 'am_bike_to_work_travel_time',
                       'awlktm': 'am_walk_time_in_minutes'
                      }
                }
        export_skims_batch_file_name -- batch file name living on the TM path that invokes 
                the python exporting script (default skims2h5.bat).
        matrix_h5_directory -- path to the resulting hdf5 file called xxxx-travelmodel.h5 
                where xxxx is replaced by the TM year (default is the Emme base directory).
        
        """
        tmconfig = self.config['travel_model_configuration']
        bank_year = tmconfig[year]['bank'][0]
        skimnames_config = tmconfig.get('matrix_variable_map', {})
        skimnames = {}
        for spath, sdict in skimnames_config.iteritems():
            skimnames[spath] = sdict.keys()
        skimfile = tempfile.mktemp(suffix='.pickle', prefix='opus_tmp')
        f = open(skimfile, 'w')
        pickle.dump(skimnames, f)
        f.close()
        logger.start_block('Exporting emme4 skims into hdf5')
        try:
            cmd = "%s %s %s %s" % (os.path.join(self.get_emme2_base_dir(), tmconfig.get('export_skims_batch_file_name', 'skims2h5.bat')),
                                os.path.join(self.get_emme2_base_dir(), "src", "results"),
                                os.path.join(tmconfig.get('matrix_h5_directory', self.get_emme2_base_dir()), "%s-travelmodel.h5" % bank_year),
                                skimfile
                                )
            logger.log_status('Invoking: %s' % cmd)     
            if os.system(cmd):
                raise StandardError("Problem with simulation")
        finally:
            logger.end_block()
            os.remove(skimfile)

    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_emme2.models.run_macros_abstract import prepare_for_running_macro
    parser = OptionParser()
    resources, options = prepare_for_running_macro(parser)
    RunExportSkims(resources).run(options.year)    
