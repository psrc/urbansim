#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
        'zone_id = job.disaggregate(building.disaggregate(zone.zone_id))',
        'taz2012_id = job.disaggregate(building.disaggregate(zone.taz2012_id))',
        'mpa_id = job.disaggregate(building.disaggregate(zone.mpa_id))',
        'raz_id = job.disaggregate(building.disaggregate(zone.raz_id))',
        'raz2012_id = job.disaggregate(building.disaggregate(zone.raz2012_id))',
        'county_id = job.disaggregate(building.disaggregate(zone.county_id))',
        'tazi03_id = job.disaggregate(building.disaggregate(zone.tazi03_id))',
        'pseudo_blockgroup_id = job.disaggregate(building.disaggregate(zone.pseudo_blockgroup_id))',
        'census_place_id = job.disaggregate(building.disaggregate(zone.census_place_id))',
        # aggregate sector job totals:
        "is_public_job = numpy.in1d(job.sector_id, (21,22))",
        "is_industrial_job = numpy.in1d(job.sector_id, (2,5,6,8))",
        "is_entertainment_job = numpy.in1d(job.sector_id, (7,18,19))",
        "is_office_job = numpy.in1d(job.sector_id, (9,10,11,12,13))",
        "is_homebased_job = job.home_based_status==1",
        "is_nonhomebased_job = job.home_based_status==0",
        # individual sector job totals:
        "is_agricultural_job = job.sector_id==1",
        "is_mining_job = job.sector_id==2",
        "is_utilities_job = job.sector_id==3",
        "is_construction_job = job.sector_id==4",
        "is_manufacturing_job = job.sector_id==5",
        "is_wholesale_job = job.sector_id==6",
        "is_retail_job = job.sector_id==7",
        "is_transportation_job = job.sector_id==8",
        "is_information_job = job.sector_id==9",
        "is_finance_job = job.sector_id==10",
        "is_realestate_job = job.sector_id==11",
        "is_professional_job = job.sector_id==12",
        "is_healthcare_job = job.sector_id==16",
        "is_accomodation_job = job.sector_id==18",
        "is_foodservice_job = job.sector_id==19",
        "is_pubfedstate_job = job.sector_id==21",
        "is_publocal_job = job.sector_id==22",
        # aliases for older v3x configurations
        'is_pub_employment = (job.sector_id == 20)',

        'sector_group = job.disaggregate(sector.sector_group)',
           ]


