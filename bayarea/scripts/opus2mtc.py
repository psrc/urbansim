# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# The MTC travel model input specifications can be found here:
#
# http://mtcgis.mtc.ca.gov/foswiki/Main/DataDictionary
#
# This script prepares the TazData, PopSynHousehold, PopSynPerson, and
# WalkAccessBuffers from opus bay area land use model output.

OPUS_HOUSEHOLD_TABLE = 'households'

import os
import sys
from optparse import OptionParser
from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.csv_storage import csv_storage
from numpy import array, zeros

if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option('-c', '--cache_path', dest='cache_path', type='string', 
        help='The filesystem path to the cache to export (required)')
    parser.add_option('-o', '--output_directory', dest='output_directory', 
        type='string', help='The filesystem path of the database to which '
            'output will be written (required)')

    (options, args) = parser.parse_args()

    cache_path = options.cache_path
    output_directory = options.output_directory
    
    if None in (cache_path, output_directory):
        parser.print_help()
        sys.exit(1)

    in_storage = flt_storage(storage_location=cache_path)
    out_storage = csv_storage(storage_location=output_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # PopSynHousehold

    # TODO: throughout this code, I assme that the data is clean (e.g., no
    # negative income, etc.)  Is this acceptable?
    logger.start_block('Preparing PopSynHousehold')
    opus_hh = in_storage.load_table(OPUS_HOUSEHOLD_TABLE)

    mtc_hh = {}
    mtc_hh['HHID'] = opus_hh['household_id']

    # TODO: Join HH and buildings on building id, then join in zones on
    # building id, then dump 'TAZ'
    # mtc_hh['TAZ'] = ???

    # TODO: What about PUMA serial number SERIALNO?
    # mtc_hh['SERIALNO'] = ???

    # TODO: Not sure what the PUMA5 is.  Four-digit integer indicating PUMA
    # geography from which the drawn household is from (not the PUMA where the
    # hosuehold is placed)  Huh?
    # mtc_hh['PUMA5'] = ???

    # TODO: I'm assuming income is HH income in 2000 dollars as required by MTC.
    mtc_hh['HINC'] = opus_hh['income']    

    mtc_hh['PERSONS'] = opus_hh['persons']

    # TODO: HHT is household type.  Hmm.  family v. non-family?  marriage
    # status?  gender of householder?
    # mtc_hh['HHT'] = ???

    # TODO: The hunittype field can apparently distinguish between housing,
    # institutional group, and non-institutional group.  But it's not showing
    # up in the output household table.  Can we add it to future runs?
    # mtc_hh['UNITTYPE'] = ???

    # TODO: According to
    # http://www.urbansim.org/Documentation/Parcel/HouseholdsTable, 'children'
    # column is boolean.  We need to know number of children for the travel
    # model.
    # mtc_hh['NOC'] = ???

    # From MTC docs, BLDGSZ is:
    # 1 - mobile home
    # 2 - one-family house detached from any other house
    # 3 - one-family house attached to one or more houses
    # 4 - a building with 2 apartments
    # 5 - a building with 3 or 4 apartments
    # 6 - a building with 5 to 0 apartments
    # 7 - a building with 10 to 19 apartments
    # 8 - a building with 20 to 49 apartments
    # 9 - a building with 50 or more apartments
    # 10 - a boat, RV, van, etc.
    
    # Maybe we can use building.residential_units and building_types.  But it
    # looks like boat/rv and mobile home are missing.  Maybe this is OK?
    # mtc_hh['BLDGSZ'] = ???

    # TODO: Looks like opus just has 1 and 2 for tenure.  Is this own and rent?
    # rent and own?  MTC requires:
    # 1 - owned by your or someone in this household with a mortgage or loan
    # 2 - owned by your or someone in this household free and clear
    # 3 - rented for cash rent
    # 4 - occupied without payment of cash rent
    mtc_hh['TENURE'] = opus_hh['tenure']

    # TODO: confirm mtc VEHICL can be 0.
    mtc_hh['VEHICL'] = opus_hh['cars']

    # TODO: for some reason, opus income has some negative values
    # 
    # 1 - 0 to 20k(-)
    # 2 - 20 to 50k
    # 3 - 50 to 100k
    # 4 - more than 100k
    # TODO: is there a better way to do this coding?
    def income2hinccat1(i):
        if i < 20000:
            return 1
        elif i < 50000:
            return 2
        elif i < 100000:
            return 3
        else:
            return 4
    mtc_hh['hinccat1'] = array(list(map(income2hinccat1, opus_hh['income'])))

    # 1 - 0 to 10k
    # 2 - 10 to 20k
    # 3 - 20 to 30k
    # 4 - 30 to 40k
    # 5 - 40 to 50k
    # 6 - 50 to 60k
    # 7 - 60 to 75k
    # 8 - 75 to 100k
    # 9 - more than 100k
    def income2hinccat2(i):
        if i < 0:
            logger.log_warning("Found hh income < 0")
            return -1
        if i < 10000:
            return 1
        elif i < 20000:
            return 2
        elif i < 30000:
            return 3
        elif i < 40000:
            return 4
        elif i < 50000:
            return 5
        elif i < 60000:
            return 6
        elif i < 75000:
            return 7
        elif i < 100000:
            return 8
        else:
            return 9
    mtc_hh['hinccat2'] = array(list(map(income2hinccat2, opus_hh['income'])))

    def hhagecat(a):
        if a >= 0  and a <= 64:
            return 1
        if a > 64:
            return 2
        else:
            logger.log_warning("Found age_of_head < 0")
            return -1
    mtc_hh['hhagecat'] = array(list(map(hhagecat, opus_hh['age_of_head'])))

    def hsizecat(s):
        if s >= 4:
            return 4
        else:
            return s
    mtc_hh['hsizecat'] = array(list(map(hsizecat, opus_hh['persons'])))

    # TODO: need family v. non-family
    # mtc_hh['hfamily'] = ???

    # TODO: Doesn't opus already calculate this?  Is it the same coding:
    # 0 - housing unit
    # 1 - institutional group quarters
    # 2 - non-institutional group quarters
    # mtc_hh['hunittype'] = ???

    mtc_hh['hNOCcat'] = opus_hh['children']

    # TODO: MTC docs say this is "number of workers in the hh category".  What
    # category?  Is this not just number of workers in the hh as in opus?
    # Probably not considering that we have hworkers later.
    mtc_hh['hwrkrcat'] = array([w if w < 4 else 3 for w in opus_hh['workers']])

    # TODO: These next categories are summaries of the household members of
    # certain ages.  How can we find this out?  Do we need to traverse the
    # many-to-one relationship of persons to households?  Can opus create these
    # columns?
    # mtc_hh['h0004'] = ???
    # mtc_hh['h0511'] = ???
    # mtc_hh['h1215'] = ???
    # mtc_hh['h1617'] = ???
    # mtc_hh['h1824'] = ???
    # mtc_hh['h2534'] = ???
    # mtc_hh['h3549'] = ???
    # mtc_hh['h5064'] = ???
    # mtc_hh['h6579'] = ???
    # mtc_hh['h80up'] = ???

    mtc_hh['hworkers'] = opus_hh['workers']

    # TODO: we need employment data such as number of full- and part-time
    # workers in the HH, college students, pre-school, driving aged, etc.
    # Maybe we need to traverse the many-to-one relationship between persons
    # and hh?
    # mtc_hh['hwork_f'] = ???
    # mtc_hh['hwork_p'] = ???
    # mtc_hh['huniv'] = ???
    # mtc_hh['hnwork'] = ???
    # mtc_hh['hretire'] = ???
    # mtc_hh['hpresch'] = ???
    # mtc_hh['hschpred'] = ???
    # mtc_hh['hschdriv'] = ???

    # TODO: this is just a remix of BLDGSZ
    # mtc_hh['htypdwel'] = ???

    # TODO: I'm assuming that opus data is own=1 and rent=2.  Is this right?
    mtc_hh['hownrent'] = opus_hh['tenure']

    # TODO: working and non-working students?
    # mtc_hh['hadnwst'] = ???
    # mtc_hh['hadwpst'] = ???

    # TODO: adult children aged 18-24?
    # mtc_hh['hadkids'] = ???

    mtc_hh['bucketBin'] = zeros(len(opus_hh['tenure']), dtype=int)

    # This seems to be exactly the same as PUMA5
    # mtc_hh['originalPUMA'] = mtc_hh['PUMA5']

    # TODO: probably can get this from building table or BLDGSZ
    # mtc_hh['hmultiunit'] = ???

    logger.log_note('Writing %d households to table...' % len(opus_hh['household_id']))
    out_storage.write_table(table_name='PopSynHousehold', table_data=mtc_hh,
                            append_type_info=False)
    logger.end_block()

    # PopSynPerson
    logger.start_block('Preparing PopSynPerson (UNIMPLEMENTED)')
    logger.end_block()

    # TazData
    logger.start_block('Preparing TazData (UNIMPLEMENTED)')
    logger.end_block()
