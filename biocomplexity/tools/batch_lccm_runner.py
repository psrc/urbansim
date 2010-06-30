#
# Opus software. Copyright (C) 2005-2009 University of Washington
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

from biocomplexity.opus_package_info import package
from biocomplexity.examples.run_simulation_all_chunks import Simulation
from biocomplexity.tools.lc_convert_to_flt2 import ConvertToFloat
from biocomplexity.tools.lc_convert2 import LCCMInputConvert
from opus_core.logger import logger

from optparse import OptionParser
from time import time

import os
import shutil
import sys
import gc

#::directories::
#base_dir = C:\eclipse\opus\src\biocomplexity\data\LCCM_4County
#base_dir_convert = C:\eclipse\opus\src\biocomplexity\data\LCCM_4County_converted
#output_dir
#usc_dir = C:\eclipse\opus\src\urbansim_cache\data\2009_10_15__13_44

class LCCMBatch(object):
    base_dir = r"C:\eclipse\opus\src\biocomplexity\data\LCCM_4County"
    base_dir_convert = r"C:\eclipse\opus\src\biocomplexity\data\LCCM_4County_converted"
    usc_dir = r"C:\eclipse\opus\src\urbansim_cache\data\2009_10_15__13_44"
#    output_dir = r"C:\mmarsik\lccm\data\output\a9902c_v4"
#    output_dir = r"C:\mmarsik\lccm\data\output\a9902c_nosmall_v3"
    output_dir = r"C:\mmarsik\lccm\data\output\a9599c_noCAOs"
    
    def _get_prediction_year(self, current_year, years):
        current_year_index = -1
        for i in range(len(years)):
            if current_year == years[i]:
                prediction_year_index = i+1
        if i <= 0 or i >= len(years):
            logger.log_error("invalid year " + str(current_year))
        return years[prediction_year_index]
        
    def _move_LCCM_base_directory(self,flt_directory_in,flt_directory_out):
        names = os.listdir(flt_directory_in)
        logger.log_status("\r\n1. moving base data\r\n")
        for name in names:
            if name != "lct.lf4":
                shutil.move(os.path.join(flt_directory_in,name),flt_directory_out)
                logger.log_status("\t%s successfully moved" % (name))

    def _copy_output(self,flt_directory_in,flt_directory_out):
        if os.path.exists(flt_directory_in):
            names = os.listdir(flt_directory_in)
            logger.log_status("\r\n2. copying output data\r\n")
            for name in names:
                if name == "lct.lf4":
                    shutil.copy(os.path.join(flt_directory_in,name),flt_directory_out)
                    logger.log_status("\t%s successfully copied\r\n" % (name))
        
    def _move_LCCM_converted_directory(self,flt_directory_in,flt_directory_out):
        names = os.listdir(flt_directory_in)
        logger.log_status("\r\n4. moving converted data\r\n")
        for name in names:
            if name != "lct.lf4":
                shutil.move(os.path.join(flt_directory_in,name),flt_directory_out)
                logger.log_status("\t%s successfully moved" % (name))
    def _delete_land_covers_from_ucs(self,usc_dir):
        logger.log_status("\r\n5. deleting land covers under\r\n%s\r\n" % usc_dir)
        if os.path.exists(os.path.join(usc_dir,"land_covers")):
            shutil.rmtree(os.path.join(usc_dir,"land_covers"))
        if os.path.exists(os.path.join(usc_dir,"land_covers.computed")):
            shutil.rmtree(os.path.join(usc_dir,"land_covers.computed"))

if __name__ == "__main__":    
#    years = [2002, 2005, 2008, 2011, 2014, 2017, 2020, 2023, 2026, 2029, 2032, 2035, 2038, 2041, 2044, 2047, 2050]
    years = [2002, 2005, 2008]
    for year in years:
        if year != years[0] and year != years[-1]:
            current_year = str(year)
            previous_year = str(Simulation()._get_previous_year(year, years))
            prediction_year = [LCCMBatch()._get_prediction_year(year, years)]
            print previous_year, current_year, prediction_year
            # 1. move LCCM_base_directory from previous year to current year
            LCCMBatch()._move_LCCM_base_directory(os.path.join(LCCMBatch.base_dir, previous_year, "land_covers"),
                                     os.path.join(LCCMBatch.base_dir, current_year, "land_covers"))
            # 2. copy output from previous predictions as input for next prediction
            LCCMBatch()._copy_output(os.path.join(LCCMBatch.output_dir, current_year, "land_covers"),
                                     os.path.join(LCCMBatch.base_dir, current_year, "land_covers"))
            # 3. convert input
            LCCMInputConvert()._convert_lccm_input(os.path.join(LCCMBatch.base_dir, current_year),
                                                   os.path.join(LCCMBatch.base_dir_convert, current_year))
            # 4. move LCCM_converted_directory from previous year to current year
            LCCMBatch()._move_LCCM_converted_directory(os.path.join(LCCMBatch.base_dir_convert, previous_year, "land_covers"),
                                     os.path.join(LCCMBatch.base_dir_convert, current_year, "land_covers"))

            # 5. delete land_covers and land_cover.computed from urbansimcache from previous years predictions
            LCCMBatch()._delete_land_covers_from_ucs(os.path.join(LCCMBatch.usc_dir, current_year))
            LCCMBatch()._delete_land_covers_from_ucs(os.path.join(LCCMBatch.usc_dir, previous_year))
            
            # 6. run single year of lccm
            # choose set of specification and coefficients:
#            specification = "lccm_specification_all99to02v2c"
#            coefficients = "lccm_coefficients_all99to02v2c"
#            specification = "lccm_specification_all99to02v5_from_minspecc"
#            coefficients = "lccm_coefficients_all99to02v5_from_minspecc"

#            specification = "lccm_specification_all99to02v4_use4predictionsc"
#            coefficients = "lccm_coefficients_all99to02v4_use4predictionsc"
#            coefficients = "lccm_coefficients_all99to02_nosmall_v3_from_allspecc"
#            specification = "lccm_specification_all99to02_nosmall_v3_from_allspecc"
            coefficients = "lccm_coefficients_all95to99_noCAOsc"
            specification = "lccm_specification_all95to99_noCAOsc"

#            specification = "lccm_specification_all99to02v6_from_allspecc"
#            coefficients = "lccm_coefficients_all99to02v6_from_allspecc"
#            specification = "land_cover_change_model_specification_small_test"
#            coefficients = "land_cover_change_model_coefficients_small_test"
#            specification = "land_cover_change_model_specification_a91_95corrected"
#            coefficients = "land_cover_change_model_coefficients_a91_95corrected"
#            specification = "land_cover_change_model_specification_a95_99corrected"
#            coefficients = "land_cover_change_model_coefficients_a95_99corrected"

            # Temporary swap folder, if not provided, a system temp directory will be used
            temp_folder = None
            logger.log_status("6. Running LCCM predictions\r\n")
            t1 = time()
            Simulation().run(os.path.join(LCCMBatch.base_dir_convert, current_year), 
                             LCCMBatch.usc_dir, 
                             prediction_year, 
                             LCCMBatch.output_dir, 
                             temp_folder,
                             coefficients, specification,
                             convert_flt=True, convert_input=False)
            logger.log_status("Model prediction done. " + str(time()-t1) + " s")
