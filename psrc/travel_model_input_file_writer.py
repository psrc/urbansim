#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
import string
import sys
import time
import urbansim
from opus_core.logger import logger
from numpy import logical_or, logical_and, array, where, zeros, median

class TravelModelInputFileWriter(object):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. """

    def _init_tazdata(self, max_zone_id):
        array_demension = max_zone_id + 1
        self.retail_by_taz  = zeros((array_demension,))
        self.fires_by_taz   = zeros((array_demension,))
        self.gov_by_taz   = zeros((array_demension,))
        self.educ_by_taz  = zeros((array_demension,))
        self.wtcu_by_taz  = zeros((array_demension,))
        self.manu_by_taz  = zeros((array_demension,))
        self.univ_by_taz  = zeros((array_demension,))
        self.low_income_hh_by_taz  = zeros((array_demension,))
        self.low_mid_income_hh_by_taz = zeros((array_demension,))
        self.upper_mid_income_hh_by_taz = zeros((array_demension,))
        self.upper_income_hh_by_taz  = zeros((array_demension,))

    def create_tripgen_travel_model_input_file(self, job_set, household_set, taz_col_set, max_zone_id,
                                               current_emme2_tripgen_dir, current_year):
        """Writes to the an emme2 input file in the tripgen/inputtg/TAZDATA.MA2.
           If the datasets need to select by year.
               The attributes needed are:
                   job_set: job_id, zone_id, sector_id
                   household_set: household_id, zone_id, income
        """
        logger.log_status("max_zone_id = ", max_zone_id)
        self._init_tazdata(max_zone_id)

        # setup for calculating quartile information
        hh_income = household_set.get_attribute("income")
        median_income = median(hh_income)
        lower_median = median(hh_income[where(hh_income<median_income)])
        upper_median = median(hh_income[where(hh_income>median_income)])
        hh_zones = household_set.get_attribute('zone_id')

        # setup for calculating other data
        zones = array(range(1, max_zone_id+1))
        job_zones = job_set.get_attribute('zone_id')
        job_sector_ids = job_set.get_attribute("sector_id")

        logger.log_status("calculating entries for emme2 input file")
        for zone in zones:
            job_zone_sector_id = job_sector_ids[where(job_zones == zone)]
            hh_in_this_zone = where(hh_zones == zone)

            self.manu_by_taz[zone] = logical_and(job_zone_sector_id>=3, job_zone_sector_id < 5).sum()
            self.wtcu_by_taz[zone] = logical_and(job_zone_sector_id>=5, job_zone_sector_id < 8).sum()
            self.retail_by_taz[zone] = logical_and(job_zone_sector_id>=8, job_zone_sector_id < 10).sum()
            self.fires_by_taz[zone] = logical_and(job_zone_sector_id>=10, job_zone_sector_id < 14).sum()
            self.gov_by_taz[zone] = logical_or(job_zone_sector_id==14, job_zone_sector_id ==15).sum() + \
                               logical_or(job_zone_sector_id==17, job_zone_sector_id ==18).sum()
            self.educ_by_taz[zone] = (job_zone_sector_id == 16).sum()

            # calculate quartiles
            self.low_income_hh_by_taz[zone] = (hh_income[hh_in_this_zone] < lower_median).sum()
            self.low_mid_income_hh_by_taz[zone] = (logical_and(hh_income[hh_in_this_zone] >= lower_median,
                                                               hh_income[hh_in_this_zone] < median_income)).sum()
            self.upper_mid_income_hh_by_taz[zone] = (logical_and(hh_income[hh_in_this_zone] >= median_income,
                                                          hh_income[hh_in_this_zone] < upper_median)).sum()
            self.upper_income_hh_by_taz[zone] = (hh_income[hh_in_this_zone] >= upper_median).sum()

        return self._write_to_file(taz_col_set, current_emme2_tripgen_dir, current_year, max_zone_id)

    def _write_to_file(self, taz_col_set, current_emme2_tripgen_dir, current_year, max_zone_id):
        logger.start_block("Writing to emme2 input file")
        full_path = os.path.join(current_emme2_tripgen_dir, 'inputtg')
        if not os.path.exists(full_path):
            os.makedirs('%s' % full_path)
        try:
            newfile = open(os.path.join(full_path, 'TAZDATA.MA2'), 'w')
            try:
                newfile.write(r"""c  from
