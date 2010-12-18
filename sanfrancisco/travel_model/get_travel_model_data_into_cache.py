# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2010 University of Washington and the SFCTA
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import array, where, zeros, logical_and, logical_or
import os, csv, shutil, subprocess
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from champUtil import SkimUtil, TRIPMODE

from opus_core.misc import get_config_from_opus_path

class GetTravelModelDataIntoCache(GetTravelModelDataIntoCache):
    """
    A class to access the output of travel models.
    """
    TABLE_NAME = "travel_data"
    RECYCLE_BIN = r"Recycle Bin"

    def get_travel_data_from_travel_model(self, config, 
                                          year, zone_set ):
        """
        Returns a new travel data set populated by a travel model
        """
        logger.log_status("Running GetTravelModelDataIntoCache with year %d" % (year))
        logger.log_status(zone_set)
        tm_config = config['travel_model_configuration']
        
        base_dir    = tm_config['travel_model_base_directory']    
        run_dir     = os.path.join(base_dir, tm_config[year]['year_dir'])
        in_storage  = StorageFactory().get_storage('dict_storage')
        max_zone_id = zone_set.get_id_attribute().max()
        in_storage.write_table(
                table_name=self.TABLE_NAME,
                table_data=self._read_skims(run_dir, max_zone_id)
            )
                
        travel_data_set = TravelDataDataset(in_storage=in_storage, in_table_name=self.TABLE_NAME)
         
        # zip up model_dir
        cmd = r'"C:\Program Files\7-Zip\7z.exe"' 
        cmd = cmd + ' a %s.7z %s' % (tm_config[year]['year_dir'], tm_config[year]['year_dir'])
        logger.start_block("Running [%s]" % (cmd))
        zipproc = subprocess.Popen( cmd, cwd = base_dir, stdout=subprocess.PIPE ) 
        for line in zipproc.stdout:
            logger.log_status(line.strip('\r\n'))
        zipret  = zipproc.wait()
        logger.log_status("Returned %d" % (zipret))
        if zipret != 0: print "Zip (%s) exited with bad return code" % (cmd)
        logger.end_block()
        
        # delete everything except for the triptables subdir
        try:
            delete_list = os.listdir(run_dir)
            for del_file in delete_list:
                if del_file == "triptables": continue
                
                del_file_path = os.path.join(run_dir, del_file)
                if os.path.isfile(del_file_path): os.remove(del_file_path)
                elif os.path.isdir(del_file_path): shutil.rmtree(del_file_path)
            
            
            # recycle bin remove
            (drive, tail) = os.path.splitdrive(run_dir)
            recycle_dir =  os.path.join(drive + r"\\", RECYCLE_BIN, tail.lstrip(r"\\"))
            shutil.rmtree(recycle_dir)
        except Exception, err:
            logger.log_error("Error: %s" % str(err))


        return travel_data_set

    def _read_skims(self, run_dir, maxTAZ, MISSING_VALUE=9999):
        """ Read the travel times for O/D pairs from the AM skim tables into a dictionary;
            Columns are origin taz, dest taz, distance (? roadway ?), travel times for
              auto (DA), WLW, WMW, WBW, WPW (what about the others?)
              
            Assuming zero values are invalid; substituting in missing values
        """
        logger.start_block("Opening and reading skims for travel times")
        return_data = \
            { "from_zone_id":[],  "to_zone_id":[],  "dist":[], \
              "hwy":[],           "bus":[],         "lrt":[], \
              "bart":[],          "exp":[] \
            }
        
        skims   = SkimUtil(run_dir, useTempTrn = True, timeperiods=[2], trnskims=["WLW", "WMW", "WBW", "WPW"], skimprefix="final")
        maxTAZ  = min(skims.getMaxTAZnum(), maxTAZ)
        modes   = dict((v,k) for k,v in TRIPMODE.iteritems())
        logger.log_status("Opened and read Skims")

        for otaz in range(1, maxTAZ+1):
            for dtaz in range(1, maxTAZ+1):
                return_data["from_zone_id"].append(otaz)
                return_data["to_zone_id"].append(dtaz)
                
                if otaz == dtaz: 
                    nonmott = skims.getTripTravelTime(tripmode=modes["Walk"], segdir=1,
                                                      otaz=otaz, dtaz=dtaz,
                                                      timeperiod=2)
                
                # auto 
                d = skims.getTripTravelDist(tripmode=modes["DA"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if d > 0:           return_data["dist"].append(d)
                else:               return_data["dist"].append(MISSING_VALUE)
                
                t = skims.getTripTravelTime(tripmode=modes["DA"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if t > 0:           return_data["hwy"].append(t)
                else:               return_data["hwy"].append(MISSING_VALUE)
                
                # WLW
                t = skims.getTripTravelTime(tripmode=modes["WalkToLocal"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if t > 0:           return_data["bus"].append(t)
                elif otaz==dtaz:    return_data["bus"].append(nonmott)
                else:               return_data["bus"].append(MISSING_VALUE)
                
                # WMW
                t = skims.getTripTravelTime(tripmode=modes["WalkToMUNI"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if t > 0:           return_data["lrt"].append(t)
                elif otaz==dtaz:    return_data["lrt"].append(nonmott)
                else:               return_data["lrt"].append(MISSING_VALUE)

                # WBW
                t = skims.getTripTravelTime(tripmode=modes["WalkToBART"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if t > 0:           return_data["bart"].append(t)
                elif otaz==dtaz:    return_data["bart"].append(nonmott)
                else:               return_data["bart"].append(MISSING_VALUE)
                
                # WPW
                t = skims.getTripTravelTime(tripmode=modes["WalkToPremium"], segdir=1,
                                            otaz=otaz, dtaz=dtaz, timeperiod=2)
                if t > 0:           return_data["exp"].append(t)
                elif otaz==dtaz:    return_data["exp"].append(nonmott)
                else:               return_data["exp"].append(MISSING_VALUE)
                
            if otaz % 100 == 0: logger.log_status("Completed all destinations for otaz up to %d" % (otaz))

        # convert to numpy array        
        for item, value in return_data.iteritems():
            try:
                return_data[item] = array(value)
            except:
                ##TODO: add handling for string array
                pass
        
        
        del skims
        modes.clear()
        
        logger.end_block()
        return return_data

    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources", default=None)
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    #these options were added by SFCTA
    parser.add_option("-c", "--alt-config", dest="alt_config", action="store", type="string",
                      help="opus path to config if pickled resources not available", default=None)
    parser.add_option("-d", "--alt-cache-dir", dest="alt_cache_dir", action="store", type="string",
                      help="cache directory if pickled resources not available", default=None)
    (options, args) = parser.parse_args()
    
    #options here added by SFCTA
    if (options.alt_config is not None) and (options.alt_cache_dir is not None):
        resources=get_config_from_opus_path(options.alt_config)
        resources['cache_directory']=options.alt_cache_dir
    elif options.resources_file_name is not None:
        r = get_resources_from_file(options.resources_file_name)
        resources = Resources(get_resources_from_file(options.resources_file_name))
    else:
        parser.print_help()
        sys.exit(1)

    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    GetTravelModelDataIntoCache().run(resources, options.year)
