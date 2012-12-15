# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import win32com.client as w32c
from opus_core.logger import logger

def run_get_file_location_macro(config):
    """ run the macro define in configuration for get_file_location, which should return a list of tuples of
    file location define in model.bin (in the case of SEMCOG, SEMCOG_MOD.bin), and convert the tuples into dict
    """
    
    macroname, dbname = config['macro']['get_file_location'], config['ui_file']
    args = None
    return dict(run_transcad_macro(macroname, dbname, args))

def run_transcad_macro(macroname, dbname, args=None):
    tc = w32c.Dispatch("TransCAD.AutomationServer")
    try:
        return_val = tc.Macro(macroname, dbname, args)
        logger.log_status('return_val: %s' % (return_val))
        if return_val is not None:
            try:logger.log_error( return_val[-1][-1] )  #if the return is an error msg
            except:
                return return_val  #else pass the return_val to the caller
    finally:
        del tc

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", "--macroname", dest="macroname", action="store", type="string",
                         help="Name of macro")
    parser.add_option("-u", "--dbname", dest="dbname", action="store", type="string",
                      help="ui database file name")
    parser.add_option("-a", "--args", dest="args", action="store", type="int",
                      help="argument values")

    (options, args) = parser.parse_args()
    run_transcad_macro(options.macroname, options.dbname, options.args)