c  prepared: %s
t matrices
m matrix="hhemp"
""" % time.strftime("%c", time.localtime(time.time())))
                tm_year = self._decade_floor(current_year)
                line_template = "%4d    %3d: %8.2f \n"
                for taz_id in range(1,max_zone_id+1):
                    pctmf = taz_col_set.get_attribute_by_id('pctmf',id=(taz_id,tm_year))
                    gqi = taz_col_set.get_attribute_by_id('gqi',id=(taz_id,tm_year))
                    gqn = taz_col_set.get_attribute_by_id('gqn',id=(taz_id,tm_year))
                    fteuniv = taz_col_set.get_attribute_by_id('fteuniv',id=(taz_id,tm_year))
                    density = taz_col_set.get_attribute_by_id('den',id=(taz_id,tm_year))
                    
#                    pctmf = constant_taz_reader.get_value('pctmf', taz=taz_id, year=tm_year)
#                    gqi = constant_taz_reader.get_value('gqi', taz=taz_id, year=tm_year)
#                    gqn = constant_taz_reader.get_value('gqn', taz=taz_id, year=tm_year)
#                    fteuniv = constant_taz_reader.get_value('fteuniv', taz=taz_id, year=tm_year)
#                    density = constant_taz_reader.get_value('den', taz=taz_id, year=tm_year)
        
                    newfile.write(line_template % (taz_id, 101, pctmf))
                    newfile.write(line_template % (taz_id, 102, self.low_income_hh_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 103, self.low_mid_income_hh_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 104, self.upper_mid_income_hh_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 105, self.upper_income_hh_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 106, gqi))
                    newfile.write(line_template % (taz_id, 107, gqn))
                    newfile.write(line_template % (taz_id, 108, -1)) #total_pop_by_taz[taz_id])) # not used
                    if density == 1:  #Density
                        newfile.write(line_template % (taz_id, 109, self.retail_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 109, 0.0))
                    if density == 2:
                        newfile.write(line_template % (taz_id, 110, self.retail_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 110, 0.0))
                    if density == 3:
                        newfile.write(line_template % (taz_id, 111, self.retail_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 111, 0.0))
                    if density == 1:
                        newfile.write(line_template % (taz_id, 112, self.fires_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 112, 0.0))
                    if density == 2:
                        newfile.write(line_template % (taz_id, 113, self.fires_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 113, 0.0))
                    if density == 3:
                        newfile.write(line_template % (taz_id, 114, self.fires_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 114, 0.0))
                    if density == 1:
                        newfile.write(line_template % (taz_id, 115, self.gov_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 115, 0.0))
                    if density == 2:
                        newfile.write(line_template % (taz_id, 116, self.gov_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 116, 0.0))
                    if density == 3:
                        newfile.write(line_template % (taz_id, 117, self.gov_by_taz[taz_id]))
                    else:
                        newfile.write(line_template % (taz_id, 117, 0.0))
                    newfile.write(line_template % (taz_id, 118, self.educ_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 119, self.wtcu_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 120, self.manu_by_taz[taz_id]))
                    newfile.write(line_template % (taz_id, 121, fteuniv)) #univ-fte
                    tazs_for_122 = [58,59,60,71,72,73,84,85,86,150,251,266,489,578,687,688,797,868]
                    tazs_for_123 = [531,646,847,850,888,894,899,910]
                    if taz_id in tazs_for_122:
                        newfile.write(line_template % (taz_id, 122, gqn))
                    else:
                        newfile.write(line_template % (taz_id, 122, 0.0))
                    if taz_id in tazs_for_123:
                        newfile.write(line_template % (taz_id, 123, gqn))
                    else:
                        newfile.write(line_template % (taz_id, 123, 0.0))
                    if not(taz_id in tazs_for_122) and not(taz_id in tazs_for_123):
                        newfile.write(line_template % (taz_id, 124, gqn))
                    else:
                        newfile.write(line_template % (taz_id, 124, 0.0))
            finally:
                newfile.close()
        finally:
            logger.end_block()
        return os.path.join(full_path, 'TAZDATA.MA2')

    def _decade_floor(self, year):
        return int(round(year - 5, -1))
