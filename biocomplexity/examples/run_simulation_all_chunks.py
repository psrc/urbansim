# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import gc
import os
import sys
import shutil
import tempfile

from numpy import arange

from opus_core.variables.attribute_type import AttributeType
from opus_core.store.attribute_cache import AttributeCache
from opus_core.coefficients import Coefficients
from opus_core.storage_factory import StorageFactory
from opus_core.opus_package import OpusPackage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger
    
from opus_core.session_configuration import SessionConfiguration
from urbansim.datasets.gridcell_dataset import GridcellDataset

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.models.land_cover_change_model import LandCoverChangeModel
from biocomplexity.equation_specification import EquationSpecification
from biocomplexity.opus_package_info import package
from biocomplexity.constants import Constants
from biocomplexity.examples.lccm_runner_sample import LccmConfiguration
from biocomplexity.tools.lc_convert_to_flt2 import ConvertToFloat
from biocomplexity.tools.lc_convert2 import LCCMInputConvert
from opus_core.chunk_specification import ChunkSpecification


class Simulation(object):
    """ Import data from urbansim cache directory, and compute the following
    computed variables: devt, de, commden, house_den, comm_add and house_add.
    """
    
    package_path = OpusPackage().get_path_for_package("biocomplexity") 
    #lct_attribute = "biocomplexity.land_cover.lct_recoded"
    lct_attribute = "lct"
    possible_lcts = range(1,15)
    
    def _clean_up_land_cover_cache(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
            
    def _get_previous_year(self, current_year, years):
        current_year_index = -1
        for i in range(len(years)):
            if current_year == years[i]:
                current_year_index = i
        if i <= 0 or i >= len(years):
            logger.log_error("invalid year " + str(current_year))
        return years[current_year_index-1]
            
    def _generate_input_land_cover(self, current_year, base_directory, 
                         urbansim_cache_directory, years, output_directory,
                         convert_flt, convert_input):
        if current_year == years[0]:
            if not convert_input:
                return base_directory
            else:
                
                package_dir_path = package().get_package_path()
                command = os.path.join(package_dir_path, "tools", "lc_convert.py")
                status = os.system(command + ' %s -i "%s" -o "%s"' % ('input data',  base_directory, self.temp_land_cover_dir))
                assert(status == 0, "generate input failed")
                return self.temp_land_cover_dir
            
        previous_year = self._get_previous_year(current_year, years)
            
        if not convert_flt: 
            logger.start_block("Copy data from %s to temp land cover folder" % urbansim_cache_directory)
            try:
                self._copy_invariants_to_temp_land_cover_dir(os.path.join(urbansim_cache_directory, str(previous_year)))
            finally:
                logger.end_block()
            return self.temp_land_cover_dir
        
#        package_dir_path = package().get_package_path()
#        command = os.path.join(package_dir_path, "tools", "lc_convert.py")
        flt_directory_in = os.path.join(output_directory, str(previous_year))
        flt_directory_out = self.temp_land_cover_dir
        LCCMInputConvert()._convert_lccm_input(flt_directory_in, flt_directory_out)
#        status = os.system(command + ' %d -i "%s" -o "%s"' % (previous_year, flt_directory_in, flt_directory_out))
#        assert(status == 0, "generate input failed")        
        return self.temp_land_cover_dir
            
    def _get_max_index(self, land_cover_path):
        land_covers = LandCoverDataset(in_storage=StorageFactory().get_storage("flt_storage", storage_location=land_cover_path))
        return land_covers.size()
        
    def _copy_invariants_to_temp_land_cover_dir(self, land_cover_path):
        logger.log_status("temp input land cover data in " + self.temp_land_cover_dir)
        land_covers = LandCoverDataset(in_storage=StorageFactory().get_storage("flt_storage", storage_location=land_cover_path),
                                   out_storage=StorageFactory().get_storage("flt_storage", storage_location=self.temp_land_cover_dir),
                                   out_table_name='land_covers', debuglevel=4)
        logger.log_status("Land cover dataset created.... ") # added dec 4, 2009
        land_covers.flush_dataset() # added dec 4, 2009
        land_covers.write_dataset(attributes=AttributeType.PRIMARY)
        
    def _generate_output_flt(self, current_year, urbansim_cache_directory,
                              output_directory, convert_flt):
        if not convert_flt:
            return
        
        package_dir_path = package().get_package_path()
        command = os.path.join(package_dir_path, "tools", "lc_convert_to_flt.py")        
        flt_directory_in = os.path.join(urbansim_cache_directory, str(current_year))
        flt_directory_out = os.path.join(output_directory, str(current_year))
        status = os.system(sys.executable + ' ' + command + ' %d -i "%s" -o "%s"' % (current_year, flt_directory_in, flt_directory_out))
        assert(status == 0, "generate output failed")
    
    def _generate_output_flt2(self, current_year, urbansim_cache_directory, 
                             output_directory, convert_flt):
        if not convert_flt:
            return
        flt_directory_in = os.path.join(urbansim_cache_directory, str(current_year))
        flt_directory_out = os.path.join(output_directory, str(current_year))

        ConvertToFloat()._create_flt_file(current_year, flt_directory_in, flt_directory_out)

    def run(self, base_directory, urbansim_cache_directory, years, output_directory, temp_folder,
            coefficients_name, specification_name, convert_flt=True, convert_input=False):
        """ run the simulation
                base_directory: directory contains all years folder of lccm.
                urbansim_cache_directory: directory contains all years folder of urbansim cache.
                years: lists of year to run."""
        model = LandCoverChangeModel(self.possible_lcts, submodel_string=self.lct_attribute, 
                                     choice_attribute_name=self.lct_attribute, debuglevel=4)
        coefficients = Coefficients()
        storage = StorageFactory().get_storage('tab_storage', 
            storage_location=os.path.join(self.package_path, 'data'))
        coefficients.load(in_storage=storage, in_table_name=coefficients_name)
        specification = EquationSpecification(in_storage=storage)
        specification.load(in_table_name=specification_name)
        specification.set_variable_prefix("biocomplexity.land_cover.")
        constants = Constants()
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(urbansim_cache_directory)
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['biocomplexity', 'urbansim', 'opus_core'],
                             in_storage=AttributeCache())
                
        ncols = LccmConfiguration.ncols        
        
        if temp_folder is None:
            self.temp_land_cover_dir = tempfile.mkdtemp()
        else:
            self.temp_land_cover_dir = temp_folder
        
        for year in years:
            land_cover_path = self._generate_input_land_cover(year, base_directory, urbansim_cache_directory, 
                                                              years, output_directory, convert_flt, convert_input)
            #max_size = 174338406 (orig) - act. int: 19019944 (37632028 incl NoData)
            max_size = self._get_max_index(land_cover_path) # 1st instance of lc_dataset - but looks like a 'lite' version
            offset = min(LccmConfiguration.offset, max_size)
            s = 0
            t = offset
            while (s < t and t <= max_size):
                logger.log_status("Offset: ", s, t)
                index = arange(s,t)
                
                land_cover_cache_path=os.path.join(urbansim_cache_directory,str(year),'land_covers')
                self._clean_up_land_cover_cache(land_cover_cache_path)
                
                simulation_state.set_current_time(year)
                
                # 2nd instance of lc_dataset
                land_covers = LandCoverDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path),
                                           out_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path),
                                           debuglevel=4)
                land_covers.subset_by_index(index)
#                land_covers.load_dataset()
                gridcells = GridcellDataset(in_storage=attribute_cache, debuglevel=4)

                agents_index = None
                model.run(specification, coefficients, land_covers, data_objects={"gridcell":gridcells,
                              "constants":constants, "flush_variables":True},
                              chunk_specification = {'nchunks':5}) ## chunk size set here
                land_covers.flush_dataset()
                del gridcells
                del land_covers

#                self._generate_output_flt(year, urbansim_cache_directory, output_directory, convert_flt)
                self._generate_output_flt2(year, urbansim_cache_directory, output_directory, convert_flt)
                
                if t >= max_size: break
                s = max(t-10*ncols,s)
                t = min(t+offset-10*ncols,max_size)
                
        # clean up temp storage after done simulation
        shutil.rmtree(self.temp_land_cover_dir)
    
if __name__ == "__main__":    
    base_dir = r"O:\unix\projects\urbansim9\land_cover_change_model\LCCM_4County_converted/1995"
    urbansim_cache  = r"D:\urbansim_cache\2006_02_10__13_06"
    Simulation().run(base_dir, urbansim_cache, [2005])
    
